from flask import Flask, request, render_template, jsonify
import json
from model import probe_model
import os

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    data = json.load(file)
    if "data" not in data:
        return "Invalid JSON format", 400

    result = probe_model(data["data"])
    return render_template('results.html', result=json.dumps(result, indent=4))

@app.route('/api/result', methods=['POST'])
def api_result():
    data = request.get_json()
    if "data" not in data:
        return jsonify({"error": "Invalid JSON format"}), 400

    result = probe_model(data["data"])
    return jsonify(result)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
