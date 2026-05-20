import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '3d-model-transfer-tool'))

try:
    import app as _tool
    app = _tool.app
except Exception as e:
    # If star