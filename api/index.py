import sys
import os

# Add the tool directory so analyzer, knowledge_base, claude_ai all resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '3d-model-transfer-tool'))

import app as _module
app = _module.app
