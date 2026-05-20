import sys
import os
import importlib.util
from flask import Flask, jsonify

# Declare app at module level so Vercel's static analysis can find it
app = Flask(__name__)

try:
    _tool_dir = os.