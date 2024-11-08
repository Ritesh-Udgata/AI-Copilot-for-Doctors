const express = require('express');
const router = express.Router();

// Hardcoded sample flowchart data
const sampleFlowchartData = {
    nodes: [
        { id: "1", name: "Start", x: 100, y: 100 },
        { id: "2", name: "Decision", x: 300, y: 100 },
        { id: "3", name: "Action 1", x: 300, y: 300 },
        { id: "4", name: "Action 2", x: 500, y: 100 },
        { id: "5", name: "End", x: 700, y: 100 }
    ],
    links: [
        { source: "1", target: "2" },
        { source: "2", target: "3" },
        { source: "2", target: "4" },
        { source: "4", target: "5" }
    ]
};

// Define the API route to get flowchart data
router.get('/get-flowchart-data', (req, res) => {
    res.json(sampleFlowchartData);
});

module.exports = router;
