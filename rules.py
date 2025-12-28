# # rules.py

# # ----------------------------
# # SERVICE & NETWORKING RULES
# # ----------------------------
# def check_service_types(services):
#     issues = []
#     for svc in services:
#         svc_type = svc.spec.type
#         name = svc.metadata.name

#         if svc_type == "LoadBalancer":
#             issues.append({
#                 "severity": "warning",
#                 "category": "network",
#                 "message": f"Service '{name}' uses LoadBalancer"
#             })
#         elif svc_type == "NodePort":
#             issues.append({
#                 "severity": "info",
#                 "category": "network",
#                 "message": f"Service '{name}' uses NodePort"
#             })
#     return issues

# def check_cloud_service_annotations(services):
#     issues = []
#     for svc in services:
#         annotations = svc.metadata.annotations or {}
#         for key in annotations:
#             if any(x in key.lower() for x in ["aws", "azure", "gcp"]):
#                 issues.append({
#                     "severity": "error",
#                     "category": "network",
#                     "message": f"Service '{svc.metadata.name}' has cloud-specific annotation '{key}'"
#                 })
#     return issues

# # ----------------------------
# # INGRESS RULES
# # ----------------------------
# def check_ingress_annotations(ingresses):
#     issues = []
#     for ing in ingresses:
#         annotations = ing.metadata.annotations or {}
#         for key in annotations:
#             if any(x in key.lower() for x in ["alb", "aws", "azure", "gce"]):
#                 issues.append({
#                     "severity": "error",
#                     "category": "ingress",
#                     "message": f"Ingress '{ing.metadata.name}' uses cloud-specific ingress '{key}'"
#                 })
#     return issues

# # ----------------------------
# # STORAGE RULES
# # ----------------------------
# def check_pvc_storage(pvcs):
#     issues = []
#     for pvc in pvcs:
#         sc = pvc.spec.storage_class_name or "default"
#         name = pvc.metadata.name
#         if any(x in sc.lower() for x in ["aws", "azure", "gcp", "ebs", "disk"]):
#             issues.append({
#                 "severity": "error",
#                 "category": "storage",
#                 "message": f"PVC '{name}' uses cloud-specific StorageClass '{sc}'"
#             })
#     return issues

# def check_hostpath_volumes(pods):
#     issues = []
#     for pod in pods:
#         for vol in pod.spec.volumes or []:
#             if vol.host_path:
#                 issues.append({
#                     "severity": "error",
#                     "category": "storage",
#                     "message": f"Pod '{pod.metadata.name}' uses hostPath volume"
#                 })
#     return issues

# # ----------------------------
# # SECURITY RULES
# # ----------------------------
# def check_cloud_iam_annotations(serviceaccounts):
#     issues = []
#     for sa in serviceaccounts:
#         annotations = sa.metadata.annotations or {}
#         for key in annotations:
#             if any(x in key.lower() for x in ["eks.amazonaws.com", "azure.workload.identity"]):
#                 issues.append({
#                     "severity": "error",
#                     "category": "security",
#                     "message": f"ServiceAccount '{sa.metadata.name}' uses cloud IAM annotation '{key}'"
#                 })
#     return issues

# # ----------------------------
# # SCHEDULING & IMAGE RULES
# # ----------------------------
# def check_node_selectors(pods):
#     issues = []
#     for pod in pods:
#         selectors = pod.spec.node_selector or {}
#         for key in selectors:
#             if any(x in key.lower() for x in ["aws", "azure", "gcp"]):
#                 issues.append({
#                     "severity": "error",
#                     "category": "scheduling",
#                     "message": f"Pod '{pod.metadata.name}' uses cloud-specific nodeSelector '{key}'"
#                 })
#     return issues

# def check_image_registries(pods):
#     issues = []
#     for pod in pods:
#         for c in pod.spec.containers:
#             image = c.image
#             if any(x in image for x in ["amazonaws.com", "azurecr.io", "gcr.io"]):
#                 issues.append({
#                     "severity": "warning",
#                     "category": "image",
#                     "message": f"Container '{c.name}' uses cloud registry '{image}'"
#                 })
#     return issues

# # ----------------------------
# # RESOURCE LIMITS
# # ----------------------------
# def check_resource_limits(pods):
#     issues = []
#     for pod in pods:
#         for c in pod.spec.containers:
#             if not c.resources or not c.resources.limits:
#                 issues.append({
#                     "severity": "warning",
#                     "category": "resources",
#                     "message": f"Container '{c.name}' in pod '{pod.metadata.name}' has no resource limits"
#                 })
#     return issues



# rules.py
# Kubernetes Migration Readiness Scanner Rules

# ----------------------------
# SERVICE & NETWORKING RULES
# ----------------------------
def check_service_types(services):
    issues = []
    for svc in services:
        svc_type = svc.spec.type
        name = svc.metadata.name

        if svc_type == "LoadBalancer":
            issues.append({
                "severity": "warning",
                "category": "network",
                "message": f"Service '{name}' uses LoadBalancer"
            })
        elif svc_type == "NodePort":
            issues.append({
                "severity": "info",
                "category": "network",
                "message": f"Service '{name}' uses NodePort"
            })
    return issues

def check_cloud_service_annotations(services):
    issues = []
    for svc in services:
        annotations = svc.metadata.annotations or {}
        for key in annotations:
            if any(x in key.lower() for x in ["aws", "azure", "gcp"]):
                issues.append({
                    "severity": "error",
                    "category": "network",
                    "message": f"Service '{svc.metadata.name}' has cloud-specific annotation '{key}'"
                })
    return issues

# ----------------------------
# INGRESS RULES
# ----------------------------
def check_ingress_annotations(ingresses):
    issues = []
    for ing in ingresses:
        annotations = ing.metadata.annotations or {}
        for key in annotations:
            if any(x in key.lower() for x in ["alb", "aws", "azure", "gce"]):
                issues.append({
                    "severity": "error",
                    "category": "ingress",
                    "message": f"Ingress '{ing.metadata.name}' uses cloud-specific ingress '{key}'"
                })
    return issues

# ----------------------------
# STORAGE RULES
# ----------------------------
def check_pvc_storage(pvcs):
    issues = []
    for pvc in pvcs:
        sc = pvc.spec.storage_class_name or "default"
        name = pvc.metadata.name
        if any(x in sc.lower() for x in ["aws", "azure", "gcp", "ebs", "disk"]):
            issues.append({
                "severity": "error",
                "category": "storage",
                "message": f"PVC '{name}' uses cloud-specific StorageClass '{sc}'"
            })
        if pvc.spec.access_modes:
            for mode in pvc.spec.access_modes:
                if mode == "ReadWriteMany":
                    issues.append({
                        "severity": "warning",
                        "category": "storage",
                        "message": f"PVC '{name}' uses ReadWriteMany — may not migrate easily"
                    })
    return issues

def check_hostpath_volumes(pods):
    issues = []
    for pod in pods:
        for vol in pod.spec.volumes or []:
            if vol.host_path:
                issues.append({
                    "severity": "error",
                    "category": "storage",
                    "message": f"Pod '{pod.metadata.name}' uses hostPath volume"
                })
    return issues

# ----------------------------
# DEPLOYMENT / POD RULES
# ----------------------------
def check_init_containers(pods):
    issues = []
    for pod in pods:
        for c in pod.spec.init_containers or []:
            issues.append({
                "severity": "warning",
                "category": "deployment",
                "message": f"Pod '{pod.metadata.name}' has initContainer '{c.name}' — check for cloud dependencies"
            })
    return issues

def check_node_selectors(pods):
    issues = []
    for pod in pods:
        selectors = pod.spec.node_selector or {}
        for key in selectors:
            if any(x in key.lower() for x in ["aws", "azure", "gcp"]):
                issues.append({
                    "severity": "error",
                    "category": "scheduling",
                    "message": f"Pod '{pod.metadata.name}' uses cloud-specific nodeSelector '{key}'"
                })
        for tol in pod.spec.tolerations or []:
            issues.append({
                "severity": "warning",
                "category": "scheduling",
                "message": f"Pod '{pod.metadata.name}' has tolerations — check for cloud-specific nodes"
            })
    return issues

def check_resource_limits(pods):
    issues = []
    for pod in pods:
        for c in pod.spec.containers:
            if not c.resources or not c.resources.limits:
                issues.append({
                    "severity": "warning",
                    "category": "resources",
                    "message": f"Container '{c.name}' in pod '{pod.metadata.name}' has no resource limits"
                })
            if not c.resources or not c.resources.requests:
                issues.append({
                    "severity": "warning",
                    "category": "resources",
                    "message": f"Container '{c.name}' in pod '{pod.metadata.name}' has no resource requests"
                })
    return issues

def check_image_registries(pods):
    issues = []
    for pod in pods:
        for c in pod.spec.containers:
            image = c.image
            if any(x in image for x in ["amazonaws.com", "azurecr.io", "gcr.io"]):
                issues.append({
                    "severity": "warning",
                    "category": "image",
                    "message": f"Container '{c.name}' uses cloud registry '{image}'"
                })
    return issues

# ----------------------------
# SECURITY RULES
# ----------------------------
def check_cloud_iam_annotations(serviceaccounts):
    issues = []
    for sa in serviceaccounts:
        annotations = sa.metadata.annotations or {}
        for key in annotations:
            if any(x in key.lower() for x in ["eks.amazonaws.com", "azure.workload.identity"]):
                issues.append({
                    "severity": "error",
                    "category": "security",
                    "message": f"ServiceAccount '{sa.metadata.name}' uses cloud IAM annotation '{key}'"
                })
    return issues

# ----------------------------
# CONFIGMAPS & SECRETS
# ----------------------------
def check_secrets(configmaps, secrets):
    issues = []
    for sec in secrets:
        if sec.type in ["kubernetes.io/dockerconfigjson", "Opaque"]:
            issues.append({
                "severity": "warning",
                "category": "secrets",
                "message": f"Secret '{sec.metadata.name}' may contain cloud credentials"
            })
    for cm in configmaps:
        if cm.data:
            for key, val in cm.data.items():
                if any(x in val.lower() for x in ["cloud", "aws", "gcp", "azure"]):
                    issues.append({
                        "severity": "warning",
                        "category": "configmap",
                        "message": f"ConfigMap '{cm.metadata.name}' key '{key}' may contain cloud-specific references"
                    })
    return issues

# ----------------------------
# MAIN SCAN FUNCTION
# ----------------------------
def scan_namespace_objects(namespace_objects):
    """
    namespace_objects: dict with keys
      - services
      - pods
      - pvcs
      - ingresses
      - serviceaccounts
      - configmaps
      - secrets
    """
    issues = []
    issues.extend(check_service_types(namespace_objects.get("services", [])))
    issues.extend(check_cloud_service_annotations(namespace_objects.get("services", [])))
    issues.extend(check_ingress_annotations(namespace_objects.get("ingresses", [])))
    issues.extend(check_pvc_storage(namespace_objects.get("pvcs", [])))
    issues.extend(check_hostpath_volumes(namespace_objects.get("pods", [])))
    issues.extend(check_init_containers(namespace_objects.get("pods", [])))
    issues.extend(check_node_selectors(namespace_objects.get("pods", [])))
    issues.extend(check_resource_limits(namespace_objects.get("pods", [])))
    issues.extend(check_image_registries(namespace_objects.get("pods", [])))
    issues.extend(check_cloud_iam_annotations(namespace_objects.get("serviceaccounts", [])))
    issues.extend(check_secrets(namespace_objects.get("configmaps", []), namespace_objects.get("secrets", [])))
    return issues
