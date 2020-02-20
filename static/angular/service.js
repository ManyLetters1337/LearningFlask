App.service('service', function ($http, $q){
    return {
        getData: function (url) {
            var deffered = $q.defer();
            $http({method: 'GET', url: url}).
                then (function success(response){
                    deffered.resolve(response.data);
                }, function error(response) {
                    deffered.reject(response.status);
                });
            return deffered.promise;
        },
    };
});