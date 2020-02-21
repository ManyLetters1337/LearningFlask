angular.module('users.user', [

])

.controller('UserController', function ($scope, $stateParams, service, CONSTANS_URLS) {
    let getUserData = function (url, data) {
        let promiseObj = service.getData(url);
        promiseObj.then(function (value) {
            $scope[data] = value;
        })
    };

    getUserData(CONSTANS_URLS.users + $stateParams['uuid'], 'usersData');
    getUserData(CONSTANS_URLS.userProjects + $stateParams['uuid'], 'projects');
    getUserData(CONSTANS_URLS.userNotes + $stateParams['uuid'], 'notes');


});