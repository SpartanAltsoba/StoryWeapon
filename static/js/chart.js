// static/js/charts.js

function initializeCharts(revenueVsExpensesData) {
    if (!document.getElementById('amountsChart')) return;
    const ctx = document.getElementById('amountsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: revenueVsExpensesData.map(item => item.year),
            datasets: [
                {
                    label: 'Total Revenue',
                    data: revenueVsExpensesData.map(item => item.total_revenue),
                    backgroundColor: 'rgba(6, 22, 247, 0.5)',
                    borderColor: 'rgba(6, 22, 247, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Total Expenses',
                    data: revenueVsExpensesData.map(item => item.total_expenses),
                    backgroundColor: 'rgba(247, 22, 6, 0.5)',
                    borderColor: 'rgba(247, 22, 6, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { 
                    ticks: {
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 45,
                        color: '#e0e0e0'
                    },
                    grid: {
                        color: '#333'
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#e0e0e0'
                    },
                    grid: {
                        color: '#333'
                    }
                }
            },
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    titleColor: '#e0e0e0',
                    bodyColor: '#e0e0e0',
                    backgroundColor: '#1a1a1a',
                    borderColor: '#f71606',
                    borderWidth: 1
                },
                legend: {
                    position: 'top',
                    labels: {
                        color: '#e0e0e0'
                    }
                }
            }
        }
    });
}
