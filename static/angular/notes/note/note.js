angular.module('notes.note', [

])

.controller('NoteController', function ($scope, $stateParams, CONSTANS_URLS, service) {
    let getNoteData = function (url) {
        let promiseObj = service.getData(url);
        promiseObj.then(function (value) {
            $scope.note = value;
        })
    };

    getNoteData(CONSTANS_URLS.note + $stateParams['uuid'])
});