// static/js/dashboard.js

$(document).ready(function () {
    // Load the extracted data
    $.ajax({
        url: '/dashboard/data', // Endpoint to get the extracted data
        type: 'GET',
        success: function (response) {
            // Parse the JSON data
            let jsonData = response.data;
            // Generate the network graph
            generateNetworkGraph(jsonData.visualization_data.network_graph);
            // Generate the financial charts
            generateFinancialCharts(jsonData.visualization_data.bar_chart);
            // Display the analysis summary
            displayAnalysisSummary(jsonData.analysis_summary);
        },
        error: function (xhr, status, error) {
            console.error('Error loading data for dashboard:', error);
            $('#networkGraphContainer').html('<p>Error loading data.</p>');
            $('#financial-charts').html('<p>Error loading data.</p>');
        }
    });

    function generateNetworkGraph(networkData) {
        let nodes = new vis.DataSet(networkData.nodes);
        let edges = new vis.DataSet(networkData.edges);

        let container = document.getElementById('networkGraphContainer');
        let data = {
            nodes: nodes,
            edges: edges
        };
        let options = {
            nodes: {
                shape: 'dot',
                size: 16
            },
            edges: {
                width: 2
            }
        };
        let network = new vis.Network(container, data, options);
    }

    function generateFinancialCharts(barChartData) {
        // Revenue vs Expenses Chart
        let revenueExpensesCtx = document.getElementById('revenueExpensesChart').getContext('2d');
        let revenueExpensesChart = new Chart(revenueExpensesCtx, {
            type: 'bar',
            data: {
                labels: barChartData.revenue_vs_expenses.map(item => item.year),
                datasets: [
                    {
                        label: 'Total Revenue',
                        data: barChartData.revenue_vs_expenses.map(item => item.total_revenue),
                        backgroundColor: 'rgba(54, 162, 235, 0.6)'
                    },
                    {
                        label: 'Total Expenses',
                        data: barChartData.revenue_vs_expenses.map(item => item.total_expenses),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)'
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Revenue vs Expenses Over Time'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        // Net Assets Over Time Chart
        let netAssetsCtx = document.getElementById('netAssetsChart').getContext('2d');
        let netAssetsChart = new Chart(netAssetsCtx, {
            type: 'line',
            data: {
                labels: barChartData.assets_over_time.map(item => item.year),
                datasets: [
                    {
                        label: 'Net Assets',
                        data: barChartData.assets_over_time.map(item => item.net_assets),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        fill: false,
                        borderColor: 'rgba(75, 192, 192, 1)'
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Net Assets Over Time'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    function displayAnalysisSummary(analysisSummary) {
        $('#analysisSummary').text(JSON.stringify(analysisSummary, null, 2));
    }
});
