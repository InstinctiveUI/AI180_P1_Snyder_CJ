---
type: record-of-resistance
context: "p3-next-steps"
project: "3D Model Lifecycle Pipeline"
date: "2026-05-18"
record-number: 3
---

# Record of Resistance

**Course:** AI 180
**Project:** P3 — 3D Model Lifecycle Pipeline
**Date:** 2026-05-18
**Record #:** 03

---

## What AI Suggested

When asked how to host the 3D Model Transfer Tool on Vercel, Claude assessed the app's architecture — 200MB file uploads, local file storage, heavy Python dependencies, long processing times — and concluded that Vercel was a poor fit. It recommended switching to Railway or Render instead.

> "Honestly, a better fit for this app would be Railway or Render — both support persistent disks, larger uploads, and long-running processes, and Flask deploys to them in minutes with almost no code changes. Want me to walk you through one of those instead?"

---

## Why I Rejected or Revised It

The suggestion swapped out my goal for a different goal. I asked how to deploy on Vercel, not which platform to use. Accepting the redirect would have meant letting the AI decide the scope of my project based on what was technically convenient. The technical limitations were real, but they were mine to weigh — not Claude's to decide for me.

---

## What I Did Instead

I told Claude to walk me through Vercel anyway. Claude then adapted the app — redirecting file storage to `/tmp`, creating a proper entry point for Vercel's Python runtime, and working through multiple config errors until the deployment was functional.

---

*Epistemic Stewardship Framework, Record of Resistance Template*
*Document moments where you deliberately did not follow an AI suggestion, and why.*
*These records make your creative judgment visible.*
