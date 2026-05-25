# Case Study: 3D Model Lifecycle Pipeline
## CJ Snyder | AI 180 | P3

---

## Section 1: Inquire

**The problem I started with:**

I work in 3D modeling for game development. The workflow moves between multiple applications — modeling in 3ds Max or ZBrush, then bringing the result into a game engine like Unity or Unreal. Every time a model crosses that boundary, something can break. The axes interpret differently. The scale is off. Faces invert. Normals flip. What looked clean in the source application arrives broken in the destination.

My standard habit was to wait for the problem to appear and then look it up. That worked until it didn't — when deadline pressure was high and debugging a broken import ate hours I didn't have.

The question I brought into P3 came from P2: I had already built a basic tool that could detect transfer issues. What I didn't know at the start of P3 was whether I could take that tool further — make it deployable somewhere, make it explain itself, and map the larger system that creates the problem in the first place.

**What I already knew:**

I knew the common failure modes from direct experience: axis mismatches, scale inconsistencies, non-manifold geometry, inverted normals. I had documented these in P2 and built the core analysis and fix logic around them. What I didn't know was how to make the tool accessible outside a local Python environment, or how to make the system visible as a system rather than just a list of symptoms.

**Questions I brought into the project:**

- Can I deploy this so someone without Python installed can use it?
- Can AI explain the analysis results in plain language, not just flag issues?
- What does the larger pipeline look like when I map all the actors and forces?
- Where is the leverage point that actually matters?

---

## Section 2: Position

**Written before AI engagement on P3:**

I am pursuing the creative pipeline of creating models in video game development and a way to help people in my field bypass a bottleneck in the creation process.

What matters most: making sure the program — and AI's role in it — is a thinking partner, not a plug-and-pray tool. This tool should enable people to get work done faster but not do all the work and thinking for them. The pipeline of creation and the files themselves must survive, as well as the file formats and types. The decision-making stays on the human side.

What I will not compromise on: AI will not make its own decisions. Everything AI does has to be decided by me and something I ask for with a reason. I will not compromise on the use case, the type of program, or what it does to the files. It is a specific use case — that's it.

**Why this position mattered:**

This position created a hard line before I touched anything in P3. It meant that when AI suggested switching deployment platforms, I had already committed to Vercel — so I redirected rather than accepted. It meant that when AI framed three leverage points as roughly equal, I knew from my own experience that was wrong and corrected it. The position wasn't a document I wrote and forgot. It was what I checked against when something felt off.

---

## Section 3: Explore

**Generating options and pressure-testing the position:**

The first major exploration in P3 was the systems map. I came in with the actors already identified from my own experience: CJ as creator, 3ds Max and ZBrush as authoring tools, the transfer tool as an intervention point, Unity and Unreal as destination environments. What I didn't have structured was how those actors related to each other and where the feedback happened.

Working through the map with AI surfaced three feedback loops I recognized from practice but hadn't articulated: a Quality Feedback Loop where engine problems drive corrections in the source file, a Tool Refinement Loop where repeated errors push the user toward better export settings, and a Knowledge Accumulation Loop where each transfer failure builds expertise. These loops were real — I had experienced all three. AI organized the language. The content was mine.

The leverage point question is where I had to push back. AI presented three options as a balanced set — export settings, the transfer tool, and engine import settings. That framing was technically accurate but experientially wrong. The transfer tool is not one of three equal factors. It is the hinge. Everything on the source side collapses to a single moment when the file crosses into the destination environment, and that moment is where the transfer tool operates. I rejected the balanced framing and restructured the map to reflect that. That became Record of Resistance #04.

**The deployment question:**

When I asked about hosting the tool on Vercel, AI assessed the app's architecture and recommended Railway or Render instead. The reasoning was technically sound — Vercel has real constraints for heavy Python workloads. But accepting that recommendation would have let the AI determine my project's scope based on convenience. I held the platform choice and directed AI to adapt the app to Vercel's constraints instead. That became Record of Resistance #03.

The adaptation turned out to be generative: the constraints of Vercel (read-only filesystem, 4MB upload limit, cold start behavior) forced design decisions that made the code more explicit about its own environment. The limitations became design pressure.

---

## Section 4: Make

**What was built:**

The P3 tool is a Flask web application deployable on Vercel without requiring a local Python environment. It accepts 3D model file uploads, runs mesh analysis, returns structured issue reports, applies targeted auto-fixes, and exports repaired files. It adds three capabilities the P2 version did not have:

**AI integration:** Three new endpoints powered by Claude: a plain-English summary of the analysis report, AI-powered format advice for a specific source-to-target workflow, and a multi-turn chat so users can ask questions about their specific file.

**Security hardening:** The P2 version had a path traversal vulnerability in all three file-handling routes. P3 applies `werkzeug.secure_filename()` to every filename the application touches. The P2 version also had six bare `except: pass` blocks in the analyzer that silently swallowed errors. P3 replaces all six with explicit error capture that surfaces the warning in the analysis output.

**Environment awareness:** The application now detects whether it is running on Vercel or locally and adjusts storage paths and upload limits accordingly. This was a necessary change to make deployment functional and a good design change regardless — the app now knows its own context.

**The systems map:** A Mermaid diagram documenting the full 3D model lifecycle with named actors, typed information flows, three feedback loops, and three leverage points. The transfer tool is positioned at the center — the handoff point between creation software and game engine — rather than as one factor among several.

**What I held from my position:**

The tool still requires deliberate action from the user for everything consequential. It analyzes, suggests, and flags — but it does not modify a file without a user clicking Auto-Fix and selecting a format. That was non-negotiable from my position statement and it did not change.

**Where I had to intervene:**

During the Vercel deployment work, there were multiple iterations where the entry point broke in different ways — a Python 3 scoping bug where the exception variable was deleted before the error handler could use it, a template resolution failure because the Flask app loaded via importlib wasn't registered in `sys.modules`, line ending issues from the Windows filesystem that broke Vercel's static analyzer. Each of these required identifying the specific failure, understanding why it happened, and directing a targeted fix. I reviewed every change before it was applied.

---

## Section 5: Reflect

**What I kept, revised, and rejected from AI:**

I kept the core application code — the Flask routes, the analyzer logic, the Claude API integration — because it matched my specifications and I tested it with real files. I kept the systems map structure after revising the leverage point framing. I kept the ESF documentation (Records of Resistance, Five Questions) after reviewing each one for accuracy.

I revised the leverage point framing, the deployment platform, and the git workflow approach (from the AI's suggested workaround to one that actually solved the problem).

I rejected the recommendation to switch from Vercel to another platform. I rejected AI's initial framing of the three leverage points as equal. I rejected the suggestion to run git commands from my own terminal when the AI concluded the lock file problem was unsolvable from the sandbox.

**What I learned that I would not have learned without AI:**

I would not have built a deployable Flask application without AI assistance. That is true. What I learned in the process of directing that build was more specific: how serverless environments change what code has to know about itself, what a path traversal vulnerability actually looks like and why `secure_filename` matters, how Python 3 handles exception variable scope in a way that breaks closures, and what it looks like when a framework can't resolve its own file path because the module loader didn't register it.

Those are things I now understand and could explain to someone else. I learned them not by writing the code but by holding responsibility for every change, reading the diffs, and tracking down the failures.

**What I learned despite AI:**

My editorial judgment developed through this project. The three Records of Resistance are evidence of that — each one documents a moment where AI's framing was plausible but wrong for my purpose, and where I identified the mismatch and redirected. That skill — noticing when something is technically reasonable but not actually what you meant — is the one I would point to as the real learning outcome.

**What I would do differently:**

I would write the systems map earlier. I built it toward the end of P3, but it clarified the problem better than any other artifact I produced. Starting from the systems view would have given me cleaner decisions about what to build and why throughout.

**Where I was most tempted to accept AI output uncritically:**

The deployment troubleshooting. When you are deep in configuration errors across many iterations, each fix that produces a new error makes the previous fix feel validated. I had to stay focused on the actual behavior — does the right thing happen at the URL — rather than on whether the current error was different from the last one. The temptation to accept "progress" when what I needed was "working" was the hardest part of P3 to hold against.

---

*AI 180 | P3 — Case Study: 3D Model Lifecycle Pipeline*
*ESF Phases: Inquire · Position · Explore · Make · Reflect*
