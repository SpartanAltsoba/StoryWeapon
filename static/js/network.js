// static/js/network.js

function drawNetworkGraph(nodes, edges) {
    if (!document.getElementById('networkGraph')) return;

    const cy = cytoscape({
        container: document.getElementById('networkGraph'),
        elements: [
            // Nodes
            ...nodes.map(node => ({
                data: { id: node.id, label: node.label, group: node.group }
            })),
            // Edges
            ...edges.map(edge => ({
                data: { source: edge.from, target: edge.to, relationship: edge.relationship }
            }))
        ],
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'background-color': '#666',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': '#fff',
                    'width': '40px',
                    'height': '40px',
                    'font-size': '12px',
                    'text-outline-width': 1,
                    'text-outline-color': '#000'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'label': 'data(relationship)',
                    'font-size': '10px',
                    'text-rotation': 'autorotate',
                    'text-margin-x': 0,
                    'text-margin-y': -10,
                    'color': '#e0e0e0'
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeOverlap: 20,
            refresh: 20,
            fit: true,
            padding: 30,
            randomize: true,
            componentSpacing: 100,
            nodeRepulsion: 400000,
            edgeElasticity: 100,
            nestingFactor: 5,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        }
    });
}
