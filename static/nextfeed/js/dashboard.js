function SubscriptionController($scope, $http) {
    $scope.subscription = [];

    $scope.update_subscriptions = function() {
        $http({method: 'GET', url: 'subscriptions'}).
            success(function(data, status, headers, config) {
                console.log(data);
                $scope.subscriptions = []
                for (var i = 0; i < data.length; i++) {
                    $scope.subscriptions.push(data[i])
                }
        });
    }
    $scope.update_subscriptions()

    $scope.add_feed = function($scope) {
        $http({method: 'POST', url: 'subscribe'}).
            success(function(data, status, headers, config) {
                $scope.update_subscriptions()
        });
    }
}
