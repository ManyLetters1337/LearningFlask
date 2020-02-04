import {Utils} from './Utils.js';
import {ViewChart} from './Chart.js';

document.addEventListener("DOMContentLoaded", function(event) { 
	
	Utils.makeRequest('GET', 'http://' + window.location.host + '/api' + window.location.pathname, function(data) {
	    let project;

	    for (let key in data){
	    	project = key;
	    }

	    let chart = new ViewChart(data[project]);
	    
	    chart.createChart();
	});
});
