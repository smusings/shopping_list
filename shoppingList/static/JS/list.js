shoppingList.controller('listController', function($scope, $http){

	$scope.list = []
	$scope.listId = document.getElementById('listId').value
	$scope.name;

	$scope.getData = function()
	{
		$scope.getUrl = document.getElementById('url').value
		$http.get($scope.getUrl)
		.success(function(response) {
				$scope.list = response['data'];
			});
	}

	$scope.getData();

	$http.get('/list/name/'+listId.value).success(function(response) {
		document.getElementById('list_name').innerHTML = response.name
	});

	$scope.addItem = function()
	{
		$scope.newItem = [{
			'name': $scope.itemName,
			'list_id': $scope.listId,
			'quantity': $scope.itemQuantity,
			'price': $scope.itemPrice
		}];

		$http.post('/item', $scope.newItem)
		.success(function(response)
			{
				alert(response);
				$scope.getData();
				clearField();
			});
	}

	$scope.deleteItem = function(id)
	{
		$http.delete('/item/'+id)
		.success(function(response)
		{
			alert(response);
			$scope.getData();
		});
	}

	function clearField()
	{
		$scope.itemName = "";
		$scope.itemQuantity = "";
		$scope.itemPrice = "";
	}
});