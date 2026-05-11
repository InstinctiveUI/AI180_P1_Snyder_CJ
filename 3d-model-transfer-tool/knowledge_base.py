"""
Knowledge base built from 3D_Model_Transfer_Issues.xlsx
Contains all transfer issues, format comparisons, causes, and tool recommendations.
"""

# --- Transfer Issues (Sheet 1, rows 1-3) ---
TRANSFER_ISSUES = [
    {
        "from": "CAD (SolidWorks, Fusion 360)",
        "to": "Mesh Modeler (Blender, Maya, 3ds Max)",
        "what_breaks": "Surface topology, parametric data",
        "details": "CAD uses NURBS (smooth curves); mesh modelers use polygons. Exporting to FBX/OBJ converts smooth surfaces into dense, often messy triangle meshes.",
        "broken_features": "Loss of parametric editing (e.g., changing a fillet radius).",
        "solution": "Use STEP files for better mesh generation."
    },
    {
        "from": "Game Engine (Unreal, Unity)",
        "to": "DCC Software (Blender, Maya)",
        "what_breaks": "Textures, material shaders, animation rigs",
        "details": "Game engines use specialized shaders that do not export back to standard formats.",
        "broken_features": "PBR textures may appear flat gray or incorrect. Complex animations may not map correctly.",
        "solution": "Manually rebind materials/rigs after transfer."
    },
    {
        "from": "Blender / DCC",
        "to": "CAD (SolidWorks, Fusion 360)",
        "what_breaks": "Geometry, scale",
        "details": "CAD programs struggle with high-poly models and complex mesh topology.",
        "broken_features": "Large models may fail to import entirely. Normals often flip, making parts invisible or broken.",
        "solution": "Decimate mesh before export; check normals."
    },
]

# --- 3D Print Transfer Issues (Sheet 1, rows 6-11) ---
PRINT_ISSUES = [
    {
        "issue": "Incorrect Scale / Size",
        "category": "Scale Mismatch",
        "symptom": "Model appears tiny or massive in the slicer.",
        "fix": "Set modeling software to Metric (mm) before exporting. Set 1 Blender unit = 1 mm.",
        "tools": "Blender Unit settings, slicer scale tool",
        "export_tip": "Verify units match between modeler and slicer."
    },
    {
        "issue": "Non-Manifold Geometry",
        "category": "Mesh Errors",
        "symptom": "Missing faces, holes, or edges shared by more than two faces — model is unprintable.",
        "fix": "Use repair software to fill holes and fix mesh errors.",
        "tools": "3D Builder, Meshmixer, Netfabb",
        "export_tip": "Run mesh analysis before export."
    },
    {
        "issue": "Unapplied Modifiers",
        "category": "Export Oversight",
        "symptom": "Mirror, Solidify, or Boolean modifiers don't carry over to the exported STL.",
        "fix": "Apply all modifiers in the modeling software before exporting.",
        "tools": "Blender: Ctrl+A modifiers",
        "export_tip": "Check modifier stack is empty before export."
    },
    {
        "issue": "Intersecting / Inverted Faces",
        "category": "Normal Errors",
        "symptom": "Faces are inside out or intersecting, causing slicer errors.",
        "fix": "Recalculate normals (Flip / Align Normals) in the modeling program.",
        "tools": "Blender: Shift+N recalculate outside",
        "export_tip": "Enable face orientation overlay to spot issues."
    },
    {
        "issue": "Low Resolution Mesh",
        "category": "Mesh Quality",
        "symptom": "Curved surfaces appear blocky or angular (faceted look).",
        "fix": "Increase subdivision or export resolution in exporter settings.",
        "tools": "Subdivision Surface modifier",
        "export_tip": "Balance poly count vs. file size for your printer."
    },
    {
        "issue": "File Format Errors",
        "category": "Compatibility",
        "symptom": "STL file not recognized, or ASCII vs. Binary STL mismatch.",
        "fix": "Use Binary STL for smaller files and better compatibility. Ensure .stl extension.",
        "tools": "Most slicers prefer Binary STL",
        "export_tip": "Binary STL is the safer default for all printers."
    },
]

# --- Format Comparison (Sheet 2) ---
FORMAT_INFO = {
    "obj": {
        "name": "OBJ",
        "extension": ".obj / .mtl",
        "geometry": "Excellent",
        "textures": "Basic (MTL)",
        "animation": None,
        "best_for": "Static geometry exchange",
        "limitations": "Breaks animation and complex PBR material mapping."
    },
    "fbx": {
        "name": "FBX",
        "extension": ".fbx",
        "geometry": "Good",
        "textures": "Good",
        "animation": "Good",
        "best_for": "Animated characters (industry standard)",
        "limitations": "Proprietary; version differences cause issues between Autodesk/Maya/Blender."
    },
    "stl": {
        "name": "STL",
        "extension": ".stl",
        "geometry": "Raw only",
        "textures": None,
        "animation": None,
        "best_for": "3D printing",
        "limitations": "No color, textures, or animation — raw geometry only."
    },
    "glb": {
        "name": "GLTF/GLB",
        "extension": ".glb",
        "geometry": "Good",
        "textures": "Good (PBR)",
        "animation": "Good",
        "best_for": "Web sharing and real-time apps",
        "limitations": "Can lose specialized shader effects from offline renderers."
    },
    "gltf": {
        "name": "GLTF/GLB",
        "extension": ".gltf / .glb",
        "geometry": "Good",
        "textures": "Good (PBR)",
        "animation": "Good",
        "best_for": "Web sharing and real-time apps",
        "limitations": "Can lose specialized shader effects from offline renderers."
    },
    "step": {
        "name": "STEP",
        "extension": ".step / .stp",
        "geometry": "Excellent",
        "textures": None,
        "animation": None,
        "best_for": "CAD-to-CAD or CAD-to-mesh",
        "limitations": "No visual material data; geometry-focused."
    },
}

# --- Key Causes (Sheet 3) ---
KEY_CAUSES = [
    {
        "cause": "Scale Mismatch",
        "description": "Different software uses different default units.",
        "example": "Meters vs. Millimeters vs. Inches — models appear tiny or gigantic."
    },
    {
        "cause": "Axis Orientation",
        "description": "Software disagrees on which axis is 'up'.",
        "example": "Blender (Z-up) vs. Unity (Y-up) — models appear rotated."
    },
    {
        "cause": "Texture Paths",
        "description": "Image file links break when moved between systems.",
        "example": "MTL files can't find texture images after transfer."
    },
]

# --- Recommended Tools (Sheet 3) ---
RECOMMENDED_TOOLS = [
    {
        "tool": "Speckle",
        "description": "Open-source connector bridging CAD and mesh software.",
        "use_case": "Bridges Revit, Rhino, AutoCAD with Blender while keeping data organized."
    },
    {
        "tool": "3D Builder",
        "description": "Free Microsoft app for model repair.",
        "use_case": "Repairs broken STL files."
    },
    {
        "tool": "MeshMixer",
        "description": "Mesh cleanup and editing tool.",
        "use_case": "Cleans up and cuts models when geometry is broken."
    },
]

# --- App categories for the UI ---
APP_CATEGORIES = {
    "Blender": "Mesh Modeler",
    "Maya": "Mesh Modeler",
    "3ds Max": "Mesh Modeler",
    "Cinema 4D": "Mesh Modeler",
    "ZBrush": "Mesh Modeler",
    "SolidWorks": "CAD",
    "Fusion 360": "CAD",
    "AutoCAD": "CAD",
    "Rhino": "CAD",
    "Inventor": "CAD",
    "Unity": "Game Engine",
    "Unreal Engine": "Game Engine",
    "Godot": "Game Engine",
    "Cura": "3D Print Slicer",
    "PrusaSlicer": "3D Print Slicer",
    "OrcaSlicer": "3D Print Slicer",
    "Three.js": "Web / Real-time",
    "Sketchfab": "Web / Real-time",
    "Web Browser (GLTF)": "Web / Real-time",
}

# --- Format recommendations based on source -> target ---
def get_recommended_format(source_app, target_app):
    src_cat = APP_CATEGORIES.get(source_app, "Unknown")
    tgt_cat = APP_CATEGORIES.get(target_app, "Unknown")

    recommendations = []

    if tgt_cat == "3D Print Slicer":
        recommendations.append({"format": "STL", "reason": "Universal 3D printing format, supported by all slicers.", "priority": 1})
        recommendations.append({"format": "OBJ", "reason": "Backup option if STL has issues; preserves some material info.", "priority": 2})
    elif tgt_cat == "CAD" and src_cat == "Mesh Modeler":
        recommendations.append({"format": "STEP", "reason": "Best geometry preservation for CAD import.", "priority": 1})
        recommendations.append({"format": "OBJ", "reason": "Fallback — CAD may struggle with high-poly meshes.", "priority": 2})
    elif tgt_cat == "Mesh Modeler" and src_cat == "CAD":
        recommendations.append({"format": "STEP", "reason": "Preserves geometry better than FBX/OBJ from CAD sources.", "priority": 1})
        recommendations.append({"format": "FBX", "reason": "Good if you need materials; watch for messy triangulation.", "priority": 2})
        recommendations.append({"format": "OBJ", "reason": "Simple static geometry transfer.", "priority": 3})
    elif tgt_cat == "Game Engine":
        recommendations.append({"format": "FBX", "reason": "Industry standard for game engines; supports animation + materials.", "priority": 1})
        recommendations.append({"format": "GLTF/GLB", "reason": "Modern alternative with good PBR support.", "priority": 2})
    elif tgt_cat == "Web / Real-time":
        recommendations.append({"format": "GLTF/GLB", "reason": "The standard for web 3D — compact, PBR-ready.", "priority": 1})
        recommendations.append({"format": "OBJ", "reason": "Simpler fallback for static scenes.", "priority": 2})
    elif src_cat == "Game Engine" and tgt_cat == "Mesh Modeler":
        recommendations.append({"format": "FBX", "reason": "Best bet for preserving animations and rigs.", "priority": 1})
        recommendations.append({"format": "GLTF/GLB", "reason": "Good PBR material preservation.", "priority": 2})
    else:
        recommendations.append({"format": "FBX", "reason": "Widely supported general-purpose format.", "priority": 1})
        recommendations.append({"format": "OBJ", "reason": "Simple and reliable for static geometry.", "priority": 2})
        recommendations.append({"format": "GLTF/GLB", "reason": "Modern format with good material support.", "priority": 3})

    return recommendations


def get_relevant_issues(source_app, target_app):
    src_cat = APP_CATEGORIES.get(source_app, "Unknown")
    tgt_cat = APP_CATEGORIES.get(target_app, "Unknown")
    issues = []

    for ti in TRANSFER_ISSUES:
        from_match = any(k.lower() in ti["from"].lower() for k in [source_app, src_cat])
        to_match = any(k.lower() in ti["to"].lower() for k in [target_app, tgt_cat])
        if from_match or to_match:
            issues.append(ti)

    if tgt_cat == "3D Print Slicer":
        issues.extend(PRINT_ISSUES)

    return issues
