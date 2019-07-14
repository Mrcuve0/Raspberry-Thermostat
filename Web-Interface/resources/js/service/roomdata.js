'use strict';

angular.module('thermostat')
    .factory('RoomdataService', function ($http, config) {

        var path = config.path;

        return {

            getConfiguration: function () {
                return $http({
                    method: 'GET',
                    url: path + '/roomdata/read.php',
                    headers: {
                        ContentType: "application/json"
                    }
                });
            }

        };
    });