angular.module('directives.validators.validatePhoneModel', [])
.directive('validatePhoneModel', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, element, attrs, ctrl) {
            var modelRegex = /^[A-Za-z0-9]+$/;

            function validatePhoneModel(value) {
                if (!value) { return; }
                var regular = modelRegex.test(value);

                ctrl.$setValidity("validate", regular);

                return value;
            }

            function getValidate (value) {
                return validatePhoneModel(value);
            }

            ctrl.$formatters.unshift(getValidate);

            ctrl.$parsers.unshift(getValidate);
        }
    };
});