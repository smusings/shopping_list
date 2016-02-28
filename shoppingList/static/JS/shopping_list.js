shoppingList.controller('listController', function($scope, $http){

	$scope.shoppingList = []
	$scope.items = []

	$scope.getData = function()
	{
		$http.get("api/list")
		.success(function(response) {
				$scope.shoppingList = response['data'];
				console.log("skre");
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
		$http.delete('/list/'+id)
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
			$http.post("api/list", JSON.stringify($scope.listName))
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

	$scope.getList = function(id)
	{
		$http.get("/api/list/item"+id)
		.success(function(response) {
				$scope.items = response['data'];
			});
		// Pass in an id, and get the content, then display it in content.
		// This way you can keep everything on one app and save page reloads.
	}
});