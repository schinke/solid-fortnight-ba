// var remote = require('remote')
// var menu = remote.require('menu')
const {ipcRenderer} = require('electron')
const fs=require('fs')
const baseURL='http://localhost:5000'
const extenderSwitches=['showAllergeneExtender','showAlternativeExtender','showCoValueExtender','showDensityExtender','showEndOfLocalSeasonExtender','showFoodWasteDataExtender','showNutrientProcessExtender','showNutrientExtender','showOriginExtender','showProcessCoExtender','showStartOfLocalSeasonExtender','showSynonymsExtender','showTagsExtender','showUnitWeightExtender']
const valueTypes={ProductNutrientAssociation:{type:'ProductNutrientAssociation', extender:'nutrientExtender'},ProductAllergeneAssociation:{type:'ProductAllergeneAssociation', extender:'showAllergeneExtender'},Co2Value:{type:'Co2Value', extender:'showCoValueExtender'},FoodWasteData:{type:'FoodWasteData', extender:'foodWasteDataExtender'},ProductDensity:{type:'ProductDensity', extender:'showDensityExtender'},ProductProcessNutrientAssociation:{type:'ProductProcessNutrientAssociation', extender:'nutrientProcessExtender'},ProductProcessCO2Association:{type:'ProductProcessCO2Association', extender:'showProcessCoExtender'},ProductUnitWeight:{type:'ProductUnitWeight', extender:'showUnitWeightExtender'}}

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function httpDeleteAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("DELETE", theUrl, true); // true for asynchronous 
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

angular.module('productFormApp', [])

.controller('ProductFormController',function($scope) {

  ipcRenderer.on('prodFormId' , function(event, id){
    $scope.id=id;
    $scope.valueId=null
    $scope.productURL=baseURL.concat('/products/'.concat(id))
    // store product in scope
    $scope.updateAllFromServer()

    })

$scope.updateAllFromServer=function(){
      httpGetAsync($scope.productURL, function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.localProduct=$scope.fromServer
      $scope.updateAllergeneGroups()
      $scope.updateNutrientGroups()
      $scope.updateServerNutrients()
      $scope.updateServerAllergenes()
      $scope.$apply()

    })
}

$scope.updateServerNutrients = function(){
  httpGetAsync(baseURL.concat('/nutrients'), function(response){
    $scope.serverNutrients=angular.fromJson(response)
  })
}

$scope.updateServerAllergenes = function(){
  httpGetAsync(baseURL.concat('/allergenes'), function(response){
    $scope.serverAllergenes=angular.fromJson(response)
  })
}

$scope.updateAllergeneGroups = function(){     
  $scope.allergenesGrouped={}
  $scope.allergeneGroupKeys=[] 
  $scope.localProduct.allergenes.forEach(function(allergene){
    
    var group = JSON.stringify(allergene.referenceId)||"undefined";
    if ($scope.allergenesGrouped[group]==null){$scope.allergenesGrouped[group]=[]; console.log("found new group:"+group); $scope.allergeneGroupKeys.push(group); console.log($scope.allergeneGroupKeys)}
    $scope.allergenesGrouped[group].push(allergene);
    $scope.$apply()
  })
}


$scope.updateNutrientGroups = function(){
  $scope.nutrientsGrouped={}
  $scope.nutrientGroupKeys=[]

  $scope.localProduct.nutrients.forEach(function(nutrient){
    var group = JSON.stringify(nutrient.referenceId)||"undefined";
    if ($scope.nutrientsGrouped[group]==null){$scope.nutrientsGrouped[group]=[]; console.log("found new group:"+group); $scope.nutrientGroupKeys.push(group); console.log($scope.nutrientGroupKeys)}
    $scope.nutrientsGrouped[group].push(nutrient);
    $scope.$apply()
  })
}

$scope.updateNutrientProcessGroups = function(){
  $scope.nutrientProcessesGrouped={}
  $scope.nutrientProcessGroupedKeys=[]
    $scope.localProduct.nutrientProcesses.forEach(function(nutrient){
    var group = JSON.stringify(nutrient.referenceId)||"undefined";
    if ($scope.nutrientProcessesGrouped[group]==null){$scope.nutrientProcessesGrouped[group]=[]; console.log("found new group:"+group); $scope.nutrientProcessGroupedKeys.push(group); console.log($scope.nutrientProcessGroupedKeys)}
    $scope.nutrientProcessesGrouped[group].push(nutrient);
    $scope.$apply()
  })
}

$scope.addNutrientProcess = function(){
  var newNutrientProcess={"name":$scope.newProcessName, "amount":$scope.newProcessAmount, "nutrient":$scope.newNutrientName}
  $scope.localProduct.nutrientProcesses.push(newNutrientProcess);
  $scope.putProduct()()
  $scope.newProcessName=""
  $scope.newProcessAmount=""
  $scope.newNutrientName=""
}

$scope.addFoodWasteData = function(){
  var newFoodWasteData={"field":$scope.newFoodWasteField, "amount":$scope.newFoodWasteAmount}
  $scope.localProduct.foodWasteData.push(newFoodWasteData);
  $scope.putProduct()()
  $scope.newFoodWasteField=""
  $scope.newFoodWasteAmount=""
}

$scope.putProduct = function(){
  $scope.lastSentData=angular.fromJson(JSON.stringify($scope.localProduct))
  httpPutAsync($scope.productURL, JSON.stringify($scope.localProduct), function(response){
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

$scope.deleteValue  = function(value){
  console.log("attempting to post value: "+JSON.stringify(value))
  httpDeleteAsync(baseURL.concat('/values/').concat(value.id), function(response){
    console.log("postValueRespone: "+response)
    $scope.updateAllFromServer()
  })
}

$scope.postValue = function(value){
  console.log("attempting to post value: "+JSON.stringify(value))
  httpPostAsync(baseURL.concat('/values'), JSON.stringify(value), function(response){
    console.log("postValueRespone: "+response)
    $scope.updateAllFromServer()
  })
}


$scope.toggleExtender = function(values, extenderSwitch){
  extenderSwitches.forEach(function(o){
    //make sure only one extender is visible
    if(o===extenderSwitch){
      $scope[o]=true
    }
    else{
      $scope[o]=false
    }
  },extenderSwitch)
  $scope.extenderVisible=!$scope.extenderVisible||values!=$scope.editValues;
  $scope.editValues=values
  
  console.log("show extender");
}

$scope.togglePostField = function(){
  $scope.showPostField=!$scope.showPostField
  console.log("toggled PostField")
}
})

.controller("extenderController", function($scope){
  console.log("extenderController executed")


})
.directive("allergeneExtender",function(){
  return({
    templateUrl:"snippets/extender/allergeneExtender.html"
  })
})
.directive("nutrientExtender",function(){
  return({
    templateUrl:"snippets/extender/nutrientExtender.html"
  })
})
.directive("extender", function(){
  return({
    templateUrl:"valueSidebar.html"
  })
})
