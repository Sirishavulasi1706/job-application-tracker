document.addEventListener("DOMContentLoaded", function () {

    const pending = Number(document.getElementById("pending").value);
    const interviews = Number(document.getElementById("interviews").value);
    const offers = Number(document.getElementById("offers").value);
    const rejected = Number(document.getElementById("rejected").value);

    // Bar Chart
    new Chart(document.getElementById("statusChart"), {
        type: "bar",
        data: {
            labels: [
                "Applied",
                "Interview",
                "Offered",
                "Rejected"
            ],
            datasets: [{
                label: "Applications",
                data: [
                    pending,
                    interviews,
                    offers,
                    rejected
                ],
                borderRadius: 12,
                backgroundColor: [
                    "#0d6efd",
                    "#0dcaf0",
                    "#198754",
                    "#dc3545"
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    // Pie Chart
    new Chart(document.getElementById("pieChart"), {
        type: "doughnut",
        data: {
            labels: [
                "Applied",
                "Interview",
                "Offered",
                "Rejected"
            ],
            datasets: [{
                data: [
                    pending,
                    interviews,
                    offers,
                    rejected
                ],
                backgroundColor: [
                    "#0d6efd",
                    "#0dcaf0",
                    "#198754",
                    "#dc3545"
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

});