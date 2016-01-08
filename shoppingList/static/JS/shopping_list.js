shoppingList.controller('listController', function($scope, $http){

	$scope.shoppingList = []

	$scope.getData = function()
	{
		$http.get("/shoppingList.json")
		.success(function(response) {
				$scope.shoppingList = response['data'];
			});
	}

	$scope.getData();

	$scope.listForm = false;

	$scope.toggleForm = function()
	{
		$scope.listForm = $scope.listForm?false:true;
	}

	$scope.delete_list= function(id)
	{
		$http.delete('/deleteTable.json/'+id)
		.success(function(response)
		{
			alert(response);
			$scope.getData();
		});
	}

	$scope.submitList = function()
	{
		if($scope.listName.length >= 1)
		{
			$http.post("/newList.json", JSON.stringify($scope.listName))
			.success(function(response)
			{
				alert(response);
			});
			$scope.toggleForm();
			$scope.getData();
		}
		else
		{
			alert("Enter List Name!")
		}
	}
});