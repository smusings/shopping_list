shoppingList.controller('listController', function($scope, $http){

	$scope.list = []
	$scope.listId = document.getElementById('listId').value

	$scope.getData = function()
	{
		$scope.getUrl = document.getElementById('url').value
		$http.get($scope.getUrl)
		.success(function(response) {
				console.log(response['data']);
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
			'price': $scope.itemPrice
		}];

		$http.post('/newItem.json', $scope.newItem)
		.success(function(response)
			{
				alert(response);
				$scope.getData();
			});
	}

	$scope.deleteItem = function(id)
	{
		console.log(id);
		$http.post('/deleteItem.json', id)
		.success(function(response)
		{
			alert(response);
			$scope.getData();
		});
	}


});