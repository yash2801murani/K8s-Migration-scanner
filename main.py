# main.py
import sys
from scanner import scan_namespace
from rules import (
    check_service_types,
    check_cloud_service_annotations,
    check_ingress_annotations,
    check_pvc_storage,
    check_hostpath_volumes,
    check_cloud_iam_annotations,
    check_node_selectors,
    check_image_registries,
    check_resource_limits
)

# ----------------------------
# CLI argument for namespace
# ----------------------------
if len(sys.argv) != 2:
    print("Usage: python main.py <namespace>")
    sys.exit(1)

namespace = sys.argv[1]

# ----------------------------
# Scan cluster
# ----------------------------
data = scan_namespace(namespace)

# ----------------------------
# Apply rules
# ----------------------------
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

# ----------------------------
# Print report
# ----------------------------
print("\nKubernetes Migration Readiness Report")
print("="*40)
print(f"Namespace: {namespace}\n")

if not issues:
    print("✔ No migration risks detected")
    print("Readiness Score: 100%")
else:
    for i in issues:
        sev = "❌" if i["severity"] == "error" else "⚠️"
        print(f"{sev} {i['message']}")
    score = max(0, 100 - len(issues)*5)
    print(f"\nReadiness Score: {score}%")
