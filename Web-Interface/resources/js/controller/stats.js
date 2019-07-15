'use strict';

angular.module('thermostat')
  .controller('StatsCtrl', function ($scope, RoomdataService, ConfigurationService, TemperaturesService) {
    //var roomdata = {"conf":[{"roomID":"0","roomName":"default","sensors":[{"sensorID":"0"},{"sensorID":"1"}],"actuators":[{"actuatorID":"0","type":"hot","valves":[{"valveID":"1"},{"valveID":"2"},{"valveID":"3"}]}]},{"roomID":"1","roomName":"Bagno","sensors":[{"sensorID":"3"}],"actuators":[{"actuatorID":"1","type":"hot","valves":[{"valveID":"4"},{"valveID":"5"}]}]},{"roomID":"2","roomName":"Camera","sensors":[{"sensorID":"4"}],"actuators":[{"actuatorID":"2","type":"cold","valves":[{"valveID":"6"},{"valveID":"7"}]},{"actuatorID":"3","type":"cold"}]}]};
    //var configuration = {"rooms_settings":[{"room":"0","room_name":"default","mode":"manual","info":{"temp":25,"weekend":0},"season":"hot","program":{"MFM":"1","MFE":"2","MFN":"3","WEM":"4","WEE":"5","WEN":"6"}},{"room":"1","room_name":"Cucina","mode":"manual","info":{"temp":23,"weekend":0},"season":"cold","program":{"MFM":"7","MFE":"8","MFN":"9","WEM":"0","WEE":"1","WEN":"2"}},{"room":"2","room_name":"Camera","mode":"manual","info":{"temp":27,"weekend":0},"season":"hot","program":{"MFM":"1","MFE":"2","MFN":"3","WEM":"4","WEE":"5","WEN":"6"}}]};

    var configuration;
    var roomdata;
    var temperatures;
    loadConfiguration();

    //$scope.repeat_var = [];

    //updateGraph();
    /*$scope.data = {
        "nodes": $scope.nodes,
        "links": $scope.links
    };*/


    $scope.temp_options = {
      chart: {
        type: 'discreteBarChart',
        height: 300,//450,
        margin: {
          top: 20,
          right: 20,
          bottom: 50,
          left: 55
        },
        x: function (d) { return d.label; },
        y: function (d) { return d.value; },
        showValues: true,
        valueFormat: function (d) {
          return d3.format(',.4f')(d);
        },
        duration: 500,
        xAxis: {
          axisLabel: 'Room'
        },
        yAxis: {
          axisLabel: 'Temperature',
          axisLabelDistance: -10
        }
      }
    };

    function updateDiscrete() {
      $scope.temp_data = [
        {
          key: "Cumulative Return",
          values: []
        }
      ]
      for (var i = 0; i < temperatures.length; i++) {
        var label = searchRoomGivenId(temperatures[i].room);
        var value = temperatures[i].temperature;
        var temp_value = { "label": label, "value": value };
        $scope.temp_data[0].values.push(temp_value);
      }
    }

    //CONFIGURATION OF THE ROUTE GRAPH
    var color = d3.scale.category20();
    $scope.options = {
      chart: {
        type: 'forceDirectedGraph',
        height: 200,
        width: (function () {
          return nv.utils.windowSize().width / 4
        })(),
        margin: { top: -40, right: 20, bottom: 40, left: 20 },
        color: function (d) {
          if (d.group == 4)
            return "#b41f1f";
          return color(d.group)
        },
        charge: -200,
        linkDist: function (d) {
          if (d.info == "origin")
            return 20;
          else if (d.info == "union")
            return 200;
          return 10;
        },
        radius: function (d) {
          if (d.rad == 1)
            return 13;
          return 8;
        },
        nodeExtras: function (node) {
          node && node
            .append("text")
            .attr("dx", 20)
            .attr("dy", ".35em")
            .text(function (d) { return d.name })
            .style('font-size', '16px');
        }
      }
    };
    function initGraph(data, room_name) {
      data.nodes = [
        { "name": room_name, "group": 2, "rad": 1 },
        { "name": "sensors", "group": 3, "rad": 1 },
        { "name": "actuators", "group": 4, "rad": 1 }
      ];
      data.links = [
        { "source": 0, "target": 1, "value": 30, "info": "origin" },
        { "source": 1, "target": 2, "value": 0.001, "info": "union" },
        { "source": 0, "target": 2, "value": 30, "info": "origin" }
      ];
      $scope.count = 2;
    }
    function pushToNodes(data, name, group) {
      data.nodes.push(newNode(name, group));
      $scope.count++;
    }
    function pushToLinks(data, source, target, value) {
      data.links.push(newLink(source, target, value));
    }
    function newNode(name, group) {
      return {
        name: name,
        group: group
      }
    }
    function newLink(source, target, value) {
      return {
        source: source,
        target: target,
        value: value
      }
    }
    function nodesSensorList(data, sensorList) {
      for (var i = 0; i < sensorList.length; i++) {
        pushToNodes(data, sensorList[i].sensorID, 3);
        pushToLinks(data, 1, $scope.count, 4)
      }
    }
    function nodesActuatorList(data, actuatorList) {
      for (var i = 0; i < actuatorList.length; i++) {
        pushToNodes(data, actuatorList[i].type + '' + actuatorList[i].actuatorID, 4);
        pushToLinks(data, 2, $scope.count, 4)
      }
    }
    function updateGraph(roomdata) {
      $scope.data = [];
      $scope.repeat_var = [];
      for (var i = 0; i < roomdata.conf.length; i++) {
        $scope.data.push({});
        $scope.data[i] = { "nodes": [], "links": [] };
        var room_name = searchRoomGivenId(roomdata.conf[i].roomID);
        initGraph($scope.data[i], room_name);
        nodesSensorList($scope.data[i], roomdata.conf[i].sensors);
        nodesActuatorList($scope.data[i], roomdata.conf[i].actuators);

        $scope.repeat_var.push({ 'data': $scope.data[i], 'roomdata': roomdata.conf[i] });
      }
    }

    function searchRoomGivenId(room_id) {
      var room_name = room_id;
      for (var i = 0; i < configuration.rooms_settings.length; i++) {
        if (configuration.rooms_settings[i].room == room_id) {
          room_name = configuration.rooms_settings[i].room_name;
        }
      }
      return room_name;
    }

    function loadRoomdata() {
      var request = RoomdataService.getConfiguration();
      request.then(
        function (response) {
          //OK
          roomdata = response.data;
          $scope.roomdata = roomdata;
          updateGraph(roomdata);
        },
        function (response) {
          // ERROR
        }
      );
    }

    function loadConfiguration() {
      var request = ConfigurationService.getConfiguration();
      request.then(
        function (response) {
          //OK
          configuration = response.data;
          loadRoomdata();
          loadTemperatures();
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
          updateDiscrete();
        },
        function (response) {
          // ERROR
        }
      );
    }

  });