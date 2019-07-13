'use strict';


angular
    .module('thermostat', [
        'ngAnimate',
        'ngAria',
        'ngRoute',
        'ngTouch',
        'ui.bootstrap'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'resources/views/thermo.html',
                controller: 'ThermoCtrl'
            })
             .when('/info/', {
                templateUrl: 'resources/views/info.html'
            })
            .otherwise({
                redirectTo: '/'
            });
    })
    .constant('config', {
        path: 'http://thermostat.local/rest'
    })
;
