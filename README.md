# Agentic Engineering Skill

A Codex/agentskills-style Skill that turns Matt Van Horn's June 2026 agentic engineering workflow notes into reusable agent behavior.

This repository also packages the Skill as a Codex plugin marketplace entry, so it can be installed from the Codex Plugins UI or CLI. It does not reproduce the source article; it paraphrases the workflow into compact instructions, references, guardrails, and examples that an agent can load when planning and executing work.

## What It Does

- Pushes substantial work through a plan-first loop.
- Treats fresh research as a default step before durable decisions.
- Keeps the user in the taste, judgment, and react-and-redirect role.
- Supports code work, strategy docs, meeting transcripts, product specs, launch materials, and other knowledge work.
- Encourages context compounding through notes, previous plans, and reusable skills.
- Adds guardrails for privacy, cost, sensitive automation, and overbuilding.

## Repository Layout

```text
.
  .agents/plugins/marketplace.json
  plugins/agentic-engineering/
    .codex-plugin/plugin.json
    skills/agentic-engineering/
      SKILL.md
      agents/openai.yaml
      references/
agentic-engineering/
  SKILL.md
  agents/openai.yaml
  references/
    bootstrap-setup.md
    examples.md
    hack-map.md
```

## Install As A Codex Plugin

Install the marketplace from GitHub:

```bash
codex plugin marketplace add alexwang91/agentic-engineering-skill
```

Then install the plugin:

```bash
codex plugin add agentic-engineering@agentic-engineering
```

Restart Codex or start a new thread after installing so the bundled skill metadata is loaded.

You can also open the Codex app, go to **Plugins**, select the Agentic Engineering marketplace, and install **Agentic Engineering**.

## Share In A Workspace

After installing locally, you can share it with members of your ChatGPT workspace from the Codex app:

1. Open **Plugins**.
2. Go to **Created by you**.
3. Open **Agentic Engineering**.
4. Select **Share** and choose people, groups, or copy a share link.

Workspace sharing does not publish the plugin to the public Plugin Directory. It keeps access inside your workspace or organization boundary.

## Public Directory Status

The current Codex manual documents local, repo, and workspace plugin distribution. It does not document a self-serve submission flow for OpenAI's public curated plugin directory. This repository is packaged so it is ready for a repo marketplace and workspace sharing; a public OpenAI-curated listing would still require whatever review or partner process OpenAI makes available.

## Install As A Standalone Skill

Clone the repository:

```bash
git clone https://github.com/alexwang91/agentic-engineering-skill.git
```

Install into Codex skills on macOS or Linux:

```bash
mkdir -p ~/.codex/skills
cp -R agentic-engineering-skill/agentic-engineering ~/.codex/skills/agentic-engineering
```

Install into Codex skills on Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\agentic-engineering-skill\agentic-engineering" "$env:USERPROFILE\.codex\skills\agentic-engineering"
```

If `CODEX_HOME` is set, install under `$CODEX_HOME/skills` instead.

## Use

Example prompts:

```text
Use $agentic-engineering to turn this bug report into a plan and fix it.
```

```text
Use $agentic-engineering to turn this meeting transcript into a product strategy memo.
```

```text
Bootstrap full agentic engineering setup for this machine.
```

The Skill should also trigger naturally for mentions of agentic engineering, compound engineering, `/ce-plan`, `/ce-work`, `/last30days`, `plan.md`, cmux, research-first execution, human signal, or reusable agent workflows.

## Automatic Triggering

Automatic triggering is enabled through two pieces:

- `agentic-engineering/SKILL.md` has a broad `description` with the trigger phrases Codex sees before loading the Skill.
- `agentic-engineering/agents/openai.yaml` sets `policy.allow_implicit_invocation: true`.

After installing or updating the Skill, restart Codex so the skill metadata is reloaded. Once reloaded, you can invoke it explicitly with `$agentic-engineering`, but Codex can also pick it automatically when the request matches the description.

## Validation

Validate the Skill metadata with the Codex skill creator helper:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./agentic-engineering
```

On Windows, use the equivalent path:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\agentic-engineering"
```

## Source Notes

Inspired by Matt Van Horn's June 2026 article, ["Every Agentic Engineering Hack I Know"](https://x.com/mvanhorn/status/2061877533885473181), and the user's provided brief. Public summaries are available from independent readers such as [SOTA Sync](https://sotasync.com/reader/2026-06-03-mvanhorn-agentic-engineering-hacks/).
