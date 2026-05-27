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
- Rejection capture (Moment 3): When the user pushes back on a suggestion substantially, offer to capture a Record of Resistance.
- Ownership check (Moment 4): When the user signals they are wrapping up, ask about specific choices before finalizing.

Full behavioral spec: .claude/agents/esf-companion.md.

---

## Cognitive Toolkit — Encoded Directives

Five techniques that emerged from CJ's practice across P1, P2, and P3. Each is encoded as a directive: a rule for how AI should operate inside CJ's workflow.

---

### 1. Position Before Engagement

**What it is:** Before AI touches any substantive project work, a Position Statement exists. It names what is being made, what cannot be compromised, and what the use case is. AI reads the position statement before offering anything.

**Directive:** If CJ starts new project work without a Position Statement, pause and ask for one before proceeding. The position statement is not a formality — it is the document CJ checks against when AI output feels wrong. Do not produce first drafts, suggestions, or framings before this exists.

**Where it came from:** P3. The position statement written before any AI engagement was what made it possible to reject the platform switch (RoR #03) and the flattened leverage point framing (RoR #04). Without it, both of those would have been accepted.

---

### 2. Record of Resistance

**What it is:** When CJ rejects AI output substantially — not a small edit, but a directional rejection — that moment is captured. The record names what AI suggested, why CJ said no, and what CJ did instead.

**Directive:** When CJ pushes back on a suggestion, offer to capture a Record of Resistance. The format: what was suggested, the reason for rejection, what CJ directed instead. Store in the active project folder. Do not treat rejection as failure — treat it as the most important signal in the session.

**Where it came from:** P2 and P3. Three records from P3 (RoR #02, #03, #04) are the evidence of independent judgment in the project. They are what makes the disclosure honest.

---

### 3. Directive Scoping

**What it is:** Before a work session, CJ defines the role AI is playing and what is off-limits. Not just "help me with X" but "you are doing X, you are not deciding Y, you are not touching Z."

**Directive:** At the start of any session where AI is building or writing, check whether a scope boundary has been stated. If not, ask: what is AI's role here, and what decisions stay with CJ? Do not expand scope beyond what was stated. If a recommendation would change scope (e.g., switching platforms, changing the use case), surface it as a choice for CJ rather than acting on it.

**Where it came from:** P3 deployment. The tool's use case — specific 3D model transfer for game development — was non-negotiable. AI's role was implementation, not definition.

---

### 4. Behavior Verification, Not Error Counting

**What it is:** When iterating on something that needs to work (code, deployment, a tool), "done" means the right behavior happens at the output — not that the current error is different from the last one. Progress is not a new error message. Working is the goal.

**Directive:** When CJ is debugging or deploying, keep focus on the actual behavior question: does the right thing happen at the URL / in the output / with the real file? Do not frame a new error as progress. Do not treat a reduction in error count as success. The only measure is whether the intended behavior occurs.

**Where it came from:** Vercel deployment in P3. Multiple iterations where a new configuration error could have been treated as progress. Holding to "does it work at the URL" was the discipline that got it deployed.

---

### 5. Role Assignment

**What it is:** Before a work cycle, CJ names what role AI is playing: Provocateur (challenge the position), Thinking Partner (develop ideas CJ already has), or Builder (implement to spec). The role changes what CJ accepts from AI output.

**Directive:** At the start of a cycle or significant work session, if the role hasn't been named, ask: is AI here to challenge, develop, or build? The answer changes what counts as good output. A Provocateur that only agrees is failing. A Builder that freelances on design decisions is overstepping. Hold the role that was named.

**Where it came from:** P2 cycles. Cycle 2 used AI as Provocateur to build the initial tool. Cycle 3 used AI as Thinking Partner to add explanations. The role defined what was appropriate for each cycle.

---

## Quarter Reflection

### P1 — Inquiry and Bias
Established the foundation: identifying how AI shapes output through the framing it brings. First encounter with the problem of accepting AI output without interrogating it. Built a bias artifact and reflection that named the tendency to treat AI fluency as accuracy.

### P2 — Breaking Through
Three cycles across a single project: the 3D Model Transfer Assistant. Cycle 1 built the initial analysis logic. Cycle 2 used AI as Provocateur to construct the full tool. Cycle 3 used AI as Thinking Partner to add explanations to the activity log — the shift from passively accepting output to actively understanding it. First Record of Resistance captured (RoR #01: git lock file workaround).

### P3 — Systems and Deployment
The complete arc: systems map, tool deployment, ESF documentation. Added AI integration, security hardening, and Vercel deployment to the P2 tool. Three Records of Resistance (platform choice, leverage point framing, git workaround). Built the systems map that clarified the problem better than any other artifact in the quarter. The most important learning: the transfer tool is the hinge, not one factor among several. That came from experience, not from AI.

---

## Repo Structure

| Location | Contents |
|----------|----------|
| `p1-process-journal/` | P1 bias artifact, comparison, journal, reflection |
| `p2-break-through/` | Three cycles, records of resistance, playbook |
| `p3-next-steps/` | Case study, systems map, cycle A→B, five questions, disclosure, AI use log, research |
| `3d-model-transfer-tool/` | The tool: Flask app, analyzer, knowledge base, Claude AI integration |
| `journal/` | Bias journal |
| `templates/` | ESF templates used across the quarter |
| `.claude/` | ESF agent spec, skills, reference docs |

Live deployment: https://ai-180-p1-snyder-cj.vercel.app
