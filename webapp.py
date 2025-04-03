from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from controller import Controller
from config import load_config
from pyvis.network import Network
import json
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Global variables to store scan results
result_graph = None
result_json = None


# ----------- Main Routes -----------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    global result_graph, result_json
    targets = request.form.get("targets")
    darkweb = request.form.get("darkweb") == "on"
    permutations = request.form.get("permutations") == "on"

    if not targets:
        flash("Please enter at least one target.", "danger")
        return redirect(url_for("index"))

    target_list = [line.strip() for line in targets.splitlines() if line.strip()]

    # Build a simple args-like object for configuration.
    class Args:
        def __init__(self, darkweb, permutations):
            self.darkweb = darkweb
            self.permutations = permutations
            self.output = "results.json"

    args = Args(darkweb, permutations)
    config = load_config(args)

    flash("Scan started. This may take a few moments...", "info")
    controller = Controller(config)
    result_graph = controller.run(target_list)
    result_json = result_graph.get_data()
    flash("Scan complete!", "success")
    return redirect(url_for("results"))


@app.route("/results", methods=["GET"])
def results():
    global result_json
    if not result_json:
        flash("No scan results available. Please run a scan first.", "warning")
        return redirect(url_for("index"))
    return render_template("results.html", data=result_json)


@app.route("/graph", methods=["GET"])
def graph():
    global result_graph
    if not result_graph:
        flash("No graph available. Please run a scan first.", "warning")
        return redirect(url_for("index"))
    net = Network(height="750px", width="100%", notebook=False, directed=False)
    net.from_nx(result_graph.graph)
    net.repulsion(
        node_distance=200, central_gravity=0.33, spring_length=110, spring_strength=0.10
    )
    return net.generate_html()


@app.route("/download", methods=["GET"])
def download():
    global result_json
    if not result_json:
        flash("No results available. Please run a scan first.", "warning")
        return redirect(url_for("index"))
    response = app.response_class(
        response=json.dumps(result_json, indent=4),
        mimetype="application/json",
    )
    response.headers["Content-Disposition"] = "attachment; filename=results.json"
    return response


# ----------- Settings Routes -----------
@app.route("/settings", methods=["GET", "POST"])
def settings():
    # List all JSON config files in the configs folder
    configs_dir = os.path.join(os.path.dirname(__file__), "configs")
    config_files = [f for f in os.listdir(configs_dir) if f.endswith(".json")]
    selected_config = request.args.get("config")
    content = ""
    if selected_config and selected_config in config_files:
        with open(os.path.join(configs_dir, selected_config), "r", encoding="utf-8") as f:
            content = f.read()
    if request.method == "POST":
        selected_config = request.form.get("selected_config")
        new_content = request.form.get("config_content")
        action = request.form.get("action")
        if action == "save" and selected_config in config_files:
            try:
                # Validate JSON before saving
                if new_content is None:
                    raise ValueError("Config content cannot be empty")
                json_data = json.loads(new_content)
                with open(os.path.join(configs_dir, selected_config), "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4)
                flash(f"{selected_config} updated successfully.", "success")
            except Exception as e:
                flash(f"Error updating {selected_config}: {e}", "danger")
        else:
            flash("Update cancelled.", "info")
        return redirect(url_for("settings", config=selected_config))
    return render_template(
        "settings.html",
        config_files=config_files,
        selected_config=selected_config,
        content=content,
    )


# ----------- Logs Routes -----------
@app.route("/logs", methods=["GET"])
def logs():
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    log_files = [
        f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))
    ]
    return render_template("logs.html", log_files=log_files)


@app.route("/logs/<log_filename>", methods=["GET"])
def view_log(log_filename):
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    log_path = os.path.join(logs_dir, log_filename)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
        return render_template(
            "view_log.html", log_filename=log_filename, log_content=log_content
        )
    else:
        flash("Log file not found.", "danger")
        return redirect(url_for("logs"))


# ----------- API Endpoint (placeholder) -----------
@app.route("/api/scan", methods=["POST"])
def api_scan():
    # This endpoint can be expanded for asynchronous scanning in the future.
    return jsonify({"status": "Not yet implemented"}), 501


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
