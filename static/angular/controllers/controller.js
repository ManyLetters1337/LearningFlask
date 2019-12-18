document.addEventListener("DOMContentLoaded", function(event) {
    App.controller("Controller", function ($scope, service) {

    $scope.data = {};

    $scope.modes = [{
        value: 'Cars',
        label: 'Cars'
    },{
        value: 'Phones',
        label: 'Phones'
    },{
        value: 'Statistics',
        label: 'Statistics'
    }];

    $scope.phones = [{
        name: "iPhone",
        model: "X",
        price: 1200,
    },
    {
        name: "Samsung",
        model: "Galaxy",
        price: 800,
    },
    {
        name: "Nokia",
        model: "6.1 plus",
        price: 400,
    }];
    $scope.cars = [{
        name: "Volkswagen",
        model: "B-5",
        price: 12000,
    },
    {
        name: "BMW",
        model: "M3",
        price: 8000,
    },
    {
        name: "Mercedes",
        model: "E220",
        price: 4000,
    }];

    var promiseObj=service.getData();
    promiseObj.then(function(value) { $scope.projects=value; });

    $scope.addPhone = function(name, model, price){
        service.addPhone(name, model, price, $scope.phones);
    };

    $scope.getList = function (mode) {
        return service.getPage(mode);
    };

     $scope.addCars = function (name, model, price) {
        service.addCar(name, model, price, $scope.cars);
     };
    });
});