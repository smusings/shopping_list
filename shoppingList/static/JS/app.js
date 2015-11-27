var shoppingList = angular.module('shoppingList', []);

shoppingList.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[');
	$interpolateProvider.endSymbol(']}');
}]);	//Jinja uses {{}} so we will use {[]} for angularJS