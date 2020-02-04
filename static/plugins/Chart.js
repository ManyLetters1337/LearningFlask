const COLORS = {
    Open : '#ff4f4f',
    Closed : '#a39d9d',
    InProgress: '#55b5fa',
    Resolved : '#6bfa55'
};

const STATUSES = {
	Open : 'Open',
	Closed : 'Closed',
	InProgress : 'In Progress',
	Resolved : 'Resolved'
};

export class ViewChart{
	constructor(statuses){
		this.status_data = statuses;
	};

	getCanvas(){

		return document.getElementById('donutChart').getContext('2d');
	};

	setParams(){
		let donutData = {
	    labels: [
	      STATUSES.Open,
	      STATUSES.InProgress,
	      STATUSES.Resolved,
	      STATUSES.Closed,
	    ],
	    datasets: [
	        {
	      data: [this.status_data[STATUSES.Open], 
	      		 this.status_data[STATUSES.InProgress],
	      		 this.status_data[STATUSES.Resolved],
	      		 this.status_data[STATUSES.Closed]
	      		],
	      backgroundColor : [COLORS.Open, COLORS.InProgress, COLORS.Resolved, COLORS.Closed],
	        }
	    ]
	    };

	    return donutData;
	}

	createChart(){
	  
	    let donutChartCanvas = this.getCanvas();
	    
	    let donutData  = this.setParams();

	    let donutOptions = {
	        maintainAspectRatio : false,
	        responsive : true,
	    };

	    let donutChart = new Chart(donutChartCanvas, {
	        type: 'doughnut',
	        data: donutData,
	        options: donutOptions
	    });
	}
}


