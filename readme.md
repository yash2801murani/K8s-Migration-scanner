README.md (Simplified)
# Kubernetes Migration Readiness Scanner

A simple **Kubernetes Migration Readiness Scanner** built with Python and Flask.  
Scan your namespaces to check for migration risks when moving workloads between clusters or clouds.  

---

## Features

- Scan **services, deployments, PVCs, ingress, service accounts, configmaps, secrets**.  
- Detect **migration risks** such as:
  - LoadBalancer services
  - hostPath volumes
  - cloud-specific storage
  - deprecated ingress annotations
  - missing resource limits
- Web UI with **loading spinner** and **bold, clean output**.  
- Calculate **readiness score** per namespace.  

---

## Project Structure



k8s-migration-readiness/
├── main.py # Flask web app
├── scanner.py # CLI / scanning logic
├── rules.py # Migration rules
├── templates/
│ └── index.html # Web UI template
├── static/
│ ├── style.css
│ └── script.js # Web UI JS
├── requirements.txt # Python dependencies
├── sample.yaml # Sample namespace project for testing


---

## Installation (Local)

1. Clone the repo:

```bash
git clone https://github.com/yash2801murani/K8s-Migration-scanner.git
cd K8s-Migration-scanner


Create a Python virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the Flask app:

export FLASK_APP=main.py
flask run


Open your browser at http://localhost:5000

Make sure you have kubeconfig configured to access your cluster.

Usage

Enter the namespace name in the input field.

Click Scan → a loading spinner appears.

After 4–5 seconds, results display in bold black text with ✅✔️, ⚠️ warnings, ❌ errors.

Check readiness score to evaluate migration risks.

Notes

Requires read access to cluster objects (pods, deployments, services, PVCs, configmaps, secrets, serviceaccounts, ingress).

Can be run locally with kubeconfig.

Developed By

Yash Murani
You can optionally add a watermark in the UI: “Developed by Yash”.

License

MIT License