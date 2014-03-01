function ReportIssueController($scope, $http, $modal) {
    $scope.open = function () {
      var modalInstance = $modal.open({
        templateUrl: 'myModalContent.html',
        controller: ReportIssueModalController
      });
    };
};


var ReportIssueModalController = function ($scope, $http, $modalInstance,
                                           $timeout) {
    $scope.button_text = "Send";
    $scope.is_sending = false;
    $scope.button_type = "primary"

    $scope.ok = function (summary, details) {
        $scope.is_sending = true;
        $scope.button_text = "Sending...";
        var data = {summary: summary, details: details}
        $http({method: 'POST', url: 'report', data: data})
            .success(function(data, status, headers, config) {
                $scope.button_text = "Sent!";
            })
            .error(function(data, status, headers, config) {
                $scope.button_text = "Error! Try again later."
                $scope.button_type = "danger"
            });
        $timeout($modalInstance.close, 3000)
    };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
};
