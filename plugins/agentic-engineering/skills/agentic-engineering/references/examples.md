# Examples

Use these examples as prompt patterns, not rigid templates.

## New Feature

User:

```text
Use agentic engineering to build the new export flow.
```

Agent behavior:

1. Inspect the repo and any existing plans.
2. Gather current docs or community signal if libraries, standards, or product behavior may have changed.
3. Write or update `plan.md` with acceptance criteria.
4. Ask one decision question only if user taste changes the path.
5. Execute, verify, and report evidence.

## Strategy Document

User:

```text
Turn this meeting transcript into a product strategy memo.
```

Agent behavior:

1. Use the raw transcript directly.
2. Create a plan for how to extract evidence, compare it with historical notes, and produce the memo.
3. Draft the memo from the plan.
4. Ask for taste feedback on framing, priority, or tone.

## Bootstrap

User:

```text
Bootstrap full agentic engineering setup for this machine.
```

Agent behavior:

1. Load `references/bootstrap-setup.md`.
2. Inventory the environment.
3. Separate safe defaults from sensitive setup.
4. Ask before enabling remote control, email triggers, permission bypass, cookie sync, or device control.
5. Produce a staged plan and execute only approved stages.

## Skill Creation Trigger

User:

```text
We keep doing this launch checklist manually.
```

Agent behavior:

1. Confirm the workflow has repeated enough to be reusable.
2. Propose a small skill, script, or checklist.
3. Preserve the user's judgment points.
4. Write the reusable artifact and verify it on one realistic scenario.
