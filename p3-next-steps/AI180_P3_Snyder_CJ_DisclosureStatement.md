---
type: disclosure-statement
course: "AI 180"
project: "P3 — 3D Model Lifecycle Pipeline"
author: "CJ Snyder"
date: "2026-05-25"
---

# AI Collaboration Disclosure Statement

**Course:** AI 180
**Project:** P3 — 3D Model Lifecycle Pipeline
**Author:** CJ Snyder
**Date:** 2026-05-25

---

## Tool

Claude (Sonnet 4.6) by Anthropic, accessed through the Cowork desktop application.

---

## Role of AI

Claude served as builder, documentarian, and deployment technician throughout P3, working under my direction. Specific contributions:

**Application development.** Claude wrote the core Python/Flask application — `app.py`, `analyzer.py`, `knowledge_base.py`, `claude_ai.py` — and the HTML front end, building to my specifications and revising when results did not match my intent. I defined the feature set, the use case, and what the tool was for. Claude built it.

**Interactive visualization.** Claude generated the interactive 3D lifecycle pipeline HTML (`3d-lifecycle-pipeline.html`), which maps the full model creation-to-engine flow. I identified the stages and reviewed the output.

**Vercel deployment.** Claude worked through the configuration required to deploy the app on Vercel — restructuring the entry point, adapting file storage for a serverless environment, and resolving multiple config errors across many iterations. I chose Vercel and directed Claude to continue when it recommended a different platform.

**Systems map.** Claude formatted and structured the Mermaid systems map after I identified the actors, described the feedback loops from my own experience, and determined the leverage points. The conceptual content came from me.

**ESF documentation.** Claude drafted the Records of Resistance and the Five Questions based on my answers and real moments from the project. I reviewed and approved each document before it was committed.

**Code fixes and security.** Claude applied targeted fixes — path traversal vulnerability, environment-aware file limits, bare except blocks, `.gitignore` cleanup — after I reviewed each change and confirmed it before execution.

**Git workflow.** Claude managed commits and pushes to GitHub, including a workaround for a persistent lock file on the Windows/OneDrive filesystem.

---

## Role of Author

The problem I chose to solve is mine: I work in 3D modeling for game development and identified the file transfer bottleneck from direct experience. I defined what the tool does, what it should not do, and what the pipeline is for. I selected every tool and platform. I tested the application using real 3D model files. I made every consequential decision about scope, direction, and what to keep or reject. I reviewed all code, configuration, and documentation Claude produced before it was accepted or committed.

My Position Statement, written before any AI engagement, is on file in `p3-next-steps/position-statement.md`.

---

## Verification

I ran actual 3D model files through the tool to confirm that the analysis, auto-fix, and export functions work as intended. I read and understood the code changes Claude applied before accepting each one.

---

## Records of Resistance

Three documented instances where I rejected or substantially revised AI output:

- **RoR #02** — Claude concluded a persistent git lock file was a fundamental incompatibility and told me to run git commands from my own terminal. I directed Claude to find a workaround instead; it solved the problem by cloning to a location outside the locked filesystem.
- **RoR #03** — When I asked how to deploy on Vercel, Claude recommended switching to a different platform based on the app's architecture. I rejected the redirect and directed Claude to adapt the app for Vercel anyway.
- **RoR #04** — Claude presented three leverage points in the systems map as roughly equal. I corrected the framing: the transfer tool is the central leverage point, not one of three independent variables. The map was revised to reflect that.

Full records: `p3-next-steps/record-of-resistance-02.md`, `record-of-resistance-03.md`, `record-of-resistance-04.md`.

---

## Five Questions Check

All five answered "yes" prior to submission. Full responses on file: `p3-next-steps/AI180_P3_Snyder_CJ_FiveQuestions.md`.

---

*The author takes full responsibility for the accuracy and integrity of this work.*
