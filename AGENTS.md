# TradeGate Consultants Website — Working Context

This repository is the live public website of TradeGate Consultants (Django). Continue it; keep every approved feature working. The shared context lives in `context/`.

Read these files in order before any change:

1. `context/project-overview.md` — business, services, audiences, pages and features, partner-event status.
2. `context/architecture.md` — stack, deployment, models, invariants, backups.
3. `context/ui-context.md` — brand and the list of protected, approved UI.
4. `context/code-standards.md` — Django/Tailwind/translation conventions and the checks before pushing.
5. `context/ai-workflow-rules.md` — how to work, owner-only decisions, legal guardrails.
6. `context/progress-tracker.md` — current state, open issues, next steps.

## Non-negotiable

- Do only what is asked. Never remove, hide or restyle an approved feature as a side effect.
- Pushing to `main` deploys live: only with the owner's go-ahead, after tests and a visual check.
- Partner events: shown only with written permission; never show organiser websites, contacts or company names.
- Contact enquiries must always be saved and emailed.
- Copy in "we" voice. Drafts only for emails; never send.
- Keep secrets, databases and media out of Git.
- Update `context/progress-tracker.md` after every meaningful change.

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` contain the same text; keep them aligned.
