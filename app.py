from flask import Flask, render_template, request, jsonify
from scanner import scan_namespace
from rules import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    namespace = request.form.get("namespace")
    if not namespace:
        return jsonify({"error": "Namespace required"}), 400

    data = scan_namespace(namespace)
    issues = []
    issues += check_service_types(data["services"])
    issues += check_cloud_service_annotations(data["services"])
    issues += check_ingress_annotations(data["ingresses"])
    issues += check_pvc_storage(data["pvcs"])
    issues += check_hostpath_volumes(data["pods"])
    issues += check_cloud_iam_annotations(data["serviceaccounts"])
    issues += check_node_selectors(data["pods"])
    issues += check_image_registries(data["pods"])
    issues += check_resource_limits(data["pods"])

    score = max(0, 100 - len(issues)*5)
    return jsonify({"issues": issues, "score": score, "namespace": namespace})

if __name__ == "__main__":
    app.run(debug=True)
