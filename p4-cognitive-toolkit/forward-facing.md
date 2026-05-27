# Forward-Facing Section
## CJ Snyder | AI 180 | Spring 2026

---

## Where the Work Goes Next

The P3 systems map identified three leverage points in the 3D model lifecycle pipeline. The P3 tool addressed LP2 — the transfer tool at the handoff between authoring software and game engine. Two leverage points remain unaddressed, and one scaling problem exists in the current tool. Each of the following projects targets one of those gaps.

---

### Project 1 — Pre-Export Validation Tool (LP1)

**What it is:** A tool that runs inside or alongside 3ds Max and ZBrush to validate export settings before a file is ever sent to the transfer tool. Checks scale, normal orientation, axis alignment, and format selection at the source — catching errors before they compound downstream.

**Why it comes from this work:** The P3 systems map names LP1 (export settings) as the upstream leverage point: "Wrong values here break every step downstream." The current transfer tool catches and repairs errors after export. A validation tool would prevent them before export. That is an earlier intervention in the same system.

**Repo artifacts this builds from:**
- `p3-next-steps/AI180_P3_Snyder_CJ_SystemsMap.mmd` — LP1 defined and positioned
- `3d-model-transfer-tool/knowledge_base.py` — the existing catalog of format-specific failure modes becomes the validation ruleset
- `p3-next-steps/AI180_P3_Snyder_CJ_PositionStatement.md` — the use case constraint (specific 3D pipeline for game development) carries forward unchanged

---

### Project 2 — Engine Import Preset System (LP3)

**What it is:** A preset and standardization system for Unity and Unreal Engine import settings — scale multipliers, material path conventions, axis correction flags — so that each model arrives in the engine with known, consistent parameters rather than requiring manual correction after import.

**Why it comes from this work:** The P3 systems map names LP3 (engine import settings) as the downstream leverage point: "Standardising scale & material paths prevents repeat failures." The transfer tool gets the file to the engine. LP3 addresses what happens at the engine boundary. This closes the loop the transfer tool opened.

**Repo artifacts this builds from:**
- `p3-next-steps/AI180_P3_Snyder_CJ_SystemsMap.mmd` — LP3 defined; Feedback Loops 1 and 2 both originate at this boundary
- `p3-next-steps/AI180_P3_Snyder_CJ_CaseStudy.md` — Section 3 (Explore) describes the leverage point reasoning that identified this gap
- `3d-model-transfer-tool/knowledge_base.py` — engine-specific import behavior is already documented here; this project extends it into actionable presets

---

### Project 3 — Batch Asset Pipeline Manager

**What it is:** An extension of the current transfer tool that processes entire asset libraries rather than single files. In a real game production context, a single environment or character can involve dozens of models. The current one-file-at-a-time approach does not scale to that workload.

**Why it comes from this work:** The P3 tool proved that the analysis and fix logic works on individual files. Batch processing is a direct application of that logic at production scale. It does not require new analysis — it requires restructuring the tool's interface and processing loop to handle a directory of files, apply consistent settings across all of them, and return a summary report.

**Repo artifacts this builds from:**
- `3d-model-transfer-tool/app.py` — the existing routes and analysis pipeline; batch processing extends these
- `p3-next-steps/AI180_P3_Snyder_CJ_CycleAtoB.md` — Cycle B established the deployment and environment structure; Cycle C would be this
- `p3-next-steps/AI180_P3_Snyder_CJ_SystemsMap.mmd` — the reinforcing loop (Loop 4: skill compounding) applies here; a batch tool that reports patterns across many files accelerates learning even further

---

## What These Projects Have in Common

All three are grounded in the P3 systems analysis. The systems map was not just a documentation artifact — it identified what was built (LP2), what was not built (LP1 and LP3), and what scale of problem the existing tool does not yet address. These projects are the map's unfinished business.

---

*AI 180 | Forward-Facing Section | Spring 2026*
*Builds from: `p3-next-steps/AI180_P3_Snyder_CJ_SystemsMap.mmd`*
