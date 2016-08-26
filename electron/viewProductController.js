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

function httpPostAsync(theUrl, jsonData, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
  xmlHttp.open("POST", theUrl, true); // true for asynchronous 
  xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
  xmlHttp.send(jsonData);
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

  //load prod json files into scope
  $scope.convertLegacy = function(legacyProducts,legacyProcesses,legacyNutrients,legacyNutritionChanges,legacyFoodWastes){

  }
  $scope.legacyProductFilesLoaded = function (ele) {
    console.log("legacy product file load triggered")
    var files = ele.files;
    var l = files.length;
    $scope.l=l;
    var namesArr = [];
    $scope.legacyProducts={}
    var loadFile = function(index){
      var a = new FileReader();
      a.onloadend = function () {
        try{
          newProd=angular.fromJson(a.result)
          if($scope.legacyProducts[newProd.id]==null){
            $scope.legacyProducts[newProd.id]=newProd;
          }
          else{
            console.log(newProd.id+": duplicate product id in file "+files[index].name+" and product "+$scope.legacyProducts[newProd.id].name)
          }
        }
        catch(err){
          console.log(err.message+" in file "+files[index].name)
        }
          $scope.$apply();
      }
      a.readAsText(files[index])
    }
    
    for (var i = 0; i < l; i++) {
      loadFile(i)
      console.log(JSON.stringify($scope.legacyProducts))
    }
    
  }
    $scope.legacyProcessFilesLoaded = function (ele) {
    console.log("legacy process file load triggered")
    var files = ele.files;
    var l = files.length;
    $scope.l=l;
    var namesArr = [];
    $scope.legacyProcesses={}
    var loadFile = function(index){
      var a = new FileReader();
      a.onloadend = function () {
        try{
          newProc=angular.fromJson(a.result)
          if($scope.legacyProcesses[newProc.id]==null){
            $scope.legacyProcesses[newProc.id]=newProc;
          }
          else{
            console.log(newProc.id+": duplicate product id in file "+files[index].name+" and product "+$scope.legacyProcesses[newProc.id].name)
          }
        }
        catch(err){
          console.log(err.message+" in file "+files[index].name)
        }
          $scope.$apply();
      }
      a.readAsText(files[index])
    }
    
    for (var i = 0; i < l; i++) {
      loadFile(i)
      console.log(JSON.stringify($scope.legacyProducts))
    }
    
  }
  $scope.toggleAddItemModal = function(arg){
    $scope.showProductModal=($scope.visibleClass==="Product"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    $scope.showValueModal=($scope.visibleClass==="Value"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    $scope.showReferenceModal=($scope.visibleClass==="Reference"&&!$scope.showProductModal&&!$scope.showValueModal&&!$scope.showReferenceModal);
    console.log("modal toggled")
  }
  $scope.toggleUploadModal = function(arg){
    $scope.showUploadModal=!$scope.showUploadModal
  }
  $scope.postProduct = function(arg){
    console.log("posting")
    newProduct={name:$scope.newProductName, specification:$scope.newProductSpecification}
    httpPostAsync('http://localhost:5000/products', JSON.stringify(newProduct),function(response){
      $scope.updateProducts()
      if(arg){
        item=angular.fromJson(response)
        if(item['id']!=null){
          $scope.showPopup(item['id'])
        }
      }
    })
    $scope.toggleAddItemModal()
  }
  $scope.updateProducts = function(){
    httpGetAsync('http://localhost:5000/products', function(response){
    $scope.productsFromServer=angular.fromJson(response);
    $scope.$apply();
    });
  }

  $scope.updateProducts()

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
.directive('uploadModal', function(){
  return({
    templateUrl:"snippets/uploadModal.html",
  })
})