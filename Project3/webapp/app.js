'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  // 'myApp.view1',
  // 'myApp.view2',
  'myApp.search',
  'myApp.version'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  // $locationProvider.hashPrefix('!');
  $locationProvider.html5Mode({
    enabled: true,
    requireBase: false
  });

  // $routeProvider.otherwise({redirectTo: '/results'});
}]);
