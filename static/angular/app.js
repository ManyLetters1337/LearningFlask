var App = angular.module('angularApp', [
    'ui.router',
    'angularApp.users',
    'angularApp.projects',
    'angularApp.notes',
    'angularApp.statistics'
]);


angular.module('angularApp')
.config(function config($stateProvider, $locationProvider) {

    $stateProvider
        .state('statistics', {
            url: '/',
            controller: 'StatisticController',
            templateUrl: 'static/angular/statistics/statistics.html'
        })
        .state('users', {
            url: '/users',
            controller: 'UsersController',
            templateUrl: 'static/angular/users/view_users_table.html'
        })

        .state('projects', {
            url: '/projects',
            controller: 'ProjectsController',
            templateUrl: 'static/angular/projects/view_projects_table.html'
        })

        .state('notes', {
            url: '/angular/notes',
            controller: 'NotesController',
            templateUrl: 'static/angular/notes/view_notes_table.html'
        })
});
