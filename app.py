from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)

# Directory to store uploaded scripts
UPLOAD_FOLDER = 'uploaded_scripts'

# Ensure the upload directory exists; if not, create it
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # List both uploaded and pre-written test files
    uploaded = os.listdir(UPLOAD_FOLDER)
    predefined = os.listdir('tests')
    return render_template('index.html', uploaded=uploaded, predefined=predefined)

# Route to handle running the file in the sandbox
@app.route('/run', methods=['POST'])
def run_script():
     # Get the source of the test (either uploaded or predefined)
    script_source = request.form['source']
    
     # Handle the case where the test is uploaded by the user
    if script_source == 'upload':
        file = request.files['script']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

    # Handle the case where the user selects a predefined test
    else:
        filename = request.form['selected_script']
        filepath = os.path.join('tests', filename)
    
    # Run the script in the sandbox using subprocess
    try:
        result = subprocess.run(['bash', 'sandbox.sh', filepath], capture_output=True, text=True, timeout=15)
        # Return the captured output as a JSON response
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    # If the script execution exceeds the timeout, return an error
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Script execution timed out.'}), 504

if __name__ == '__main__':
    app.run(debug=True)