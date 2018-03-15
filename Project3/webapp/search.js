'use strict';

angular.module('myApp.search', ['ngRoute', 'angular-loading-bar'])

.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  $locationProvider.html5Mode({
    enabled: true,
    requireBase: false
  });

  $routeProvider.when('/search', {
    templateUrl: 'search.html',
    controller: 'SearchCtrl'
  });
}])

.controller('SearchCtrl', ['$scope', '$location', '$http', function($scope, $location, $http) {

  console.log("Enter...");

  $scope.searchParam = $location.search().search;

  $scope.search = function() {

    console.log("searchString = " + $scope.searchString);
    console.log("version = " + $scope.version);

    var data = {
      search: $scope.searchString,
      version: $scope.version
    };

    var config = {
      params: data
    };

    //var url = 'http://128.195.52.128:8088';
    var url = 'http://localhost:8088';

    var start = new Date().getTime();
    console.log("Request sent... time = " + start + "milis");

    $http.get(url, config).then(
      function(response) {
        var end = new Date().getTime();
        console.log("Response received... time = " + end + "milis");
        console.log("result = " + response.data);
        $scope.searchResults = response.data;
        $scope.searchTime = (end - start) / 1000.0;
      },
      function(error) {
        console.log(error);
      }
    );

    /*$scope.searchResults = [
      {
        title: "result1",
        url: "http://result1.ics.uci.edu/",
        description: "result1 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result2",
        url: "http://result2.ics.uci.edu/",
        description: "result2 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result3",
        url: "http://result2.ics.uci.edu/",
        description: "result2 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result4",
        url: "http://result4.ics.uci.edu/",
        description: "result4 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result5",
        url: "http://result5.ics.uci.edu/",
        description: "result5 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result6",
        url: "http://result6.ics.uci.edu/",
        description: "result6 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result7",
        url: "http://result7.ics.uci.edu/",
        description: "result7 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result8",
        url: "http://result8.ics.uci.edu/",
        description: "result8 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result9",
        url: "http://result9.ics.uci.edu/",
        description: "result9 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      },
      {
        title: "result10",
        url: "http://result10.ics.uci.edu/",
        description: "result10 is a gallery of free snippets resources templates and utilities for bootstrap " +
        "css hmtl js framework. Codes for developers and web designers"
      }
    ];*/
  };

  if ($scope.searchParam != null) {
    $scope.searchString = $scope.searchParam;
    $scope.version = 'naive';

    $scope.search();

  }

}]);