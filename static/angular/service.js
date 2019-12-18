App.factory('service', function($http, $q){
    return{
        getData: function(){
            var deferred = $q.defer();
            $http({method: 'GET', url: 'http://127.0.0.1:5000/api/projects/statistics'}).
                then (function success(response) {
                        deferred.resolve(response.data);
                    },function error(response) {
                        deferred.reject(response.status);
                    }
                );
            return deferred.promise;
        },
        addPhone: function(name, model, price, phones){
            price = parseFloat(price);
            if(name != "" && !isNaN(price) && model != ""){
                phones.push({name: name, model: model, price: price});
            }
            return phones;
        },
        addCar: function(name, model, price, cars){
            price = parseFloat(price);
            if(name != "" && !isNaN(price) && model != ""){
                cars.push({name: name, model: model, price: price});
            }
            return cars;
        },
        getPage: function(mode){
            if(mode=='Cars')
                return 'templates/carsList.html';
            else if(mode=='Phones')
                return 'templates/phonesList.html';
            else if(mode=='Statistics')
                return 'templates/statistics.html';
        }
    };
});


