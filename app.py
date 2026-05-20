import sys
import os

# Pull in all modules from the tool subdirectory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '3d-model-transfer-tool'))

import app as _tool
app = _tool.app
