var app = angular.module('nextfeedApp', ['ngCookies']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{')
  $interpolateProvider.endSymbol('}]}')
});

app.run(function($rootScope, $http, $cookies){
    // set the CSRF token here
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
});
