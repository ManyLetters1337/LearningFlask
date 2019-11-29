String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function get_data_for_chart(request_data){

    request_data = request_data.replace(/^[a-zA-Z0-9]/g, '');
    request_data = request_data.replace(/[\s\{'"']/g, '');
    request_data = request_data.split(',').join().split(':').join().split(',')

    let closed = request_data[request_data.indexOf('Closed')+1];
    let in_progress = request_data[request_data.indexOf('InProgress')+1];
    let open = request_data[request_data.indexOf('Open')+1];
    let resolved = request_data[request_data.indexOf('Resolved')+1];

    let chart_data = {
        'Open' : open,
        'Closed' : closed,
        'In Progress' : in_progress,
        'Resolved' : resolved,
    }

    return chart_data
}

function get_data_from_request(){
    url = 'http://' + window.location.host + '/api' + window.location.pathname;
    let xhr = new XMLHttpRequest();

    xhr.open('GET', url, false);
    xhr.send();

    let uuid_index = xhr.responseText.indexOf('uuid') - 10;
    let request_data = xhr.responseText.substring(0, uuid_index)

    return request_data
}

$(function () {
    const COLORS = {
        'Open' : '#ff4f4f',
        'Closed' : '#a39d9d',
        'In Progress' : '#55b5fa',
        'Resolved' : '#6bfa55',

    }

    let request_data = get_data_from_request();
    let chart_data = get_data_for_chart(request_data);

    var donutChartCanvas = $('#donutChart').get(0).getContext('2d');
    var donutData  = {
    labels: [
      'Open',
      'In Progress',
      'Resolved',
      'Close',
    ],
    datasets: [
        {
      data: [chart_data['Open'], chart_data['In Progress'], chart_data['Resolved'], chart_data['Closed']],
      backgroundColor : [COLORS['Open'], COLORS['In Progress'], COLORS['Resolved'], COLORS['Closed']],
        }
    ]
    };
    var donutOptions = {
        maintainAspectRatio : false,
        responsive : true,
    };

    var donutChart = new Chart(donutChartCanvas, {
        type: 'doughnut',
        data: donutData,
        options: donutOptions
    });
})