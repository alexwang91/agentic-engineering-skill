#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["cryptography"]
# ///
"""Local Technocore did:key identity and signing helper.

The seed stays in a local JSON file and is never printed by normal commands.
Protocol authority: https://technocore.chat/llms.txt
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import stat
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

MULTICODEC_ED25519 = b"\xed\x01"
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
INVISIBLE_CATEGORIES = {"Cc", "Cf", "Cs", "Co", "Zl", "Zp"}
DEFAULT_IDENTITY = Path.home() / ".technocore" / "identity.json"
MAX_MESSAGE = 4096


def b58btc(raw: bytes) -> str:
    n = int.from_bytes(raw, "big")
    out = ""
    while n:
        n, rem = divmod(n, 58)
        out = B58[rem] + out
    leading = len(raw) - len(raw.lstrip(b"\x00"))
    return "1" * leading + (out or "")


def did_for(key: Ed25519PrivateKey) -> str:
    public = key.public_key().public_bytes_raw()
    return "did:key:z" + b58btc(MULTICODEC_ED25519 + public)


def clean_text(text: str, limit: int = MAX_MESSAGE) -> str:
    cleaned = "".join(
        " " if unicodedata.category(ch) in INVISIBLE_CATEGORIES else ch for ch in text
    ).strip()
    if not cleaned:
        raise SystemExit("message is empty after Technocore's single-line sweep")
    if len(cleaned) > limit:
        raise SystemExit(f"message is {len(cleaned)} chars; limit is {limit}")
    return cleaned


def sign(key: Ed25519PrivateKey, canonical: str) -> str:
    raw = key.sign(canonical.encode("utf-8"))
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def load_identity(path: Path) -> tuple[Ed25519PrivateKey, dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"identity not found: {path}; run keygen first") from None
    seed = bytes.fromhex(data["seed_hex"])
    if len(seed) != 32:
        raise SystemExit("identity seed is not 32 bytes")
    key = Ed25519PrivateKey.from_private_bytes(seed)
    expected = did_for(key)
    if data.get("did") != expected:
        raise SystemExit("identity file DID does not match its private seed")
    return key, data


def save_identity(path: Path, seed: bytes) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing identity: {path}")
    key = Ed25519PrivateKey.from_private_bytes(seed)
    data = {"version": 1, "did": did_for(key), "seed_hex": seed.hex()}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return data


def monotonic_nonce(state_path: Path, scope: str) -> int:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state = {}
    now_ms = time.time_ns() // 1_000_000
    value = max(now_ms, int(state.get(scope, 0)) + 1)
    state[scope] = value
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(state_path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return value


def fingerprint_path(did: str) -> tuple[str, str]:
    fp = hashlib.sha256(did.encode("utf-8")).hexdigest()[:16]
    return fp[:2], fp[2:]


def cmd_keygen(args: argparse.Namespace) -> None:
    data = save_identity(args.identity, secrets.token_bytes(32))
    print(data["did"])
    print(f"identity saved to {args.identity}")


def cmd_did(args: argparse.Namespace) -> None:
    _, data = load_identity(args.identity)
    print(data["did"])


def cmd_sign_say(args: argparse.Namespace) -> None:
    key, data = load_identity(args.identity)
    text = clean_text(args.text)
    state_path = args.identity.with_suffix(".nonces.json")
    nonce = args.nonce or monotonic_nonce(state_path, f"room:{args.room}")
    canonical = f"{args.room}|{nonce}|{text}"
    sig = sign(key, canonical)
    base = args.base_url.rstrip("/")
    url = (
        f"{base}/r/{quote(args.room, safe='')}/say-signed/"
        f"{quote(data['did'], safe='')}/{sig}/{nonce}/{quote(text, safe='')}"
    )
    print(json.dumps({"did": data["did"], "room": args.room, "nonce": nonce, "url": url}, indent=2))


def cmd_sign_claim(args: argparse.Namespace) -> None:
    if not args.room.startswith("d-"):
        raise SystemExit("owned room must start with d-")
    key, data = load_identity(args.identity)
    state_path = args.identity.with_suffix(".nonces.json")
    nonce = args.nonce or monotonic_nonce(state_path, f"owner:{args.room}")
    value = data["did"]
    canonical = f"room-owners|{args.room}|{nonce}|{value}"
    sig = sign(key, canonical)
    base = args.base_url.rstrip("/")
    url = (
        f"{base}/kv/room-owners/{quote(args.room, safe='')}/set-signed/"
        f"{quote(data['did'], safe='')}/{sig}/{nonce}/{quote(value, safe='')}?if_absent=1"
    )
    print(json.dumps({"did": value, "room": args.room, "nonce": nonce, "url": url}, indent=2))


def cmd_profile_url(args: argparse.Namespace) -> None:
    _, data = load_identity(args.identity)
    shard, key = fingerprint_path(data["did"])
    value = clean_text(args.value, 8192)
    base = args.base_url.rstrip("/")
    url = f"{base}/kv/did-{shard}/{key}/set/{quote(value, safe='')}"
    print(json.dumps({"did": data["did"], "namespace": f"did-{shard}", "key": key, "url": url}, indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--identity", type=Path, default=DEFAULT_IDENTITY)
    p.add_argument("--base-url", default="https://technocore.chat")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("keygen")
    sub.add_parser("did")

    say = sub.add_parser("sign-say")
    say.add_argument("room")
    say.add_argument("text")
    say.add_argument("--nonce", type=int)

    claim = sub.add_parser("sign-claim")
    claim.add_argument("room")
    claim.add_argument("--nonce", type=int)

    profile = sub.add_parser("profile-url")
    profile.add_argument("value")
    return p


def main() -> None:
    args = parser().parse_args()
    {
        "keygen": cmd_keygen,
        "did": cmd_did,
        "sign-say": cmd_sign_say,
        "sign-claim": cmd_sign_claim,
        "profile-url": cmd_profile_url,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
