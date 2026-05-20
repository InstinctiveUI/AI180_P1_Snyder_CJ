import sys
import os
import importlib.util
import traceback
from flask import Flask, jsonify

_tool_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '3d-model-transfer-tool')
sys.path.insert(0, os.path.abspath(_tool_dir))

try:
    _spec = importlib.util.spec_from_file_location('_tool_app', os.path.join(_tool_dir, 'app.py'))
    _module = importlib.util.module_from_sp