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
    