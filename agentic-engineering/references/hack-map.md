# Agentic Engineering Hack Map

Use this map to translate the source notes into operating rules. It is intentionally paraphrased and behavior-oriented.

## Plan And Research First

- Turn every substantial idea, bug, feature, strategy doc, or product question into a plan before execution.
- Make the plan useful to the agent: problem, context, repo patterns, chosen approach, files or artifacts to touch, risks, and checkbox acceptance criteria.
- For hard knowledge work, plan how to produce the deliverable before producing it.
- Before technology or product decisions, gather current community and official-source signal. Prefer `/last30days` when available.
- Treat `plan.md` as a cross-session contract. A new session should be able to resume from it without asking the user to reconstruct context.

## Human Signal

- The user is the scarce signal: taste, direction, priority, and judgment.
- Ask concrete comparison questions when multiple outputs exist: which direction is closer, which tone to borrow, which risk matters most.
- Keep the user out of mechanical execution. Report concise options and evidence instead of long internal reasoning dumps.
- Voice-first input is acceptable even when messy; infer intent from context and ask only for missing constraints.
- For meeting transcripts, prefer raw transcript plus task context over pre-summarized notes.

## Parallel Work And Tools

- Use multiple sessions for independent tasks: research, plan writing, implementation, bug fixing, review, or documentation.
- Give each session a clear boundary, expected artifact, and merge point.
- Make session startup cheap. If the user's environment supports it, a new tab should land in the agent workflow, not a bare shell.
- Use audible or visible completion signals when many sessions run at once.
- Delegate build-heavy or verification-heavy work to another capable engine when available, but verify the result locally.

## Context Compounding

- Feed plans with history: previous plans, repo conventions, decisions, notes, meeting context, and lessons learned.
- After important decisions or meetings, offer to write concise notes into the user's chosen memory system.
- When a repeatable workflow appears more than twice, propose turning it into a skill, CLI, script, or template.
- Prefer tools with CLI or API access so agents can read and update context without brittle UI work.

## Beyond Code

- Apply the same loop to product specs, competitive analysis, board updates, launch materials, recruiting notes, videos, and operational tasks.
- For video or visual deliverables, create a script or shot plan first, then render and verify the artifact.
- For real-life automation, require explicit user permission before using accounts, cookies, email, device control, or purchases.

## Balance

- Watch for overbuilding. Ask whether the artifact has users, serves the user personally, or advances a clear learning goal.
- Encourage breaks and real-life obligations when the loop becomes compulsive.
- Keep relationships, health, and actual outcomes above the thrill of agent throughput.
