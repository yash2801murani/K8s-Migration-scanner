# scanner.py
from kubernetes import client, config

def get_k8s_clients():
    # Load kubeconfig and create clients
    config.load_kube_config()
    v1 = client.CoreV1Api()          # Pods, Services, PVCs, ServiceAccounts
    apps = client.AppsV1Api()        # Deployments, StatefulSets
    net = client.NetworkingV1Api()   # Ingresses
    return v1, apps, net

def scan_namespace(namespace):
    v1, apps, net = get_k8s_clients()

    services = v1.list_namespaced_service(namespace).items
    deployments = apps.list_namespaced_deployment(namespace).items
    pvcs = v1.list_namespaced_persistent_volume_claim(namespace).items
    pods = v1.list_namespaced_pod(namespace).items
    serviceaccounts = v1.list_namespaced_service_account(namespace).items
    ingresses = net.list_namespaced_ingress(namespace).items

    return {
        "services": services,
        "deployments": deployments,
        "pvcs": pvcs,
        "pods": pods,
        "serviceaccounts": serviceaccounts,
        "ingresses": ingresses
    }
