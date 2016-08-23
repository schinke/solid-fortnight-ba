// var remote = require('remote')
// var menu = remote.require('menu')
const {ipcRenderer} = require('electron')
function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }
angular.module('mainWindowApp', [])

.controller('MainWindowController', function($scope) {
  $scope.visibleClass='Product' // set the default table
  $scope.productSortField     = 'id'; // set the default product sort type
  $scope.productSortField     = 'id'; // set the default product sort type
  $scope.productSortReverse  = false;  // set the default sort order
  $scope.searchTerm   = ''; 
  $scope.showPopup = function(arg){
    ipcRenderer.send('show-prod-form', arg)
    console.log(arg)
  }
  $scope.toggleAddItemModal = function(arg){
    $scope.showProductModal=($scope.visibleClass==="Product"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    $scope.showValueModal=($scope.visibleClass==="Value"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    $scope.showReferenceModal=($scope.visibleClass==="Reference"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    console.log("modal toggled")
  }
  $scope.addProduct = function(arg){
    newProduct={'name':$scope.newProductName}
  }
  httpGetAsync('http://localhost:5000/products', function(response){
  $scope.productsFromServer=angular.fromJson(response);
  $scope.$apply();
  });

  httpGetAsync('http://localhost:5000/values', function(response){
  $scope.valuesFromServer=angular.fromJson(response);
  $scope.$apply();
  });

  httpGetAsync('http://localhost:5000/references', function(response){
  $scope.referencesFromServer=angular.fromJson(response);
  $scope.$apply();
  });
})
.controller('ProductModalController', function($scope){
})

.directive('addProductModal', function(){
  return({
    templateUrl:"snippets/addProductModal.html",
  })
})
.controller('ValueModalController', function($scope){
})
.directive('addValueModal', function(){
  return({
    templateUrl:"snippets/addValueModal.html",
  })
})
.controller('ReferenceModalController', function($scope){
})
.directive('addReferenceModal', function(){
  return({
    templateUrl:"snippets/addreferenceModal.html",
  })
})