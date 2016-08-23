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

  function httpPutAsync(theUrl, jsonData, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        callback(xmlHttp.responseText);
    }
    xmlHttp.open("PUT", theUrl, true); // true for asynchronous 
    xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xmlHttp.send(jsonData);
  }
  angular.module('productFormApp', [])

  .controller('ProductFormController',function($scope) {

    ipcRenderer.on('prodFormId' , function(event, id){
      $scope.id=id;
      $scope.valueId=null
      $scope.productURL='http://localhost:5000/products/'.concat(id)
      httpGetAsync($scope.productURL, function(response){
        $scope.fromServer=angular.fromJson(response);
        $scope.localData=angular.fromJson(response);
        $scope.$apply();
      });
      $scope.$apply()
    });
    $scope.addNutrientProcess = function(){
      var newNutrientProcess={"name":$scope.newProcessName, "amount":$scope.newProcessAmount, "nutrient":$scope.newNutrientName}
      $scope.localData.nutrientProcesses.push(newNutrientProcess);
      $scope.postProduct()
      $scope.newProcessName=""
      $scope.newProcessAmount=""
      $scope.newNutrientName=""
    }
    $scope.addFoodWasteData = function(){
      var newFoodWasteData={"field":$scope.newFoodWasteField, "amount":$scope.newFoodWasteAmount}
      $scope.localData.foodWasteData.push(newFoodWasteData);
      $scope.postProduct()
      $scope.newFoodWasteField=""
      $scope.newFoodWasteAmount=""
    }
    $scope.toggleExtender = function(valueId){
      $scope.valueURL='http://localhost:5000/values/'.concat(valueId)
      $scope.extenderVisible=!$scope.extenderVisible||valueId!=$scope.valueId;
      $scope.valueId = valueId;
      console.log("show extender");
      httpGetAsync($scope.valueURL, function(response){
        $scope.valueFromServer=angular.fromJson(response)
        $scope.valueLocal=angular.fromJson(response)
        $scope.$apply()
        $scope.$apply;
      })
    };
      $scope.postProduct = function(){
        $scope.lastSentData=angular.fromJson(JSON.stringify($scope.localData))
        httpPutAsync($scope.productURL, JSON.stringify($scope.localData), function(response){
          $scope.fromServer=angular.fromJson(response);
          $scope.$apply()
          console.log(response)
          if (JSON.stringify($scope.fromServer)===JSON.stringify($scope.lastSentData)){
            console.log("updated succesfully")
          }
          else{
            console.log(JSON.stringify($scope.fromServer))
            console.log(JSON.stringify($scope.lastSentData))
          }
        })
      }
    })
      .controller("extenderController", function($scope){
        console.log("extenderController executed")


    })
.directive("extender", function(){
  return({
    templateUrl:"valueSidebar.html"
  })
})
