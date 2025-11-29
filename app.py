import os
import subprocess
import base64
from flask import Flask, jsonify, Response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def encode_image(path):
    """Return base64 string of image if exists."""
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


@app.route("/")
def index():
    # Simple HTML + JS UI
    html = """
    <!doctype html>
    <html>
    <head>
        <title>SysJitter – OS Research Demo</title>
        <meta charset="utf-8" />
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 900px; margin: auto; }
            h1 { margin-bottom: 0; }
            .subtitle { color: #555; margin-top: 4px; }
            button { padding: 10px 18px; margin: 10px 0; border-radius: 6px;
                     border: none; cursor: pointer; font-size: 15px; }
            #runBtn { background:#2563eb; color:white; }
            #plotBtn { background:#16a34a; color:white; }
            #status { margin-top: 10px; font-family: monospace; white-space: pre-wrap; }
            .graphs { display:flex; gap:20px; flex-wrap:wrap; margin-top:20px; }
            .card { border:1px solid #ddd; border-radius:8px; padding:10px; flex:1 1 260px; }
            img { max-width:100%; border-radius:6px; }
            footer { margin-top:30px; color:#777; font-size:13px; }
        </style>
    </head>
    <body>
        <h1>SysJitter – System Jitter Analysis</h1>
        <div class="subtitle">
            C++ jitter benchmark + Python plotting, deployed on Render.
        </div>

        <button id="runBtn">1️⃣ Run Jitter Experiment</button>
        <button id="plotBtn">2️⃣ Generate & Load Graphs</button>

        <div id="status"></div>

        <div class="graphs">
            <div class="card">
                <h3>Idle System Jitter</h3>
                <img id="idleImg" alt="Idle jitter graph will appear here" />
            </div>
            <div class="card">
                <h3>Loaded System Jitter</h3>
                <img id="loadImg" alt="Loaded jitter graph will appear here" />
            </div>
        </div>

        <footer>
            API endpoints: <code>/run</code> (C++ benchmark), <code>/plot</code> (Python graphs).
        </footer>

        <script>
        async function runExperiment() {
            const status = document.getElementById("status");
            status.textContent = "Running C++ jitter benchmark...";
            try {
                const res = await fetch("/run");
                const data = await res.json();
                status.textContent = "Experiment finished.\\n" +
                    "status: " + data.status + "\\n" +
                    "exit_code: " + data.exit_code + "\\n" +
                    "stdout: " + data.stdout;
            } catch (e) {
                status.textContent = "Error running experiment: " + e;
            }
        }

        async function loadPlots() {
            const status = document.getElementById("status");
            status.textContent += "\\n\\nGenerating plots...";
            try {
                const res = await fetch("/plot");
                const data = await res.json();

                if (data.idle_img) {
                    document.getElementById("idleImg").src =
                        "data:image/png;base64," + data.idle_img;
                }
                if (data.load_img) {
                    document.getElementById("loadImg").src =
                        "data:image/png;base64," + data.load_img;
                }

                status.textContent += "\\nPlot script: " + data.plot_status;
            } catch (e) {
                status.textContent += "\\nError generating plots: " + e;
            }
        }

        document.getElementById("runBtn").onclick = runExperiment;
        document.getElementById("plotBtn").onclick = loadPlots;
        </script>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@app.route("/run")
def run_experiment():
    binary_path = os.path.join(BASE_DIR, "sysjitter")

    try:
        cpp_result = subprocess.run(
            [binary_path],
            capture_output=True,
            text=True
        )
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "stage": "running sysjitter",
            "error": "sysjitter binary not found. Check build command.",
            "details": str(e)
        }), 500
    except Exception as e:
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


@app.route("/plot")
def plot_graphs():
    # Run the existing Python script that generates PNGs
    result = subprocess.run(
        ["python", os.path.join(BASE_DIR, "plot_results.py")],
        capture_output=True,
        text=True
    )

    idle_b64 = encode_image("graph_idle.png")
    load_b64 = encode_image("graph_load.png")

    return jsonify({
        "plot_status": "ok" if result.returncode == 0 else "error",
        "plot_stdout": result.stdout,
        "plot_stderr": result.stderr,
        "idle_img": idle_b64,
        "load_img": load_b64
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
