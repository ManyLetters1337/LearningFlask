angular.module('angularApp.projects', [
    'projects.project',
    'constansApiUrls'
])

.config(function config($stateProvider) {
    $stateProvider
        .state('projectInformation', {
            url: '/projects/:uuid',
            params: { uuid : null },
            controller: 'ProjectController',
            templateUrl: 'static/angular/projects/project/view_project.html'
        })

})

.controller('ProjectsController', function ($scope, CONSTANS_URLS, service) {

    let getProjects = function () {
        let promiseObj = service.getData(CONSTANS_URLS.projects);

        promiseObj.then(function (value) {
            $scope.projectsData = value;
        })
    };

    getProjects();

});


