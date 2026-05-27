"""
3D Model Analyzer & Auto-Fixer
Inspects uploaded model files for common transfer issues and attempts to repair them.
trimesh and numpy are imported lazily (inside functions) to avoid Vercel cold-start timeout.
"""
import os


def analyze_model(filepath):
    import trimesh
    import numpy as np

    report = {
        "filename": os.path.basename(filepath),
        "format": os.path.splitext(filepath)[1].lower().strip('.'),
        "issues": [],
        "warnings": [],
        "stats": {},
        "fixable": [],
    }

    try:
        loaded = trimesh.load(filepath, force=None)
    except Exception as e:
        report["issues"].append({
            "id": "load_failure",
            "title": "File Could Not Be Loaded",
            "severity": "critical",
            "description": "The file failed to load: " + str(e),
            "auto_fixable": False
        })
        return report

    if isinstance(loaded, trimesh.Scene):
        meshes = [g for g in loaded.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if not meshes:
            report["issues"].append({
                "id": "no_geometry",
                "title": "No Geometry Found",
                "severity": "critical",
                "description": "The file loaded as a scene but contains no mesh geometry.",
                "auto_fixable": False
            })
            return report
        mesh = trimesh.util.concatenate(meshes)
        report["stats"]["object_count"] = len(meshes)
    elif isinstance(loaded, trimesh.Trimesh):
        mesh = loaded
        report["stats"]["object_count"] = 1
    else:
        report["warnings"].append("File loaded as an unsupported type. Attempting to process anyway.")
        try:
            mesh = loaded.to_mesh() if hasattr(loaded, 'to_mesh') else None
        except Exception as e:
            report["warnings"].append("Could not convert object to mesh: " + str(e))
            mesh = None
        if mesh is None:
            report["issues"].append({
                "id": "unsupported_type",
                "title": "Unsupported Geometry Type",
                "severity": "critical",
                "description": "Could not convert the loaded object to a mesh.",
                "auto_fixable": False
            })
            return report

    report["stats"].update({
        "vertices": len(mesh.vertices),
        "faces": len(mesh.faces),
        "edges": len(mesh.edges) if hasattr(mesh, 'edges') else 0,
        "is_watertight": bool(mesh.is_watertight),
        "is_volume": bool(mesh.is_volume),
        "euler_number": int(mesh.euler_number) if hasattr(mesh, 'euler_number') else None,
    })

    bounds = mesh.bounds
    dimensions = bounds[1] - bounds[0]
    report["stats"]["dimensions_mm"] = {
        "x": round(float(dimensions[0]), 4),
        "y": round(float(dimensions[1]), 4),
        "z": round(float(dimensions[2]), 4),
    }
    report["stats"]["bounding_box_volume"] = round(float(np.prod(dimensions)), 4)

    max_dim = float(np.max(dimensions))

    if max_dim > 10000:
        report["issues"].append({
            "id": "scale_too_large",
            "title": "Model Appears Extremely Large",
            "severity": "warning",
            "description": "Largest dimension is " + str(round(max_dim, 1)) + " units. May indicate a meters/millimeters mismatch.",
            "auto_fixable": True,
            "fix_action": "scale_to_mm"
        })
        report["fixable"].append("scale_to_mm")
    elif max_dim < 0.1 and max_dim > 0:
        report["issues"].append({
            "id": "scale_too_small",
            "title": "Model Appears Extremely Small",
            "severity": "warning",
            "description": "Largest dimension is " + str(round(max_dim, 6)) + " units. Model may be in meters when millimeters are expected.",
            "auto_fixable": True,
            "fix_action": "scale_to_mm"
        })
        report["fixable"].append("scale_to_mm")

    if not mesh.is_watertight:
        report["issues"].append({
            "id": "not_watertight",
            "title": "Non-Watertight Mesh (Non-Manifold)",
            "severity": "error",
            "description": "The mesh has holes, open edges, or non-manifold geometry. This causes problems in 3D printing and some game engines.",
            "auto_fixable": True,
            "fix_action": "fill_holes"
        })
        report["fixable"].append("fill_holes")

    if hasattr(mesh, 'face_normals') and len(mesh.face_normals) > 0:
        try:
            if mesh.is_watertight and mesh.volume < 0:
                report["issues"].append({
                    "id": "inverted_normals",
                    "title": "Inverted Face Normals",
                    "severity": "error",
                    "description": "The mesh has inside-out faces (negative volume). This causes rendering and slicing issues.",
                    "auto_fixable": True,
                    "fix_action": "fix_normals"
                })
                report["fixable"].append("fix_normals")
        except Exception as e:
            report["warnings"].append("Could not check inverted normals: " + str(e))

    try:
        if not mesh.is_winding_consistent:
            report["issues"].append({
                "id": "inconsistent_winding",
                "title": "Inconsistent Face Winding",
                "severity": "warning",
                "description": "Face normals are not consistently oriented. Some faces may appear inside-out in certain applications.",
                "auto_fixable": True,
                "fix_action": "fix_winding"
            })
            report["fixable"].append("fix_winding")
    except Exception as e:
        report["warnings"].append("Could not check winding consistency: " + str(e))

    try:
        non_degen = mesh.nondegenerate_faces
        degen_count = len(mesh.faces) - non_degen.sum() if hasattr(non_degen, 'sum') else 0
        if degen_count > 0:
            report["issues"].append({
                "id": "degenerate_faces",
                "title": "Degenerate Faces Detected (" + str(degen_count) + ")",
                "severity": "warning",
                "description": "Found " + str(degen_count) + " zero-area or collapsed faces. These can cause rendering artifacts.",
                "auto_fixable": True,
                "fix_action": "remove_degenerate"
            })
            report["fixable"].append("remove_degenerate")
    except Exception as e:
        report["warnings"].append("Could not check degenerate faces: " + str(e))

    try:
        unique_faces = np.unique(np.sort(mesh.faces, axis=1), axis=0)
        dup_count = len(mesh.faces) - len(unique_faces)
        if dup_count > 0:
            report["issues"].append({
                "id": "duplicate_faces",
                "title": "Duplicate Faces (" + str(dup_count) + ")",
                "severity": "warning",
                "description": "Found " + str(dup_count) + " duplicate faces. These waste memory and can cause z-fighting.",
                "auto_fixable": True,
                "fix_action": "remove_duplicates"
            })
            report["fixable"].append("remove_duplicates")
    except Exception as e:
        report["warnings"].append("Could not check duplicate faces: " + str(e))

    if len(mesh.faces) > 500000:
        report["issues"].append({
            "id": "high_poly",
            "title": "High Polygon Count (" + str(len(mesh.faces)) + " faces)",
            "severity": "info",
            "description": "Very high polygon count may cause performance issues in game engines. Consider decimating for transfer.",
            "auto_fixable": True,
            "fix_action": "decimate"
        })
        report["fixable"].append("decimate")

    try:
        split = mesh.split(only_watertight=False)
        if len(split) > 1:
            tiny = sum(1 for s in split if len(s.faces) < 10)
            report["warnings"].append("Model has " + str(len(split)) + " disconnected components (" + str(tiny) + " with <10 faces).")
            if tiny > 0:
                report["issues"].append({
                    "id": "mesh_debris",
                    "title": "Mesh Debris Detected (" + str(tiny) + " tiny components)",
                    "severity": "info",
                    "description": "Found " + str(tiny) + " very small disconnected components that may be leftover boolean artifacts.",
                    "auto_fixable": True,
                    "fix_action": "remove_debris"
                })
                report["fixable"].append("remove_debris")
    except Exception as e:
        report["warnings"].append("Could not check disconnected components: " + str(e))

    if not report["issues"]:
        report["warnings"].append("No issues detected. This model looks clean for transfer.")

    return report


def fix_model(filepath, fixes_to_apply, output_format="stl"):
    import trimesh
    import numpy as np

    try:
        loaded = trimesh.load(filepath, force=None)
    except Exception as e:
        return {"success": False, "error": "Failed to load: " + str(e)}

    if isinstance(loaded, trimesh.Scene):
        meshes = [g for g in loaded.geometry.values() if isinstance(g, trimesh.Trimesh)]
        mesh = trimesh.util.concatenate(meshes)
    elif isinstance(loaded, trimesh.Trimesh):
        mesh = loaded
    else:
        return {"success": False, "error": "Unsupported geometry type"}

    applied_fixes = []

    if "scale_to_mm" in fixes_to_apply:
        max_dim = float(np.max(mesh.bounds[1] - mesh.bounds[0]))
        if max_dim > 10000:
            mesh.apply_scale(0.001)
            applied_fixes.append("Scaled down (assumed meters to millimeters)")
        elif max_dim < 0.1:
            mesh.apply_scale(1000.0)
            applied_fixes.append("Scaled up (assumed meters to millimeters)")

    if "remove_degenerate" in fixes_to_apply:
        mask = mesh.nondegenerate_faces
        removed = len(mesh.faces) - mask.sum()
        mesh.update_faces(mask)
        applied_fixes.append("Removed " + str(removed) + " degenerate faces")

    if "remove_duplicates" in fixes_to_apply:
        before = len(mesh.faces)
        sorted_faces = np.sort(mesh.faces, axis=1)
        _, unique_idx = np.unique(sorted_faces, axis=0, return_index=True)
        mask = np.zeros(len(mesh.faces), dtype=bool)
        mask[unique_idx] = True
        mesh.update_faces(mask)
        removed = before - len(mesh.faces)
        if removed > 0:
            applied_fixes.append("Removed " + str(removed) + " duplicate faces")

    if "fix_normals" in fixes_to_apply or "fix_winding" in fixes_to_apply:
        mesh.fix_normals()
        applied_fixes.append("Fixed face normals and winding order")

    if "fill_holes" in fixes_to_apply:
        trimesh.repair.fill_holes(mesh)
        trimesh.repair.fix_normals(mesh)
        trimesh.repair.fix_winding(mesh)
        applied_fixes.append("Filled holes and repaired mesh")

    if "remove_debris" in fixes_to_apply:
        components = mesh.split(only_watertight=False)
        if len(components) > 1:
            components.sort(key=lambda c: len(c.faces), reverse=True)
            significant = [c for c in components if len(c.faces) >= 10]
            if significant:
                mesh = trimesh.util.concatenate(significant)
                removed = len(components) - len(significant)
                applied_fixes.append("Removed " + str(removed) + " tiny debris components")

    if "decimate" in fixes_to_apply:
        target = min(250000, len(mesh.faces))
        try:
            mesh = mesh.simplify_quadric_decimation(target)
            applied_fixes.append("Decimated to " + str(len(mesh.faces)) + " faces")
        except Exception as e:
            applied_fixes.append("Decimation failed: " + str(e))

    basename = os.path.splitext(os.path.basename(filepath))[0]
    ext_map = {"stl": ".stl", "obj": ".obj", "glb": ".glb", "gltf": ".gltf", "ply": ".ply"}
    ext = ext_map.get(output_format.lower(), ".stl")
    output_name = basename + "_fixed" + ext

    import os as _os
    output_dir = '/tmp/fixed' if _os.environ.get('VERCEL') == '1' else _os.path.join(_os.path.dirname(filepath), '..', 'fixed')
    _os.makedirs(output_dir, exist_ok=True)
    output_path = _os.path.join(output_dir, output_name)

    try:
        mesh.export(output_path, file_type=output_format.lower())
    except Exception as e:
        return {"success": False, "error": "Export failed: " + str(e)}

    return {
        "success": True,
        "output_file": output_name,
        "output_path": output_path,
        "applied_fixes": applied_fixes,
        "new_stats": {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "is_watertight": bool(mesh.is_watertight),
        }
    }
