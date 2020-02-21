angular.module('angularApp.statistics', [

])

.controller('StatisticController', function ($scope, CONSTANS_URLS, $stateParams, service) {
    function getUsers (url) {
        let promiseObj = service.getData(url);
        promiseObj.then(function (value){
            $scope.users = value;
            console.log($scope.users)
        })
    }

    getUsers(CONSTANS_URLS.users);

    function getCanvas(userID) {
        return document.getElementById('donutChart' + userID).getContext('2d');
    }

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

    function setParams(statusData){
        return {
            labels: [
                STATUSES.Open,
                STATUSES.InProgress,
                STATUSES.Resolved,
                STATUSES.Closed,
            ],
            datasets: [
                {
                    data: [statusData[STATUSES.Open],
                        statusData[STATUSES.InProgress],
                        statusData[STATUSES.Resolved],
                        statusData[STATUSES.Closed]
                    ],
                    backgroundColor: [COLORS.Open, COLORS.InProgress, COLORS.Resolved, COLORS.Closed],
                }
            ]
        };
	}

	 $scope.createChart = function (userID) {

        let xhr = new XMLHttpRequest();

        xhr.open(method, url, false);

        console.log(userID);
        statusData = {
            'Open' : 1,
            'Closed' : 2,
            'In Progress' : 3,
            'Resolved' : 4
        };

        let donutChartCanvas = getCanvas();

        let donutData = setParams(statusData);

        let donutOptions = {
            maintainAspectRatio: false,
            responsive: true,
        };

        let donutChart = new Chart(donutChartCanvas, {
            type: 'doughnut',
            data: donutData,
            options: donutOptions
        });
    }

});