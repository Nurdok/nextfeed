function SubscriptionController($scope, $http) {
    $scope.subscription = [];
    $scope.new_feed_url = "";

    $scope.update_subscriptions = function() {
        $http({method: 'GET', url: 'subscription'}).
            success(function(data, status, headers, config) {
                console.log(data);
                $scope.subscriptions = []
                for (var i = 0; i < data.length; i++) {
                    $scope.subscriptions.push(data[i])
                }
        });
    }
    $scope.update_subscriptions()

    $scope.add_feed = function() {
        console.log('Adding a feed!')
        $http({method: 'POST', url: 'subscription',
               data: {'link': $scope.new_feed_url}}).
            success(function(data, status, headers, config) {
                $scope.update_subscriptions()
        });
    }
}
