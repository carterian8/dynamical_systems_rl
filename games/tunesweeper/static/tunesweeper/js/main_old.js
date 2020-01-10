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


//------------------------------------------------------------------------------
// Main
//------------------------------------------------------------------------------

function main() {

	// Plot the curve(s) describing the dynamical system...
	plot_system(document.getElementById("dynamical_sys_display"));
	
	document.getElementsByClassName("dropdown-trigger").dropdown();
	
// 	$(".dropdown-trigger").dropdown();
}

// Add listener to run 'main' when the page loads...
if (window.addEventListener) {
    window.addEventListener('load', main,false); //W3C
} else {
    window.attachEvent('onload', main); //IE
}


