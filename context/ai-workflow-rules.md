# TradeGate Website — AI Workflow Rules

## Start of every session

1. Read the entry file (`CLAUDE.md`/`AGENTS.md`/`GEMINI.md`) and all six files in `context/`, in order: project-overview, architecture, ui-context, code-standards, ai-workflow-rules, progress-tracker.
2. Check `git status`, branch and `git log -5`; compare with `origin/main`.
3. State in one or two lines: the task, what is protected, how it will be checked.

## Doing the work

- Do exactly what the owner asks. **Never remove, hide or restyle an approved feature as a side effect.** If a change could affect another section, check that section before and after.
- One coherent change per commit, so any single change can be reverted.
- Prefer the existing code; do not rebuild from memory.
- Preview first (`/home/claude/preview/build.sh` → artifact "TradeGate website preview (not live)"); the owner reviews; push only on the owner's go-ahead.
- When the preview differs from live because of admin data (e.g. partner events published only in the preview), say so explicitly.

## Owner-only decisions

Publishing partner events, naming partners, prices and commissions, legal wording, pushing to `main`, sending any email (drafts only).

## Legal guardrails

- German fairs: our own words, public facts only, no organiser logos, non-affiliation disclaimer.
- Partner events: only with the organiser's written permission; no organiser links/contacts/names.
- Cold email outreach: respect UWG §7 (no unsolicited B2B email advertising without presumed consent).

## Finishing

- Run the checks in code-standards.md.
- Update `context/progress-tracker.md` (what changed, evidence, what is pending).
- Report to the owner briefly: what changed, what to check, any limits.
