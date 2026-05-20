import sys
import os

# Add the tool directory to the path so all imports (analyzer, knowledge_base, claude_ai) resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '3d-model-transfer-tool'))

from app import app
