# Cycle A → B: Iteration Documentation
## CJ Snyder | AI 180 | P3 — 3D Model Lifecycle Pipeline

---

## Baseline: Cycle A (End of P2)

**What existed at the start of P3:**

The tool at the end of P2 was a working Python/Flask web application that could:
- Accept an uploaded 3D model file (STL, OBJ, FBX, GLB, PLY, DAE, 3DS)
- Run basic mesh analysis: vertex/face counts, watertight check, normal orientation, degenerate faces, scale
- Suggest recommended export formats based on source and target application
- Apply basic auto-fixes: hole-filling, normal correction, scale adjustment, debris removal
- Write an activity log in Markdown recording what was done to each file

What it could not do:
- Explain its analysis in plain language
- Accept natural-language questions from the user
- Adapt its behavior based on the deployment environment (local vs. cloud)
- Defend itself against path traversal or unsafe file handling
- Run on anything other than a local machine

**Baseline file state (Cycle A):**

| File | State |
|------|-------|
| `app.py` | Routes working locally; no environment awareness; bare `except` blocks; no input sanitization |
| `analyzer.py` | Core analysis logic present; 6 bare `except: pass` blocks silently swallowing errors |
| `knowledge_base.py` | Format/issue reference data, complete |
| `claude_ai.py` | Not present — AI integration did not exist |
| `templates/index.html` | Front end present; no chat interface |
| `requirements.txt` | Present in tool subdirectory only; no root-level file for deployment |
| `.gitignore` | Missing `__pycache__/` and `*.pyc` entries |

---

## Changes: Cycle B (P3)

**What changed and why:**

**1. AI integration (new capability)**
Added `claude_ai.py` with three functions: plain-English analysis summaries, AI-powered format advice for a specific source→target workflow, and a multi-turn chat endpoint. The tool can now explain what it found and why, not just flag it. I defined the use case — I wanted users to be able to ask questions about their specific file, not just receive a report.

**2. Security fixes**
Applied `werkzeug.secure_filename()` to all three file-handling routes (`/api/analyze`, `/api/fix`, `/api/download`). Without this, a crafted filename like `../../etc/passwd` could escape the upload directory. This was a real vulnerability in Cycle A.

**3. Vercel environment awareness**
Added `_IS_VERCEL = os.environ.get('VERCEL') == '1'` to make storage paths and upload size limits switch automatically based on deployment environment. On Vercel: 4MB upload limit, `/tmp/` storage. Locally: 200MB limit, local `uploads/` directory.

**4. Error surface improvements**
Replaced 6 bare `except: pass` blocks in `analyzer.py` with `except Exception as e:` blocks that append a warning to the analysis report. Errors that previously disappeared silently now appear in the output.

**5. Vercel deployment**
Deployed the application to Vercel so it can run without a local Python environment. This required restructuring the entry point, adapting file paths for a read-only serverless filesystem, and resolving multiple configuration issues across multiple iterations.

**6. Systems map**
Built a Mermaid systems map (`AI180_P3_Snyder_CJ_SystemsMap.mmd`) showing the full 3D model lifecycle with named actors, typed flows, three balancing feedback loops, and three leverage points. This documents the problem the tool is solving at a systems level.

**7. `.gitignore` cleanup**
Added `__pycache__/` and `*.pyc` to `.gitignore` and removed already-tracked compiled files from the repository.

---

## Peer Test Plan

**What a peer tester needs:**
- A browser (the tool runs on Vercel — no local setup required)
- One or more 3D model files in any supported format: STL, OBJ, FBX, GLB, GLTF, PLY, DAE, or 3DS

**Test sequence:**

| Step | What to do | What to look for |
|------|------------|-----------------|
| 1 | Open the tool URL | Page loads without errors |
| 2 | Select a source app (e.g., ZBrush) and target app (e.g., Unreal Engine) | Format recommendations appear with known transfer issues listed |
| 3 | Upload a 3D model file | Analysis report appears: vertex/face counts, issues found, auto-fixable flags |
| 4 | Click "Get AI Summary" | Plain-English summary of what the analysis found and what to do about it |
| 5 | Click "Auto-Fix" with a format selected | Fixed file is generated and available for download |
| 6 | Download the fixed file | File downloads; open in a 3D application to confirm it is valid |
| 7 | Type a question into the chat (e.g., "Why does my model look inside-out?") | Claude responds with a relevant answer |

**Known limitations at time of peer test:**
- Upload limit is 4MB on Vercel (serverless constraint); larger files require a local run
- Processing time on first request may be slow (cold start)
- The fix step cannot repair every issue type — some require the originating application

---

## What Held from Cycle A

The core use case did not change: the tool is for people who move 3D models between applications and need to know what is wrong and how to fix it. The format recommendation logic, the knowledge base of transfer issues, and the auto-fix approach all carried forward from P2. The goal of keeping the human in control of the decision — the tool flags and suggests, but does not modify anything without a deliberate action — also held.

---

## Reflection on the Cycle

The biggest change between A and B was adding AI to a tool that was itself built to work alongside AI. That created a strange loop — the tool was already about using structured information to handle a workflow, and now it could explain itself. The most important thing I kept from Cycle A was the boundary: AI assists within the tool, but every action the tool takes on a file still requires a deliberate click from the user. That did not change.

The Vercel deployment was the hardest part of Cycle B and the one I had to push hardest on. The AI recommended a different platform at least once. I held the platform choice, and the constraints of Vercel shaped several of the other decisions — the environment check, the upload limit, the `/tmp/` storage. Those constraints ended up being good design pressure.

---

*AI 180 | P3 — Cycle A → B Iteration Document*
