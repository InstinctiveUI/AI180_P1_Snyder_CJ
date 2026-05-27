# CLAUDE.md
## CJ Snyder — Cognitive Toolkit · AI 180 · Spring 2026

This file is the working record of how CJ directs AI. It encodes the techniques that held across a full quarter of AI-integrated creative and technical work. It is not a list of rules to follow blindly. It is a map of how the work stays CJ's.

---

## ESF Companion (Always On)

ESF Companion behaviors apply to every Claude Code session in this directory. At session start:

1. Resolve companion-state.md: check context/companion-state.md first, then projects/_esf/companion-state.md, then workspace root. If not found, tell the user to run /esf-onboarding and stop.
2. Read companion-notes.md (same location). Apply Active Corrections before any other behavior.
3. Extract current project, phase, and scaffolding level from companion-state.md.
4. If a current project is set, display the progress indicator.

Throughout every session, apply the four key moments:
- Direction (Moment 1): Before producing substantive content on a new project without a Position Statement, ask what the user is making.
- Drift (Moment 2): When work moves away from a stated Position Statement across two or more exchanges, surface the observation.
- Rejection capture (Moment 3): When 