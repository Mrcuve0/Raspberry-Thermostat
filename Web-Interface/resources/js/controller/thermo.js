'use strict';

angular.module('thermostat')
    .controller('ThermoCtrl', function ($scope, $interval, ConfigurationService, TemperaturesService) {
    		// Configuration data structures
    		var configuration = {};
    		var room_selected = 0;
    		$scope.room_id = undefined;
    		$scope.room_name = undefined;
    		$scope.required_temperature = undefined;
    		$scope.room_season = undefined;
    		$scope.room_mode = undefined;
    		// Last temperatures data structures
    		var temperatures = [];
    		$scope.temperature = undefined;
    		// Variables for the html form
    		$scope.selected_mode = undefined;
    		$scope.lclick_temp = true;
    		$scope.rclick_temp = true;
    		$scope.manual_weekend = '0';
    		$scope.new_manual_temp = undefined;
    		$scope.prog_MFM = undefined;
    		$scope.prog_MFE = undefined;
    		$scope.prog_MFN = undefined;
    		$scope.prog_WEM = undefined;
    		$scope.prog_WEE = undefined;
    		$scope.prog_WEN = undefined;
    		$scope.date = new Date();
    		// Load data structures from the DB
    		loadConfiguration();
			loadTemperatures();					
			// Activate a timer to automatically reload data structures
			//var reload_timer = $interval(reload_function, 3000);
			var reload_timer; 
			var config_changed = false;
			function activateReloadTimer() {
				reload_timer = setInterval(reloadFunction, 3000);
			}
			function reloadFunction() {
	    		if (config_changed) {
	    			uploadConfiguration();
	    			config_changed = false;
	    		}
	    		else {
		    		loadConfiguration();
					loadTemperatures();					
				}
				$scope.date = new Date();
			}
			function configurationModified() {
				clearInterval(reload_timer);
				config_changed = true;
				reload_timer = setInterval(reloadFunction, 3000);
			}
			activateReloadTimer();
			$scope.$on('$destroy', function() {
				reloadFunction();
		        clearInterval(reload_timer);
			});

            $scope.scroll_top = function() {
                $("html, body").animate({ scrollTop: 0 }, 1000);
            }

			$scope.loadProgrammableTable = function() {
				var program = configuration.rooms_settings[room_selected].program;
				if (program == undefined) {
					configuration.rooms_settings[room_selected].program = {};
				} else {
		    		$scope.prog_MFM = program.MFM;
					$scope.prog_MFE = program.MFE;
					$scope.prog_MFN = program.MFN;
					$scope.prog_WEM = program.WEM;
					$scope.prog_WEE = program.WEE;
					$scope.prog_WEN = program.WEN;
				}
			}

            $scope.increaseRequiredTemperature = function() {
            	configurationModified();
	    		$scope.required_temperature = $scope.required_temperature + 0.5;
	    		configuration.rooms_settings[room_selected].info.temp = $scope.required_temperature;
	    		//uploadConfiguration(configuration);
            }

            $scope.decreaseRequiredTemperature = function() {
            	configurationModified();
	    		$scope.required_temperature = $scope.required_temperature - 0.5;
	    		configuration.rooms_settings[room_selected].info.temp = $scope.required_temperature;
	    		//uploadConfiguration(configuration);
            }

            $scope.changeSeason = function(season) {
            	configurationModified();
            	configuration.rooms_settings[room_selected].season = season;
            	$scope.room_season = season;
            }

            $scope.changeSelectedRoom = function(direction) {
            	if (direction == 0) {
            		if (room_selected > 0) {
            			room_selected -= 1;
            		}
            	} else {
            		if (room_selected < configuration.rooms_settings.length - 1) {
            			room_selected += 1;
            		}
            	}
            	$scope.selected_mode = undefined;
            	$scope.new_manual_temp = undefined;
            	updateButtons();
            	updateConfiguration();
            }

            $scope.changeMode = function(mode) {
            	configurationModified();
            	if (mode == 'manual') {
            		var weekend = 1;
            		if ($scope.manual_weekend == "0")
            			weekend = 0;
            		configuration.rooms_settings[room_selected].mode = 'manual';
            		configuration.rooms_settings[room_selected].info.weekend = weekend;
            		configuration.rooms_settings[room_selected].info.temp = $scope.new_manual_temp;
            		//$scope.required_temperature = $scope.new_manual_temp;
            	} else if (mode == 'antifreeze') {
            		configuration.rooms_settings[room_selected].mode = 'antifreeze';
            		//$scope.room_mode = 'antifreeze';            	
            	} else if (mode == 'programmable') {
            		configuration.rooms_settings[room_selected].mode = 'programmable';
		    		configuration.rooms_settings[room_selected].program.MFM = $scope.prog_MFM;
					configuration.rooms_settings[room_selected].program.MFE = $scope.prog_MFE;
					configuration.rooms_settings[room_selected].program.MFN = $scope.prog_MFN;
					configuration.rooms_settings[room_selected].program.WEM = $scope.prog_WEM;
					configuration.rooms_settings[room_selected].program.WEE = $scope.prog_WEE;
					configuration.rooms_settings[room_selected].program.WEN = $scope.prog_WEN;
            	}
            	updateConfiguration();
            }

            function updateButtons() {
            	$scope.lclick_temp = false;
            	$scope.rclick_temp = false;
            	if (room_selected == 0) {
	    			$scope.lclick_temp = true;
	    		} 
	    		if (room_selected == configuration.rooms_settings.length - 1) {
    				$scope.rclick_temp = true;
	    		}
            }

            function updateConfiguration() {
            	if (configuration.rooms_settings[room_selected] != undefined) {
		    		var config_room = configuration.rooms_settings[room_selected]; 
		    		$scope.room_id = config_room.room;
		    		$scope.room_name = config_room.room_name;
		    		$scope.room_season = config_room.season;
		    		$scope.room_mode = config_room.mode;
		    		//depends on the mode
		    		$scope.required_temperature = getRequiredTemperature(config_room);
		        }
		        updateButtons();
		        updateTemperatures();
            }

            function getRequiredTemperature(config_room) {
            	var result = 0;
            	if (config_room.mode == 'manual') {
            		result = config_room.info.temp;
            	} else if (config_room.mode == 'programmable') {
            		var entry = 'MF';
            		if ($scope.date.getDay() >= 6)
            			entry = 'WE';
            		var hour = $scope.date.getHours();
            		if (hour >= 0 && hour <= 5)
            			entry = entry + 'N';
            		else if (hour >= 6 && hour <= 12)
            			entry = entry + 'M';
            		else 
            			entry = entry + 'E';
            		result = config_room.program[entry];
            	} else if (config_room.mode == 'antifreeze') {
            		result = 15;
            	}
            	return result;
            }

            function updateTemperatures() {
				var found_temp = temperatures.find(function(entry) {
					return entry.room == $scope.room_id;
				});
				if (found_temp != undefined) {
		    		$scope.temperature = found_temp.temperature;
		    	} else
		    		$scope.temperature = undefined;//0
            }

            function loadConfiguration() {
	            var request = ConfigurationService.getConfiguration();
	            request.then(
	            	function (response) {
	                    //OK
	                    configuration = response.data;
	                    updateConfiguration();
	                },
	                function (response) {
	                    // ERROR
	                }
                );
	        }

            function uploadConfiguration() {
	            var request = ConfigurationService.postConfiguration(configuration);
	            request.then(
	            	function (response) {
	                    // OK 
	                    loadConfiguration();
	                },
	                function (response) {
	                    // ERROR
	                }
                );
	        }

            function loadTemperatures() {
	            var request = TemperaturesService.getTemperatures();
	            request.then(
	            	function (response) {
	                    //OK
	                    temperatures = response.data.list;
	                    updateTemperatures();
	                },
	                function (response) {
	                    // ERROR
	                }
                );
	        }

    	});