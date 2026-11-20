const API_BASE = "http://127.0.0.1:8000";
let chartInstance = null;

async function renderChart(series_id = "UNRATE") {
    const canvas = document.getElementById("chart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const res = await fetch(`${API_BASE}/api/observations/${series_id}`);
    
    if (!res.ok) {
        console.error(`Failed to fetch ${series_id}: HTTP ${res.status}`);
        return;
    }

    const rows = await res.json();
    const labels = rows.map((row) => row.obs_date);
    const values = rows.map((row) => row.value);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: series_id,
                    data: values,
                    spanGaps: true,
                    borderColor: "#2563eb",
                    borderWidth: 2,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { maxTicksLimit: 12 }
                }
            }
        }
    });
}

window.addEventListener("DOMContentLoaded", () => {
    renderChart("UNRATE");
}); 