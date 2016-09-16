// var remote = require('remote')
// var menu = remote.require('menu')
const {ipcRenderer} = require('electron')
const fs=require('fs')
const baseURL='http://localhost:5000'
const extenderSwitches=['showAllergeneExtender','showAlternativeExtender','showCoValueExtender','showDensityExtender','showEndOfLocalSeasonExtender','showFoodWasteDataExtender','showNutrientProcessExtender','showNutrientExtender','showOriginExtender','showProcessCoExtender','showStartOfLocalSeasonExtender','showSynonymsExtender','showTagsExtender','showUnitWeightExtender']
const valueTypes={ProductNutrientAssociation:{type:'ProductNutrientAssociation', extender:'nutrientExtender'},ProductAllergeneAssociation:{type:'ProductAllergeneAssociation', extender:'showAllergeneExtender'},Co2Value:{type:'Co2Value', extender:'showCoValueExtender'},FoodWasteData:{type:'FoodWasteData', extender:'foodWasteDataExtender'},ProductDensity:{type:'ProductDensity', extender:'showDensityExtender'},ProductProcessNutrientAssociation:{type:'ProductProcessNutrientAssociation', extender:'nutrientProcessExtender'},ProductProcessCO2Association:{type:'ProductProcessCO2Association', extender:'showProcessCoExtender'},ProductUnitWeight:{type:'ProductUnitWeight', extender:'showUnitWeightExtender'}}
const myStorage=localStorage;
var id = null;

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }
function httpGetSync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, false); // true for asynchronous 
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



angular.module('productFormApp', ['autocomplete'])

.controller('ProductFormController',function($scope) {

  ipcRenderer.on('prodFormId' , function(event, productId){
    id=productId

    //read pre-loaded items from browser storage
    if(myStorage.getItem("products")!=null){
      $scope.products=(angular.fromJson(myStorage.getItem("products")))
    }
    else{
      console.error("myStorage does not contain 'products': "+JSON.stringify(myStorage))
    }
    if(myStorage.getItem("references")!=null){
      $scope.references=(angular.fromJson(myStorage.getItem("references")))
    }
    else{
      console.error("myStorage does not contain 'references': "+JSON.stringify(myStorage))
    }

    //reset extenders and edit fields:
    $scope.extenderVisible=false
    for(extenderSwitch in extenderSwitches){
      $scope[extenderSwitches[extenderSwitch]]=false
    }
    $scope.newProcessName=""
    $scope.newProcessAmount=""
    $scope.newNutrientName=""
    $scope.newFoodWasteField=""
    $scope.newFoodWasteAmount=""
    init()
  });

  var init = function(){
    $scope.id=id;
    $scope.productURL=baseURL.concat('/products/'.concat(id))
    $scope.updateAllFromServer()
  }

  $scope.coValueExtract = function(product){
    if (product['co2Values']){
      if(product['co2Values'][0]){
        return product['co2Values'][0]['amount']+" "+product['co2Values'][0]['unit']
      }
    }
  }

  $scope.updateAllFromServer=function(){

    $scope.updateProductData()
    setTimeout(function(){
      $scope.updateServerNutrients()
      $scope.updateServerAllergenes()
      $scope.updateAllergeneGroups()
      $scope.updateNutrientGroups()
    },100)
  }

  $scope.updateProductData = function(){
    httpGetAsync($scope.productURL, function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.localProduct=$scope.fromServer
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

  $scope.updateServerReferences = function(){
   httpGetAsync(baseURL.concat('/references'), function(response){
    $scope.serverReferences=angular.fromJson(response)
  })
 }
 $scope.updateAllergeneGroups = function(){     
  $scope.allergenesGrouped={}
  $scope.allergeneGroupKeys=[] 
  $scope.localProduct.allergenes.forEach(function(allergene){

    var group = JSON.stringify(allergene.referenceId)||"undefined";
    if ($scope.allergenesGrouped[group]==null){
      $scope.allergenesGrouped[group]=[];
      $scope.allergeneGroupKeys.push(group)
    }
    $scope.allergenesGrouped[group].push(allergene);
    $scope.$apply()
  })
  }

  $scope.updateNutrientGroups = function(){
    $scope.nutrientsGrouped={}
    $scope.nutrientGroupKeys=[]

    $scope.localProduct.nutrients.forEach(function(nutrient){
      var group = JSON.stringify(nutrient.referenceId)||"undefined";
      if ($scope.nutrientsGrouped[group]==null){
        $scope.nutrientsGrouped[group]=[]; $scope.nutrientGroupKeys.push(group)
      }
      $scope.nutrientsGrouped[group].push(nutrient);
      $scope.$apply()
    })
  }

  $scope.updateNutrientProcessGroups = function(){
    $scope.nutrientProcessesGrouped={}
    $scope.nutrientProcessGroupedKeys=[]
    $scope.localProduct.nutrientProcesses.forEach(function(nutrient){
      var group = JSON.stringify(nutrient.referenceId)||"undefined";
      if ($scope.nutrientProcessesGrouped[group]==null){
        $scope.nutrientProcessesGrouped[group]=[]
        $scope.nutrientProcessGroupedKeys.push(group)
      }
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
    sendingData=angular.fromJson(JSON.stringify($scope.localProduct))
    httpPutAsync($scope.productURL, JSON.stringify(sendingData), function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.$apply()
      if (JSON.stringify($scope.fromServer)===JSON.stringify(sendingData)){
        console.log("put product succesfully")
      }
      else{
        console.error("server response differed from sent data")
        $scope.updateAllFromServer()
      }
    })
    $scope.$apply()
  }

  $scope.deleteValue  = function(value){
    httpDeleteAsync(baseURL.concat('/values/').concat(value.id), function(response){
      $scope.updateAllFromServer()
    })
  }

  $scope.postValue = function(value){
    httpPostAsync(baseURL.concat('/values'), JSON.stringify(value), function(response){

      $scope.updateAllFromServer()
    })
    $scope.showPostField=false
  }

  $scope.putValue = function(value){
    httpPutAsync(baseURL.concat('/values/').concat(value.id), JSON.stringify(value), function(response){
      $scope.updateAllFromServer()
      value=angular.fromJson(response)
    })
    $scope.showPostField=false
  }

  $scope.toggleGroupExtender = function(reference,editValuesType,editValues,extenderSwitch){
    extenderSwitches.forEach(function(o){
        //make sure only one extender is visible
        if(o===extenderSwitch){
          $scope[o]=true
        }
        else{
          $scope[o]=false
        }
      },extenderSwitch)
    $scope.extenderVisible=!$scope.extenderVisible||editValues!=$scope.editValues;
    $scope.editValues=editValues
    $scope.editValuesReference=reference
    $scope.editValuesType=editValuesType
  }

  $scope.toggleValueExtender = function(editValue, extenderSwitch){
    extenderSwitches.forEach(function(o){
        //make sure only one extender is visible
        if(o===extenderSwitch){
          $scope[o]=true
        }
        else{
          $scope[o]=false
        }
      },extenderSwitch)
    editValues=[editValue]
    if(editValue.derived){
      $scope.withBaseValue=true
      httpGetAsync(baseURL.concat('/values/').concat(editValue.baseValue), function(response){
        $scope.co2BaseValueProductId=angular.fromJson(response)['product']
      })
    }
    $scope.extenderVisible=!$scope.extenderVisible||JSON.stringify(editValues)!==JSON.stringify($scope.editValues);
    $scope.editValues=editValues
    $scope.editValuesType=editValue['type']
  }

  $scope.togglePostField = function(){
    $scope.showPostField=!$scope.showPostField
  }

  //store the values of the chosen product
  $scope.$watch('baseValueProductId', function() {
    if($scope.baseValueProductId===null){
      //if co2 value has base value but base value product isnt set
      if($scope.editValues[0]['baseValue']!==null){
          httpGetSync(baseURL.concat('/values/').concat($scope.editValues[0]['baseValue']), function(response){
            $scope.baseValue=angular.fromJson(response)
            $scope.baseValueProductId= $scope.baseValue['product']
        })
      }
    }
    if($scope.baseValueProductId!==null){
      httpGetAsync(baseURL.concat('/products/').concat($scope.baseValueProductId), function(response){
        $scope.baseProduct=angular.fromJson(response)
      })
    }
  })

  //delayed put of whole product
  $scope.delayedPut =function(){
    $scope.timeSinceLastChange=0
    setTimeout(function(){
      if($scope.timeSinceLastChange<1)
        $scope.putProduct()
        $scope.timeSinceLastChange++
        console.log("delayed put")
    }, 3000)
  }

  //this is triggered by the derived/not derived switch
  $scope.toggleBaseValue = function(value){

    if ($scope.baseValueBackup && $scope.withBaseValue){
      value.baseValue=$scope.baseValueBackup
    }
    else{
      $scope.baseValueBackup=value.baseValue
      delete value.baseValue
    }
    $scope.putValue(value)

  }
  $scope.$apply()
})

.controller("extenderController", function(){
})

.directive("allergeneExtender",function(){
  return({
    templateUrl:"snippets/extender/allergeneExtender.html"
  })
})

.directive("coValueExtender",function(){
  return({
    templateUrl:"snippets/extender/coValueExtender.html"
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

