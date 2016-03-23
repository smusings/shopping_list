shoppingList.controller('listController', function($scope, $http){

	$scope.shoppingList = []
	$scope.items;
	$scope.listId;

	$scope.getData = function()
	{
		$http.get("api/list")
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
		var listContainer = document.getElementById("list-container");

		$http.get("/api/list/item"+id)
		.success(function(response) {
				$scope.items = response['data'];
				listContainer.className = "col-md-3 text-right";
				$scope.listId = id;
				clearField();
			});
	}

	$scope.addItem = function(item, quantity, price)
	{
		var newItem = [{
			'name': item,
			'list_id': $scope.listId,
			'quantity': quantity,
			'price': price
		}];

		$http.post('/api/item', newItem)
		.success(function(response)
			{
				alert(response);
				$scope.getList($scope.listId);
			});
	}

	function clearField()
	{
		$scope.itemName = "";
		$scope.itemQuantity = "";
		$scope.itemPrice = "";
	}

	$scope.shareList = function()
	{
	    var email = document.getElementById("email").value;

	}
});