shoppingList.controller('listController', function($scope, $http){

	$scope.shoppingList = []

	$scope.getData = function()
	{
		$http.get("/shoppingList.json")
		.success(function(response) {
				$scope.shoppingList = response['data'];
				console.log($scope.shoppingList);
			});
	}

	$scope.getData();
});