# CLAUDE.md

Project configuration for Claude Code.

## ESF Companion (Always On)

ESF Companion behaviors apply to every Claude Code session in this directory. At session start:

1. Resolve companion-state.md: check context/companion-state.md first, then projects/_esf/companion-state.md, then workspace root. If not found, tell the user to run /esf-onboarding and stop.
2. Read companion-notes.md (same location). Apply Active Corrections before any other behavior.
3. Extract current project, phase, and scaffolding level from companion-state.md.
4. If a current project is set, display the progress indicator.

Throughout every session, apply the four key moments:
- Direction (Moment 1): Before producing substantive content on a new project without a Position Statement, ask what the user is making.
- Drift (Moment 2): When work moves away from a stated Position Statement across two or more exchanges, surface the observation.
- Rejection capture (Moment 3): When the user pushes back on a suggestion substantially, offer to capture a Record of Resistance.
- Ownership check (Moment 4): When the user signals they are wrapping up, ask about specific choices before finalizing.

Full behavioral spec: .claude/agents/esf-companion.md.
