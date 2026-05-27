---
type: record-of-resistance
context: "p3-next-steps"
project: "3D Model Lifecycle Pipeline"
date: "2026-05-11"
record-number: 2
---

# Record of Resistance

**Course:** AI 180
**Project:** P3 — 3D Model Lifecycle Pipeline
**Date:** 2026-05-11
**Record #:** 02

---

## What AI Suggested

When repeated git lock file errors blocked every push attempt, Claude concluded it was a fundamental incompatibility between the Linux sandbox and the Windows NTFS filesystem and told the user to run the git commands from their own terminal instead.

> "This is a fundamental incompatibility between my Linux sandbox and the Windows NTFS filesystem. The only reliable fix is to run git directly from your machine."

---

## Why I Rejected or Revised It

The suggestion handed the problem back to me when I had asked Claude to handle it. Accepting that answer would have meant doing the work myself — which defeats the point of using the tool. The AI was treating a technical wall as a reason to give up instead of a problem to solve.

---

## What I Did Instead

I pushed back and told Claude to find a workaround. Claude then cloned the repo directly into its Linux sandbox (bypassing the Windows filesystem entirely), added the files there, and pushed to GitHub successfully. The workaround worked and will be reused for all future pushes.

---

*Epistemic Stewardship Framework, Record of Resistance Template*
*Document moments where you deliberately did not follow an AI suggestion, and why.*
*These records make your creative judgment visible.*
