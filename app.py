from flask import Flask, jsonify, Response
import os, subprocess, base64

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def encode_image(path):
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


@app.route("/")
def index():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>SysJitter – OS Research Demo</title>
        <meta charset="utf-8" />
        <style>
            :root {
                color-scheme: dark;
            }
            * { box-sizing: border-box; }
            body {
                margin: 0;
                padding: 24px;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #020617; /* slate-950 */
                color: #e5e7eb;      /* gray-200 */
            }
            .container {
                max-width: 1080px;
                margin: 0 auto;
            }
            h1 {
                margin: 0;
                font-size: 2.2rem;
                font-weight: 700;
            }
            .subtitle {
                margin-top: 6px;
                color: #9ca3af; /* gray-400 */
                font-size: 0.95rem;
            }
            .btn-row {
                margin-top: 20px;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            button {
                padding: 10px 18px;
                border-radius: 999px;
                border: none;
                cursor: pointer;
                font-size: 0.95rem;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                font-weight: 500;
                transition: transform 0.06s ease, box-shadow 0.06s ease, background 0.15s;
            }
            button span.badge {
                background: rgba(15,23,42,0.8);
                padding: 2px 7px;
                border-radius: 999px;
                font-size: 0.75rem;
            }
            #runBtn {
                background: #2563eb;
                color: white;
                box-shadow: 0 10px 25px rgba(37,99,235,0.35);
            }
            #runBtn:hover { background:#1d4ed8; transform: translateY(-1px); }
            #plotBtn {
                background: #16a34a;
                color: white;
                box-shadow: 0 10px 25px rgba(22,163,74,0.35);
            }
            #plotBtn:hover { background:#15803d; transform: translateY(-1px); }

            #status {
                margin-top: 18px;
                padding: 12px 14px;
                border-radius: 12px;
                background: rgba(15,23,42,0.85);
                border: 1px solid rgba(55,65,81,0.8);
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
                font-size: 0.85rem;
                white-space: pre-wrap;
                min-height: 48px;
            }

            .graphs {
                display: flex;
                gap: 18px;
                flex-wrap: wrap;
                margin-top: 22px;
            }
            .card {
                flex: 1 1 280px;
                background: radial-gradient(circle at top, #111827, #020617 55%);
                border-radius: 18px;
                padding: 14px 14px 18px;
                border: 1px solid rgba(75,85,99,0.9);
                box-shadow: 0 18px 45px rgba(15,23,42,0.9);
            }
            .card h3 {
                margin: 0 0 10px;
                font-size: 1rem;
                letter-spacing: 0.02em;
            }
            img {
                max-width: 100%;
                border-radius: 10px;
                display: block;
                border: 1px solid rgba(31,41,55,0.9);
            }
            footer {
                margin-top: 26px;
                color: #6b7280;
                font-size: 0.8rem;
            }
            code {
                background: rgba(15,23,42,0.9);
                padding: 2px 5px;
                border-radius: 6px;
                border: 1px solid rgba(55,65,81,0.8);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SysJitter – System Jitter Analysis</h1>
            <div class="subtitle">
                Cloud-hosted C++ jitter benchmark with Python visualization.<br/>
                Run the experiment, then generate latency distribution graphs.
            </div>

            <div class="btn-row">
                <button id="runBtn">
                    <span class="badge">1</span>
                    <span>Run Jitter Experiment</span>
                </button>
                <button id="plotBtn">
                    <span class="badge">2</span>
                    <span>Generate &amp; Load Graphs</span>
                </button>
            </div>

            <div id="status">Ready.</div>

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
        </div>

        <script>
        async function runExperiment() {
            const status = document.getElementById("status");
            status.textContent = "Running C++ jitter benchmark on server...";
            try {
                const res = await fetch("/run");
                const data = await res.json();
                status.textContent =
                    "Experiment finished.\\n" +
                    "status: " + data.status + "\\n" +
                    "exit_code: " + data.exit_code + "\\n" +
                    "stdout: " + data.stdout;
            } catch (e) {
                status.textContent = "Error running experiment: " + e;
            }
        }

        async function loadPlots() {
            const status = document.getElementById("status");
            status.textContent += "\\n\\nGenerating plots on server...";
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
