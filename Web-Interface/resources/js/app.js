'use strict';


angular
    .module('thermostat', [
        'ngAnimate',
        'ngAria',
        'ngRoute',
        'ngTouch',
        'ui.bootstrap',
        'nvd3'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'resources/views/thermo.html',
                controller: 'ThermoCtrl'
            })
            .when('/stats/', {
                templateUrl: 'resources/views/stats.html',
                controller: 'StatsCtrl'
            })
            .when('/info/', {
                templateUrl: 'resources/views/info.html',
            })
            .otherwise({
                redirectTo: '/'
            });
    })
    .constant('config', {
        path: 'http://thermostat.local/rest'
    })
;
