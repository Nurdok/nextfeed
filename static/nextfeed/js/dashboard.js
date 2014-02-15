function SubscriptionController($scope, $http) {
    $scope.subscription = [];
    $scope.new_feed_url = "";
    $scope.loading = "hidden";
    $scope.form_results_visibility = "hidden"
    $scope.form_result = "hidden text";
    $scope.form_result_type = "success"

    $scope.update_subscriptions = function() {
        $http({method: 'GET', url: 'subscription'}).
            success(function(data, status, headers, config) {
                $scope.subscriptions = []
                for (var i = 0; i < data.length; i++) {
                    $scope.subscriptions.push(data[i])
                }
        });
    }
    $scope.update_subscriptions()

    $scope.add_feed = function() {
        $scope.loading = "visible";
        $scope.form_errors = "";
        $http({method: 'POST', url: 'subscription',
               data: {'link': $scope.new_feed_url}})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
                $scope.new_feed_url = ""
                $scope.loading = "hidden";
                $scope.form_result = "Added feed!"
                $scope.form_result_type = "success"
                $scope.form_results_visibility = "visible"
            })
            .error(function(data, status, headers, config) {
                if (status == 400) {
                    $scope.form_result = data;
                } else {
                    $scope.form_errors = "Invalid feed!";
                }
                $scope.form_result_type = "important"
                $scope.new_feed_url = "";
                $scope.loading = "hidden";
                $scope.form_results_visibility = "visible"
                $scope.update_subscriptions()
            }
        )
    };

    $scope.mark_unread = function(feed_id) {
        $http({method: 'GET', url: 'action/markunread/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };

    $scope.mark_read = function(feed_id) {
        $http({method: 'GET', url: 'action/markread/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };

    $scope.unsubscribe = function(feed_id) {
        $http({method: 'GET', url: 'action/unsubscribe/' + feed_id})
            .success(function(data, status, headers, config) {
                $scope.update_subscriptions()
            })
    };
}
