def print_report(namespace, issues):
    print("\nKubernetes Migration Readiness Report")
    print("=" * 45)
    print(f"Namespace: {namespace}\n")

    if not issues:
        print("✔ No migration risks detected")
        print("Readiness Score: 100%")
        return

    score = 100

    for issue in issues:
        if issue["severity"] == "warning":
            score -= 5
            icon = "⚠️"
        else:
            score -= 15
            icon = "❌"

        print(f"{icon} {issue['message']}")

    print(f"\nReadiness Score: {max(score,0)}%")
