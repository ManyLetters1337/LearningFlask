String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

$(function () {

    url = 'http://' + window.location.host + '/api' + window.location.pathname;
    let xhr = new XMLHttpRequest();

    xhr.open('GET', url, false);
    xhr.send();


    let second_ind = xhr.responseText.indexOf('uuid') - 10;
    let substring = xhr.responseText.substring(0, second_ind)
    substring = substring.replace(/\s/g, '');
    substring = substring.replaceAll('{', '');
    substring = substring.replace('[', '');
    substring = substring.replaceAll('"', '');
    substring = substring.split(',').join().split(':').join().split(',')

    let closed = substring[substring.indexOf('Closed')+1];
    let in_progress = substring[substring.indexOf('In Progress')+1];
    let open = substring[substring.indexOf('Open')+1];
    let resolved = substring[substring.indexOf('Resolved')+1];

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
      data: [open,in_progress,resolved,closed],
      backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
        }
    ]
    };
    var donutOptions     = {
        maintainAspectRatio : false,
        responsive : true,
    };
//Create pie or douhnut chart
// You can switch between pie and douhnut using the method below.
    var donutChart = new Chart(donutChartCanvas, {
        type: 'doughnut',
        data: donutData,
        options: donutOptions
    });
})