'use strict';

angular.module('thermostat')
    .factory('ConfigurationService', function ($http, config) {

        var path = config.path;

        return {

            getConfiguration: function () {
                return $http({
                    method: 'GET',
                    url: path + '/configuration/read.php',
                    headers: {
                        ContentType: "application/json"
                    }
                });
            },

            postConfiguration: function (configuration) {
                return $http({
                    method: 'POST',
                    url: path + '/configuration/update.php',
                    data: configuration,
                    headers: {
                        ContentType: "application/json",
                        dataType: "json"
                    }
                });
            }

        };
    });