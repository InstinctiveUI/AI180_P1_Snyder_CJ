"""
3D Model Transfer Assistant - Flask Web App
"""
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

_IS_VERCEL = os.environ.get('VERCEL') == '1'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 if _IS_VERCEL else 200 * 1024 * 1024
UPLOAD_DIR = '/tmp/uploads' if _IS_VERCEL else os.path.join(os.path.dirname(__file__), 'uploads')
FIXED_DIR  = '/tmp/fixed'   if _IS_VERCEL else os.path.join(os.path.dirname(__file__), 'fixed')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FIXED_DIR, exist_ok=True)

try:
    from analyzer import analyze_model, fix_model
    from knowledge_base import (
        get_recommended_format, get_relevant_issues, APP_CATEGORIES,
        FORMAT_INFO, KEY_CAUSES, RECOMMENDED_TOOLS, TRANSFER_ISSUES, PRINT_ISSUES
    )
    from claude_ai import get_analysis_summary, get_ai_format_advice, chat as claude_chat
    _import_error = None
except Exception as _ie:
    _import_error = str(_ie)
    def analyze_model(*a, **k): return {"error": "Import failed: " + _import_error}
    def fix_model(*a, **k): return {"error": "Import failed: " + _import_error}
    def get_recommended_format(*a, **k): return {}
    def get_relevant_issues(*a, **k): return []
    def get_analysis_summary(*a, **k): return "Import error: " + _import_error
    def get_ai_format_advice(*a, **k): return "Import error: " + _import_error
    def claude_chat(*a, **k): return "Import error: " + _import_error
    APP_CATEGORIES = {}; FORMAT_INFO = {}; KEY_CAUSES = {}
    RECOMMENDED_TOOLS = {}; TRANSFER_ISSUES = []; PRINT_ISSUES = []

ALLOWED_EXTENSIONS = {'stl', 'obj', 'fbx', 'glb', 'gltf', 'ply', 'dae', '3ds'}
LOG_FILE = '/tmp/activity_log.md' if _IS_VERCEL else os.path.join(os.path.dirname(__file__), 'activity_log.md')


def write_log(action, filename=None, details=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write('# Activity Log\n\n| Timestamp | Action | File | Details |\n|---|---|---|---|\n')
    with open(LOG_FILE, 'a') as f:
        f.write('| ' + timestamp + ' | ' + action + ' | ' + (filename or '-') + ' | ' + (details or '-') + ' |\n')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pipeline')
def pipeline():
    return render_template('pipeline.html')


@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "vercel": _IS_VERCEL,
        "import_error": _import_error,
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "python": sys.version,
    })


@app.route('/api/apps')
def get_apps():
    return jsonify(APP_CATEGORIES)


@app.route('/api/formats')
def get_formats():
    return jsonify(FORMAT_INFO)


@app.route('/api/knowledge')
def get_knowledge():
    return jsonify({"transfer_issues": TRANSFER_ISSUES, "print_issues": PRINT_ISSUES,
                    "key_causes": KEY_CAUSES, "recommended_tools": RECOMMENDED_TOOLS})


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    source = data.get('source', '')
    target = data.get('target', '')
    formats = get_recommended_format(source, target)
    issues = get_relevant_issues(source, target)
    write_log('Recommend', details=source + ' to ' + target)
    return jsonify({"formats": formats, "issues": issues})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'model' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files['model']
    if not f.filename or not allowed_file(f.filename):
        return jsonify({"error": "Invalid file type"}), 400
    safe = secure_filename(f.filename)
    if not safe:
        return jsonify({"error": "Invalid filename"}), 400
    path = os.path.join(UPLOAD_DIR, safe)
    f.save(path)
    report = analyze_model(path)
    write_log('Analyze', filename=safe, details=str(len(report.get('issues', []))) + ' issues')
    return jsonify(report)


@app.route('/api/fix', methods=['POST'])
def fix():
    data = request.json or {}
    filename = secure_filename(data.get('filename', ''))
    if not filename:
        return jsonify({"error": "Invalid filename"}), 400
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found. Please upload again."}), 404
    result = fix_model(path, data.get('fixes', []), data.get('output_format', 'stl'))
    write_log('Fix', filename=filename, details='success' if result.get('success') else result.get('error', ''))
    return jsonify(result)


@app.route('/api/download/<filename>')
def download_fixed(filename):
    safe = secure_filename(filename)
    if not safe:
        return jsonify({"error": "Invalid filename"}), 400
    write_log('Download', filename=safe)
    return send_from_directory(FIXED_DIR, safe, as_attachment=True)


@app.route('/api/ai/summary', methods=['POST'])
def ai_summary():
    data = request.json or {}
    result = get_analysis_summary(data.get('report', {}), data.get('source_app', ''), data.get('target_app', ''))
    return jsonify(result)


@app.route('/api/ai/format', methods=['POST'])
def ai_format():
    data = request.json or {}
    source = data.get('source_app', '')
    target = data.get('target_app', '')
    if not source or not target:
        return jsonify({'error': 'source_app and target_app required'}), 400
    return jsonify(get_ai_format_advice(source, target, data.get('model_stats')))


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    return jsonify(claude_chat(data.get('messages', []), data.get('context')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
