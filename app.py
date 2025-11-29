import os
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return "SysJitter backend is running. Use /run to execute the experiment."

@app.route("/run")
def run_experiment():
    binary_path = os.path.join(BASE_DIR, "sysjitter")

    # 1) C++ binary run karne ki try
    try:
        cpp_result = subprocess.run(
            [binary_path],
            capture_output=True,
            text=True
        )
    except FileNotFoundError as e:
        # binary hi nahi mili
        return jsonify({
            "status": "error",
            "stage": "running sysjitter",
            "error": "sysjitter binary not found. Check build command.",
            "details": str(e)
        }), 500
    except Exception as e:
        # koi aur unexpected error
        return jsonify({
            "status": "error",
            "stage": "running sysjitter",
            "error": str(e)
        }), 500

    return jsonify({
        "status": "ok",
        "exit_code": cpp_result.returncode,
        "stdout": cpp_result.stdout,
        "stderr": cpp_result.stderr
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
