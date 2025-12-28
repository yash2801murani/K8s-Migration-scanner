// static/script.js

document.getElementById("scanForm").addEventListener("submit", function(e){
    e.preventDefault();

    let namespace = document.getElementById("namespace").value;
    let resultsDiv = document.getElementById("results");
    let loading = document.getElementById("loading");

    // Clear previous results and show spinner
    resultsDiv.innerHTML = "";
    loading.style.display = "block";

    fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "namespace=" + encodeURIComponent(namespace)
    })
    .then(res => res.json())
    .then(data => {
        // Artificial delay for 4 seconds to show loading effect
        setTimeout(() => {
            loading.style.display = "none";

            if (data.error) {
                resultsDiv.innerHTML = `<div class="issue">❌ ${data.error}</div>`;
                return;
            }

            let html = `<h2 style="font-weight:bold;">Namespace: ${data.namespace}</h2>`;
            html += `<div class="issue">Readiness Score: ${data.score}%</div>`;

            if (data.issues.length === 0) {
                html += `<div class="issue">✔ No migration risks detected</div>`;
            } else {
                data.issues.forEach(issue => {
                    let symbol = issue.severity === "error" ? "❌" :
                                 issue.severity === "warning" ? "⚠️" : "✔";
                    html += `<div class="issue">${symbol} ${issue.message}</div>`;
                });
            }

            resultsDiv.innerHTML = html;

        }, 4000); // 4 seconds delay
    })
    .catch(err => {
        loading.style.display = "none";
        resultsDiv.innerHTML = `<div class="issue">❌ Error: ${err}</div>`;
    });
});
