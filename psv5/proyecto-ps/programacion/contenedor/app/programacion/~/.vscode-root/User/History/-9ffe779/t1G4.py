from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code_path = data['code_path']
    casos_path = data['casos_path']

    comando = f"python3 /code/programacion/scripts/scripts.py {code_path} {casos_path}"
    result = subprocess.run(comando, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 400

    try:
        output = json.loads(result.stdout)
        return jsonify(output), 200
    except json.JSONDecodeError as e:
        return jsonify({"error": str(e), "stdout": result.stdout}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

