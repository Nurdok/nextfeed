var app = angular.module('nextfeedApp', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{')
  $interpolateProvider.endSymbol('}]}')
});