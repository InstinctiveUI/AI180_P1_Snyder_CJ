"""
3D Model Transfer Assistant — Flask Web App
Upload a 3D model, select source/target applications, get analysis + auto-fix.
"""
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from analyzer import analyze_model, fix_model
from knowledge_base import (
    get_recommended_format, get_relevant_issues, APP_CATEGORIES,
    FORMAT_INFO, KEY_CAUSES, RECOMMENDED_TOOLS, TRANSFER_ISSUES, PRINT_ISSUES
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max upload

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
FIXED_DIR = os.path.join(os.path.dirname(__file__), 'fixed')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FIXED_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'stl', 'obj', 'fbx', 'glb', 'gltf', 'ply', 'dae', '3ds'}

LOG_FILE = os.path.join(os.path.dirname(__file__), 'activity_log.md')


EXPLANATIONS = {
    'Analyze': (
        "The program loaded the model file and inspected its geometry. "
        "It checked vertex and face counts, tested whether the mesh is watertight (no holes), "
        "looked for inverted normals, degenerate faces, duplicate faces, scale mismatches, "
        "and disconnected debris. Any issues found are flagged with severity levels and marked "
        "as auto-fixable where possible."
    ),
    'Auto-Fix': (
        "The program applied targeted repairs to the model based on what the analysis detected. "
        "Each fix addresses a specific transfer problem: scaling corrects unit mismatches between apps, "
        "hole-filling makes the mesh watertight for printing, normal fixes stop faces from appearing "
        "inside-out, and debris removal cleans up leftover boolean artifacts. "
        "The repaired model was exported to the chosen format."
    ),
    'Auto-Fix FAILED': (
        "The program attempted to repair the model but encountered an error during the fix or export process. "
        "The original file was not modified. Check the details column for the specific error."
    ),
    'Format Recommendation': (
        "The program looked up the source and target applications selected by the user and matched them "
        "against the knowledge base of known transfer issues. It ranked the best export formats for that "
        "specific app-to-app workflow and listed any known problems (broken materials, scale issues, "
        "animation loss, etc.) the user should expect."
    ),
    'Download': (
        "The user downloaded the repaired model file that was produced by the Auto-Fix step. "
        "This is the cleaned, export-ready version of their original upload."
    ),
}


def write_log(action, filename=None, details=None):
    """Append an entry to the markdown activity log."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write('# 3D Model Transfer Assistant — Activity Log\n\n')
            f.write('## Why the Program Uses the Fixes It Does\n\n')
            f.write('See the Fix Explanations section below the session log.\n\n')
            f.write('---\n\n')
            f.write('## Session Log\n\n')
            f.write('| Timestamp | Action | File | Details | What the Program Did |\n')
            f.write('|-----------|--------|------|---------|----------------------|\n')

    file_col = filename or '—'
    detail_col = details or '—'
    explanation = EXPLANATIONS.get(action, 'The program completed the requested operation.')
    with open(LOG_FILE, 'a') as f:
        f.write(f'| {timestamp} | {action} | {file_col} | {detail_col} | {explanation} |\n')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


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
    write_log('Format Recommendation', details=f'{source} → {target} ({len(formats)} formats suggested)')
    return jsonify({"formats": formats, "issues": issues})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'model' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['model']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file. Supported: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)

    report = analyze_model(filepath)
    issue_count = len(report.get('issues', []))
    fix_count = len(report.get('fixable', []))
    stats = report.get('stats', {})
    verts = stats.get('vertices', 0)
    faces = stats.get('faces', 0)
    write_log('Analyze', filename=file.filename,
              details=f'{verts:,} verts, {faces:,} faces, {issue_count} issues found, {fix_count} auto-fixable')
    return jsonify(report)


@app.route('/api/fix', methods=['POST'])
def fix():
    data = request.json
    filename = data.get('filename', '')
    fixes = data.get('fixes', [])
    output_format = data.get('output_format', 'stl')

    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found. Please upload again."}), 404

    result = fix_model(filepath, fixes, output_format)
    if result.get('success'):
        applied = ', '.join(result.get('applied_fixes', []))
        write_log('Auto-Fix', filename=filename,
                  details=f'Output: {result.get("output_file")} | Fixes: {applied}')
    else:
        write_log('Auto-Fix FAILED', filename=filename, details=result.get('error', 'Unknown error'))
    return jsonify(result)


@app.route('/api/download/<filename>')
def download_fixed(filename):
    write_log('Download', filename=filename, details='User downloaded fixed model')
    return send_from_directory(FIXED_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    print("\n  3D Model Transfer Assistant")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
