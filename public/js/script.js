// document.getElementById('generateFlowchart').addEventListener('click', () => {
//     fetch('/api/get-flowchart-data')
//         .then(response => response.json())
//         .then(data => renderFlowchart(data))
//         .catch(error => console.error('Error fetching data:', error));
// });

// function renderFlowchart(data) {
//     d3.select("#flowchart").html("");
//     const svg = d3.select("#flowchart").append("svg").attr("width", 800).attr("height", 600);
//     const simulation = d3.forceSimulation(data.nodes)
//         .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
//         .force("charge", d3.forceManyBody().strength(-300))
//         .force("center", d3.forceCenter(400, 300))
//         .on("tick", ticked);

//     const link = svg.append("g").attr("class", "links")
//         .selectAll("line").data(data.links).enter().append("line").attr("stroke", "#999").attr("stroke-width", 2);

//     const node = svg.append("g").attr("class", "nodes")
//         .selectAll("circle").data(data.nodes).enter().append("circle")
//         .attr("r", 20).attr("fill", "steelblue").call(drag(simulation));

//     const label = svg.append("g").attr("class", "labels")
//         .selectAll("text").data(data.nodes).enter().append("text")
//         .attr("dy", 4).attr("text-anchor", "middle").text(d => d.name);

//     function ticked() {
//         link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
//         node.attr("cx", d => d.x).attr("cy", d => d.y);
//         label.attr("x", d => d.x).attr("y", d => d.y);
//     }

//     function drag(simulation) {
//         return d3.drag().on("start", (event, d) => {
//             if (!event.active) simulation.alphaTarget(0.3).restart();
//             d.fx = d.x;
//             d.fy = d.y;
//         }).on("drag", (event, d) => {
//             d.fx = event.x;
//             d.fy = event.y;
//         }).on("end", (event, d) => {
//             if (!event.active) simulation.alphaTarget(0);
//             d.fx = null;
//             d.fy = null;
//         });
//     }
// }
function submitAndRedirect() {
    // document.getElementById("myForm").submit();

    document.getElementById("work").scrollIntoView({ behavior: "smooth" });
  }