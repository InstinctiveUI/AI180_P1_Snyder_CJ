import sys
import os
import importlib.util
from flask import Flask, jsonify
import traceback

app = Flask(__name__)

_tool_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3d-model-transfer-tool")
sys.path.insert(0, os.path.abspath(_tool_dir))

try:
    _spec = importlib.util.spec_from_file_location("_tool_app", os.path.join(_tool_dir, "app.py"))
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    app = _module.app
except Exception as e:
    _tb = traceback.format_exc()

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return jsonify({"startup_error": str(e), "traceback": _tb}), 500
