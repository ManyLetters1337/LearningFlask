document.addEventListener("DOMContentLoaded", function(event) {

    var App = angular.module("App", []);
        App.controller("Controller", function ($scope, $http) {

        $scope.data = {};


        $scope.modes = [{
            value: 'Cars',
            label: 'Машины'
        },{
            value: 'Phones',
            label: 'Смартфоны'
        },{
            value: 'Statistics',
            label: 'Статистика по проектам'
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

        $http({method: 'GET', url: 'http://127.0.0.1:5000/api/projects/statistics'}).
            then(function success(response) {
                $scope.projects = response.data;
        });


        $scope.addPhone = function (name, model, price) {
            price = parseFloat(price);
            if(name != "" && !isNaN(price) && model != ""){
                $scope.phones.push({name: name, model: model, price: price});
            }
        }

         $scope.addCars = function (name, model, price) {
            price = parseFloat(price);
            if(name != "" && !isNaN(price) && model != ""){
                $scope.cars.push({name: name, model: model, price: price});
            }
        }


    });
});