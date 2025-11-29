import os
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "SysJitter backend is running. Use /run to execute the experiment."

@app.route("/run")
def run_experiment():
    # 1) C++ benchmark run karo
    cpp_result = subprocess.run(
        ["./sysjitter"],
        capture_output=True,
        text=True
    )

    # 2) Graphs generate karne ke liye Python script run karo
    py_result = subprocess.run(
        ["python", "plot_results.py"],
        capture_output=True,
        text=True
    )

    return jsonify({
        "cpp_stdout": cpp_result.stdout,
        "cpp_stderr": cpp_result.stderr,
        "plot_stdout": py_result.stdout,
        "plot_stderr": py_result.stderr,
        "message": "Jitter analysis complete. CSV & PNG graphs generated on server."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
