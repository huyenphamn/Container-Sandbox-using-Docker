from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_scripts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # List both uploaded and pre-written scripts
    uploaded = os.listdir(UPLOAD_FOLDER)
    predefined = os.listdir('tests')
    return render_template('index.html', uploaded=uploaded, predefined=predefined)

@app.route('/run', methods=['POST'])
def run_script():
    script_source = request.form['source']
    
    if script_source == 'upload':
        file = request.files['script']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
    else:
        filename = request.form['selected_script']
        filepath = os.path.join('tests', filename)
    
    try:
        result = subprocess.run(['bash', 'sandbox.sh', filepath],
                                capture_output=True, text=True, timeout=20)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Script execution timed out.'}), 504

if __name__ == '__main__':
    app.run(debug=True)