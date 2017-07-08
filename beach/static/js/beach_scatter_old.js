
function drawScatterPlot(scatterPlot) {

    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = $( "#scatterPlotDiv" ).width(),
        height = $( window ).height() - $( "#navBar" ).height() - 100;

    // Parse the date / time
    var parseDate = d3.time.format("%Y-%m-%d").parse;

    // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(scatterPlot.x_ticks);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(scatterPlot.y_ticks);
        
    // Adds the svg canvas
    var svg = d3.select("#scatterPlotDiv")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");

    // Scale the range of the data
    x.domain(d3.extent(scatterPlot.points, function(d) { return parseDate(d.date); }));
    y.domain([0, d3.max(scatterPlot.points, function(d) { return d.dna_reading; })]);

    // add the tooltip area to the webpage
    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    svg.selectAll(".dot")
        .data(scatterPlot.points)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 3.5)
        .attr("cx", function(d) {
            return x(parseDate(d.date));
        })
        .attr("cy", function(d) { return y(d.dna_reading); })
        .style("fill", function(d) { return 'red'; }) 
        .on("mouseover", function(d) {
            tooltip.transition()
                   .duration(200)
                   .style("opacity", .9);
            tooltip.html("Point")
                   .style("left", (d3.event.pageX + 5) + "px")
                   .style("top", (d3.event.pageY - 28) + "px");
          })
          .on("mouseout", function(d) {
              tooltip.transition()
                   .duration(500)
                   .style("opacity", 0);
          });


    // Add the X Axis
    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

    // Add the Y Axis
    svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

}