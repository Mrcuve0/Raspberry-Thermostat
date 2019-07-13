'use strict';

angular.module('thermostat')
    .factory('TemperaturesService', function ($http, config) {

        var path = config.path;

        return {

            getTemperatures: function () {
                return $http({
                    method: 'GET',
                    url: path + '/temperatures/read.php',
                    headers: {
                        ContentType: "application/json"
                    }
                });
            }

        };
    });