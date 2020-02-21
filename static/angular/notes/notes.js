angular.module('angularApp.notes', [
    'constansApiUrls',
    'notes.note'
])
.config(function config($stateProvider) {
    $stateProvider
        .state('notes.noteInformation', {
            url: '/:uuid',
            params: { uuid : null },
            controller: 'NoteController',
            templateUrl: 'static/angular/notes/note/view_note.html'
        })

})

.controller('NotesController', function ($scope, CONSTANS_URLS, service) {
    let getNotes = function () {
        let promiseObj = service.getData(CONSTANS_URLS.notes);

        promiseObj.then(function (value) {
            $scope.notesData = value;
        })
    };

    getNotes()

});