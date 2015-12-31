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

	$scope.submitList = function()
	{
		if($scope.listName.length >= 1)
		{
			console.log($scope.listName);

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