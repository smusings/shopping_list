shoppingList.controller('listController', function($scope, $http){

	$scope.list = []
	$scope.getUrl = document.getElementById('url').value
	$http.get($scope.getUrl)
	.success(
		function(response) {
			$scope.list = response['data'];
		})

});