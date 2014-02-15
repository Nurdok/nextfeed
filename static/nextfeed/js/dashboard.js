function SubscriptionController($scope, $http) {
    $scope.subscription = [];
    $scope.new_feed_url = "";
    $scope.loading = "hidden";
    $scope.form_errors = "";

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
        $scope.loading = "visible";
        $scope.form_errors = "";
        $http({method: 'POST', url: 'subscription',
               data: {'link': $scope.new_feed_url}})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
                $scope.new_feed_url = ""
                $scope.loading = "hidden";
            })
            .error(function(data, status, headers, config) {
                console.log("Adding feed failed!")
                $scope.form_errors = "Invalid feed!";
                $scope.new_feed_url = "";
                $scope.loading = "hidden";
                $scope.update_subscriptions()
            }
        )
    };

    $scope.mark_unread = function(feed_id) {
        console.log("Marking feed " + feed_id + " as unread.")
        $http({method: 'GET', url: 'action/markunread/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };

    $scope.mark_read = function(feed_id) {
        console.log("Marking feed " + feed_id + " as read.")
        $http({method: 'GET', url: 'action/markread/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };

    $scope.unsubscribe = function(feed_id) {
        console.log("Unsubscribing from feed " + feed_id)
        $http({method: 'GET', url: 'action/unsubscribe/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };
}
