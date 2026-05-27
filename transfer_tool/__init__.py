from flask import Flask, jsonify
import traceback

app = Flask(__name__)

# Step 1: confirm Flask works
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# Step 2: try importing the heavy dependencies and report results
@app.route('/diagnose')
def diagnose():
    results = {}

    for pkg in ['trimesh', 'numpy', 'scipy', 'networkx', 'anthropic']:
        try:
            __import__(pkg)
            results[pkg] = "ok"
        except Exception as e:
            results[pkg] = f"FAILED: {e}"

    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '3d-model-transfer-tool'))
        import importlib.util
        _spec = importlib.util.spec_from_file_location('_tool_app', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '3d-model-transfer-tool', 'app.py'))
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        results['full_app_import'] = "ok"
    except Exception as e:
        results['full_app_import'] = f"FAILED: {traceback.format_exc()}"

    return jsonify(results)
