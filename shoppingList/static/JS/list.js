shoppingList.controller('listController', function($scope, $http){

	$scope.list = []
	$scope.listId = document.getElementById('listId').value

	$scope.getData = function()
	{
		$scope.getUrl = document.getElementById('url').value
		$http.get($scope.getUrl)
		.success(function(response) {
				$scope.list = response['data'];
			});
	}

	$scope.getData();

	$scope.addItem = function()
	{
		$scope.newItem = [{
			'name': $scope.itemName,
			'list_id': $scope.listId,
			'quantity': $scope.itemQuantity
		}];

		$http.post('/newItem.json', $scope.newItem)
		.success(function(response)
			{
				console.log("Item Created");
				$scope.getData();

			});
	}

	$scope.deleteItem = function()
	{

	}


});