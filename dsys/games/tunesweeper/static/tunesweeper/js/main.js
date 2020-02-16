//------------------------------------------------------------------------------
// Description:
//     Main javascript for dynamical systems game interface
//------------------------------------------------------------------------------


//------------------------------------------------------------------------------
// Plotting functions
//------------------------------------------------------------------------------

function plot_system(plotly_div){
	var trace1 = {
	  x: [1, 2, 3, 4],
	  y: [5, 10, 2, 8],
	  marker: {
		  color: "#C8A2C8",
		  line: {
			  width: 2.5
		  }
	  }
	};

	var data = [ trace1 ];

	var layout = { 
	  title: "Dynamical System Coupled Equations",
	  height: 375,
	  font: {size: 14}
	};

	Plotly.newPlot(plotly_div, data, layout, {responsive: true});  
}


function test_d3_plot() {
	var width = 400, height = 400;
	var data = [10, 15, 20, 25, 30];
	
	var svg = d3.select("#dynamical_sys_display")
		.append("svg")
		.attr("width", width)
		.attr("height", height)
		.attr("style", "border:1px solid black");

	var xscale = d3.scaleLinear()
		.domain([0, d3.max(data)])
		.range([0, width - 100]);

	var yscale = d3.scaleLinear()
			.domain([0, d3.max(data)])
			.range([height/2, 0]);

	var x_axis = d3.axisBottom()
			.scale(xscale);

	var y_axis = d3.axisLeft()
			.scale(yscale);

	svg.append("g")
	   .attr("transform", "translate(50, 10)")
	   .call(y_axis);

	var xAxisTranslate = height/2 + 10;

	svg.append("g")
			.attr("transform", "translate(50, " + xAxisTranslate  +")")
			.call(x_axis)

}


//------------------------------------------------------------------------------
// Main
//------------------------------------------------------------------------------

function main() {

	// Plot the curve(s) describing the dynamical system...
	plot_system(document.getElementById("dynamical_sys_display"));
	
// 	test_d3_plot();
	
}

// Add listener to run 'main' when the page loads...
if (window.addEventListener) {
    window.addEventListener('load', main,false); //W3C
} else {
    window.attachEvent('onload', main); //IE
}


