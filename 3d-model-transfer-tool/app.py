"""
3D Model Transfer Assistant - Flask Web App
"""
import sys
import os
# Ensure local modules (analyzer, knowledge_base, claude_ai) are importable
# when running as a Vercel serverless function, which does not add the
# function's own directory to sys.path automatically.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# app must be defined before local imports so Vercel builder can always find it
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

EXPLANATIONS = {
    'Analyze': 'The program loaded the model and inspected its geometry for issues.',
    'Auto-Fix': 'The program applied targeted repairs and exported the cleaned model.',
    'Auto-Fix FAILED': 'The program attempted repair but encountered an error.',
    'Format Recommendation': 'The program matched source/target apps against known transfer issues.',
    'Download': 'The user downloaded the repaired model file.',
}


def write_log(action, filename=None, details=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('# 3D Model Transfer Assistant - Activity Log\n\n')
            f.write('| Timestamp | Action | File | Details | What the Program Did |\n')
            f.write('|-----------|--------|------|---------|----------------------|\n')
    file_col = filename or '-'
    detail_col = details or '-'
    explanation = EXPLANATIONS.get(action, 'Operation completed.')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'| {timestamp} | {action} | {file_col} | {detail_col} | {explanation} |\n')


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
    import sys
    return jsonify({
        "status": "ok",
        "vercel": _IS_VERCEL,
        "import_error": _import_error,
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "upload_dir": UPLOAD_DIR,
        "fixed_dir": FIXED_DIR,
        "python": sys.version,
    })


@app.route('/api/apps', methods=['GET'])
def get_apps():
    return jsonify(APP_CATEGORIES)


@app.route('/api/formats', methods=['GET'])
def get_formats():
    return jsonify(FORMAT_INFO)


@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    return jsonify({
        "transfer_issues": TRANSFER_ISSUES,
        "print_issues": PRINT_ISSUES,
        "key_causes": KEY_CAUSES,
        "recommended_tools": RECOMMENDED_TOOLS,
    })


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    source = data.get('source', '')
    target = data.get('target', '')
    formats = get_recommended_format(source, target)
    issues = get_relevant_issues(source, target)
    write_log('Format Recommendation', details=source + ' to ' + target)
    return jsonify({"formats": formats, "issues": issues})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'model' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['model']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file. Supported: " + ', '.join(ALLOWED_EXTENSIONS)}), 400
    safe_name = secure_filename(file.filename)
    if not safe_name:
        return jsonify({"error": "Invalid filename."}), 400
    filepath = os.path.join(UPLOAD_DIR, safe_name)
    file.save(filepath)
    report = analyze_model(filepath)
    issue_count = len(report.get('issues', []))
    fix_count = len(report.get('fixable', []))
    stats = report.get('stats', {})
    write_log('Analyze', filename=file.filename,
              details=str(stats.get('vertices', 0)) + ' verts, ' + str(issue_count) + ' issues')
    return jsonify(report)


@app.route('/api/fix', methods=['POST'])
def fix():
    data = request.json
    filename = secure_filename(data.get('filename', ''))
    if not filename:
        return jsonify({"error": "Invalid filename."}), 400
    fixes = data.get('fixes', [])
    output_format = data.get('output_format', 'stl')
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found. Please upload again."}), 404
    result = fix_model(filepath, fixes, output_format)
    if result.get('success'):
        write_log('Auto-Fix', filename=filename, details='Output: ' + str(result.get('output_file')))
    else:
        write_log('Auto-Fix FAILED', filename=filename, details=result.get('error', 'Unknown error'))
    return jsonify(result)


@app.route('/api/download/<filename>')
def download_fixed(filename):
    safe_name = secure_filename(filename)
    if not safe_name:
        return jsonify({"error": "Invalid filename."}), 400
    write_log('Download', filename=safe_name, details='User downloaded fixed model')
    return send_from_directory(FIXED_DIR, safe_name, as_attachment=True)


@app.route('/api/ai/summary', methods=['POST'])
def ai_summary():
    data = request.json or {}
    report = data.get('report', {})
    source = data.get('source_app', '')
    target = data.get('target_app', '')
    result = get_analysis_summary(report, source, target)
    return jsonify(result)


@app.route('/api/ai/format', methods=['POST'])
def ai_format():
    data = request.json or {}
    source = data.get('source_app', '')
    target = data.get('target_app', '')
    stats = data.get('model_stats')
    if not source or not target:
        return jsonify({'error': 'source_app and target_app are required'}), 400
    result = get_ai_format_advice(source, target, stats)
    return jsonify(result)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    messages = data.get('messages', [])
    context = data.get('context', {})
    result = claude_ai.chat(messages, context)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
