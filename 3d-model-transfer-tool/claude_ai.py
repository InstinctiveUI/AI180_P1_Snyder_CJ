"""
Claude AI integration for 3D Model Transfer Assistant.
Requires ANTHROPIC_API_KEY environment variable.
anthropic is imported lazily to avoid Vercel cold-start timeout.
"""
import os

SYSTEM_PROMPT = (
    "You are an expert 3D modeling and file-transfer assistant embedded in the "
    "3D Model Transfer Assistant tool. You help users understand mesh issues, choose "
    "the right export formats, and troubleshoot problems when moving models between "
    "applications such as Blender, Maya, Unity, Unreal Engine, ZBrush, 3ds Max, "
    "Cinema 4D, Substance Painter, and similar tools. "
    "Keep responses concise and practical. Use plain English. "
    "When discussing formats or issues, be specific and actionable."
)


def _get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    except Exception:
        return None


def _no_key():
    return {"error": "ANTHROPIC_API_KEY is not set. Add it to your Vercel environment variables."}


def get_analysis_summary(report, source_app="", target_app=""):
    client = _get_client()
    if not client:
        return _no_key()
    stats = report.get("stats", {})
    issues = report.get("issues", [])
    dims = stats.get("dimensions_mm", {})
    dim_str = (str(round(dims.get('x',0),1)) + " x " + str(round(dims.get('y',0),1)) + " x " + str(round(dims.get('z',0),1)) + " units") if dims else "unknown"
    lines = [
        "File: " + report.get("filename", "unknown") + " (" + report.get("format", "?").upper() + ")",
        "Vertices: " + str(stats.get("vertices", 0)) + "  Faces: " + str(stats.get("faces", 0)),
        "Watertight: " + str(stats.get("is_watertight", "unknown")) + "  Dimensions: " + dim_str,
    ]
    if source_app:
        lines.append("Source app: " + source_app)
    if target_app:
        lines.append("Target app: " + target_app)
    if issues:
        lines.append("\nDetected issues:")
        for iss in issues:
            fix = " (auto-fixable)" if iss.get("auto_fixable") else ""
            lines.append("  [" + iss["severity"].upper() + "] " + iss["title"] + ": " + iss["description"] + fix)
    else:
        lines.append("\nNo issues detected.")
    context = "\n".join(lines)
    prompt = (context + "\n\nGive the user: 1. A 2-3 sentence plain-English summary of what was found. "
              "2. The single most important action they should take. "
              "3. If a target app is specified, one specific tip for that workflow. "
              "Be concise, under 120 words total.")
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"summary": msg.content[0].text}
    except Exception as exc:
        return {"error": str(exc)}


def get_ai_format_advice(source_app, target_app, model_stats=None):
    client = _get_client()
    if not client:
        return _no_key()
    lines = ["The user wants to move a 3D model from " + source_app + " to " + target_app + "."]
    if model_stats:
        v = model_stats.get("vertices", 0)
        fc = model_stats.get("faces", 0)
        wt = model_stats.get("is_watertight")
        if v or fc:
            lines.append("Model size: " + str(v) + " vertices, " + str(fc) + " faces.")
        if wt is not None:
            lines.append("Mesh is " + ("watertight" if wt else "NOT watertight") + ".")
    prompt = (" ".join(lines) + "\n\nPlease give: 1. The best 1-2 export formats for this workflow and why. "
              "2. The top 2-3 things that commonly break in a " + source_app + " to " + target_app + " transfer. "
              "3. One workflow tip most people overlook. Be specific. Under 150 words.")
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"advice": msg.content[0].text}
    except Exception as exc:
        return {"error": str(exc)}


def chat(messages, context=None):
    client = _get_client()
    if not client:
        return _no_key()
    system = SYSTEM_PROMPT
    if context:
        extras = []
        if context.get("filename"):
            extras.append("Uploaded file: " + context["filename"])
        if context.get("source_app"):
            extras.append("Source app: " + context["source_app"])
        if context.get("target_app"):
            extras.append("Target app: " + context["target_app"])
        if context.get("stats"):
            s = context["stats"]
            extras.append("Model: " + str(s.get("vertices",0)) + " verts, " + str(s.get("faces",0)) + " faces, watertight: " + str(s.get("is_watertight","unknown")))
        if context.get("issues"):
            titles = [i["title"] + " (" + i["severity"] + ")" for i in context["issues"][:6]]
            extras.append("Detected issues: " + ", ".join(titles))
        if extras:
            system = system + "\n\nCurrent session context:\n" + "\n".join("- " + e for e in extras)
    valid = [{"role": m["role"], "content": m["content"]} for m in messages if m.get("role") in ("user","assistant") and m.get("content")]
    if not valid:
        return {"error": "No messages provided."}
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=system,
            messages=valid,
        )
        return {"reply": response.content[0].text}
    except Exception as exc:
        return {"error": str(exc)}
