# Bootstrap Setup

Use this reference when the user asks for a full agentic engineering setup or a reusable workflow environment.

## Bootstrap Plan Shape

Create a master `plan.md` with these sections:

1. Goal and constraints
2. Current environment inventory
3. Required tools and optional tools
4. Security, privacy, and cost guardrails
5. Installation steps
6. Session orchestration
7. Research workflow
8. Notes and memory workflow
9. Verification checklist
10. Rollback and cleanup

## Environment Inventory

Check before recommending changes:

- Operating system and shell
- Existing agent tools and configured skills
- Git and GitHub status
- Notes or memory systems with CLI/API access
- Browser, transcript, and voice tools
- Hardware limits, battery needs, and remote-work requirements
- Security constraints around cookies, email, credentials, and device control

## Tool Categories

Prefer categories over hard dependencies; tools change quickly.

- Planning: `/ce-plan`, `plan.md`, implementation plans, acceptance checklists
- Execution: `/ce-work`, Codex, Claude Code, or another coding agent
- Fresh research: `/last30days`, official docs, web search, repo issue searches
- Parallel sessions: cmux, tmux, terminal profiles, worktrees
- Notes and memory: Bear, Obsidian, gbrain, Letta, or any CLI/API-backed memory tool
- Meeting context: Granola raw transcripts or equivalent transcript exports
- Real-life automation: Printing Press, Agent Cookie, device CLIs, email-triggered sessions
- Video or demos: script-first HTML/video render workflows

## Sensitive Setup Rules

- Ask before enabling permission bypass, remote control, email-triggered sessions, cookie sync, persistent credentials, or device control.
- Use allowlists for inbound triggers such as email.
- Keep secrets out of committed files.
- Document cost implications before recommending premium parallel agents or heavy subscriptions.

## Minimum Viable Setup

If the user wants the lightest version, start with:

1. A `plan.md` convention
2. A fresh-research step before durable decisions
3. A notes location for decisions and reusable patterns
4. A verification checklist before completion
5. A rule to create a skill after the same workflow repeats more than twice
