# AI Use Log
## CJ Snyder | AI 180 | P3 — 3D Model Lifecycle Pipeline

---

Throughout P3, Claude (Sonnet 4.6) was used as a builder and documentarian under my direction. The ideas, goals, and decisions were mine — Claude produced and revised based on what I asked for.

**Transfer tool development.** Claude wrote and iterated on the core Python/Flask application: `app.py`, `analyzer.py`, `knowledge_base.py`, `claude_ai.py`, and the HTML front end. I directed the feature set, defined the use case, and tested the tool by running real model files through it. Claude built to my specifications.

**Interactive pipeline visualization.** Claude generated the interactive 3D lifecycle pipeline HTML file (`3d-lifecycle-pipeline.html`), which visualizes the full model creation-to-engine flow. I defined the pipeline stages and reviewed the output.

**Vercel deployment.** Claude worked through the configuration required to deploy the Flask app on Vercel, including restructuring the entry point, adapting file storage for a serverless environment, and resolving multiple config errors. I chose Vercel and directed Claude to find workarounds when it suggested switching platforms.

**Systems map.** Claude drafted the Mermaid systems map after I identified the actors (CJ, 3ds Max, ZBrush, the transfer tool, Unity/Unreal), described the three feedback loops from my own experience, and confirmed the leverage points. The content came from me; Claude formatted and structured it.

**ESF documentation.** Claude drafted Records of Resistance #02, #03, and #04, and the Five Questions, based on real moments and my own answers. I reviewed and approved each before it was committed.

**Code fixes.** Claude applied a set of targeted fixes to the codebase — path traversal vulnerability, Vercel environment check, upload size limit, bare except blocks, and `.gitignore` cleanup — after I reviewed each change and confirmed it before execution.

**Git workflow.** Claude managed all commits and pushes to GitHub, including a workaround for a persistent git lock file caused by the Windows/OneDrive filesystem that I was unable to resolve directly.

---

*What AI did not do: choose the project, define the problem, select the tools, make judgments about the pipeline, or decide when work was complete. I reviewed and checked over all work AI produced — including every code change, document, and configuration — before it was accepted or committed. That review was mine.*
