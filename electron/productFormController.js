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
    if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }
function httpGetSync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, false); // true for asynchronous 
    xmlHttp.send(null);
  }

  function httpDeleteAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
        callback(xmlHttp.responseText);
    }
    xmlHttp.open("DELETE", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }

  function httpPutAsync(theUrl, jsonData, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
        callback(xmlHttp.responseText);
    }
  xmlHttp.open("PUT", theUrl, true); // true for asynchronous 
  xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
  xmlHttp.send(jsonData);
}

function httpPostAsync(theUrl, jsonData, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
      callback(xmlHttp.responseText);
  }
  xmlHttp.open("POST", theUrl, true); // true for asynchronous 
  xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
  xmlHttp.send(jsonData);
}



angular.module('productFormApp', ['autocomplete'])

.controller('ProductFormController',function($scope) {
  var productURL=""
  ipcRenderer.on('prodFormId' , function(event, productId){
    id=productId

    // //read pre-loaded items from browser storage
    // if(myStorage.getItem("products")!=null){
    //   $scope.products=(angular.fromJson(myStorage.getItem("products")))
    // }
    // else{
    //   console.error("myStorage does not contain 'products': "+JSON.stringify(myStorage))
    // }
    // if(myStorage.getItem("references")!=null){
    //   $scope.references=(angular.fromJson(myStorage.getItem("references")))
    // }
    // else{
    //   console.error("myStorage does not contain 'references': "+JSON.stringify(myStorage))
    // }

    //reset extenders and edit-fields:
    $scope.extenderVisible=false
    for(extenderSwitch in extenderSwitches){
      $scope[extenderSwitches[extenderSwitch]]=false
    }
    $scope.newProcessName=""
    $scope.newProcessAmount=""
    $scope.newNutrientName=""
    $scope.newFoodWasteField=""
    $scope.newFoodWasteAmount=""

    // fill the form
    init()
  });

  var init = function(){
    $scope.id=id;
    productURL=baseURL.concat('/products/'.concat(id))
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
    console.log("update all from server")
    updateProductData(function(){
      updateServerNutrients()
      updateNutrientGroups()
      updateCo2Values()
      updateServerReferences()
      updateServerProducts()
    })
  }

  updateProductData = function(callback){
    httpGetAsync(productURL, function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.localProduct=$scope.fromServer
      callback()
      $scope.$apply()
    })
  }

  updateCo2Values = function(){
    $scope.co2Values=$scope.localProduct.co2Values
    $scope.$apply()
  }
    
  updateServerNutrients = function(){
    httpGetAsync(baseURL.concat('/nutrients'), function(response){
      $scope.serverNutrients=angular.fromJson(response)
      $scope.$apply()
    })
  }

  updateServerReferences = function(){
    httpGetAsync(baseURL.concat('/references?fields=name,comment'), function(response){
      $scope.serverReferences=angular.fromJson(response)
      $scope.$apply()
    })
  }

  updateServerProducts = function(){
    console.log("attempting product list update")
    httpGetAsync(baseURL.concat("/products?fields=name,id,specification"), function(response){
      $scope.serverProducts=angular.fromJson(response);
      $scope.$apply()
    });
  }

  updateNutrientGroups = function(){
    console.log("update nutrient groups")
    $scope.nutrientsGrouped={}
    $scope.nutrientGroupKeys=[]
    $scope.localProduct.nutrients.forEach(function(nutrient){
      var group = JSON.stringify(nutrient.referenceId)||"undefined";
      if ($scope.nutrientsGrouped[group]==null){
        $scope.nutrientsGrouped[group]=[]; $scope.nutrientGroupKeys.push(group)
      }
      $scope.nutrientsGrouped[group].push(nutrient);
    })
    $scope.$apply()
  }

  updateNutrientProcessGroups = function(){
    $scope.nutrientProcessesGrouped={}
    $scope.nutrientProcessGroupedKeys=[]
    $scope.localProduct.nutrientProcesses.forEach(function(nutrient){
    })
  }

  //to save text data of the product
  $scope.putProduct = function(){
    sendingData=angular.fromJson(JSON.stringify($scope.localProduct))
    httpPutAsync(productURL, JSON.stringify(sendingData), function(response){
      $scope.productMustBePut=false
      $scope.updateAllFromServer()
    })
    $scope.$apply()
  }

  $scope.deleteValue  = function(value){
    httpDeleteAsync(baseURL.concat('/values/').concat(value.id), function(response){
      $scope.updateAllFromServer()
      try{
        index = $scope.editValues.indexOf(value)
        if(index>=0){
          $scope.editValues.splice(index,1)
        }
      }catch(err){

      }
    })
  }

  $scope.deleteValues = function(values){
    for(valueIndex in values){
      $scope.deleteValue(values[valueIndex])
    }

  }

  $scope.postValue = function(value,editValues){
    console.log("attempting to post value")
    httpPostAsync(baseURL.concat('/values'), JSON.stringify(value), function(response){
      $scope.updateAllFromServer()
      $scope.editValues.push(angular.fromJson(response))
      console.log($scope.editValues)
      $scope.$apply()
      

    })
    $scope.showPostField=false

  }

  $scope.putValue = function(value,update){
    httpPutAsync(baseURL.concat('/values/').concat(value.id), JSON.stringify(value), function(response){
      if (update==null || update==true){
        $scope.updateAllFromServer()
      }
      value=angular.fromJson(response)
    })
    $scope.showPostField=false
  }

  //opens valueExtender after posting a new value of type

  $scope.addValue = function(type){
    var newVal={product:$scope.localProduct.id, type:type}
    httpPostAsync(baseURL.concat('/values'),JSON.stringify(newVal),function(response){
      console.log(response)
      var serverVal=angular.fromJson(response)
      $scope.toggleValueExtender(serverVal,valueTypes[serverVal.type].extender)
      $scope.updateAllFromServer()
    })
  }

  $scope.toggleGroupExtender = function(map,groupKey,extenderSwitch){
    extenderSwitches.forEach(function(o){
        //make sure only one extender is visible
        if(o===extenderSwitch){
          $scope[o]=true
        }
        else{
          $scope[o]=false
        }
      },extenderSwitch)

      editValues=map[groupKey]
      //open extender or close if same value as before
      $scope.extenderVisible=!$scope.extenderVisible||editValues!=$scope.editValues;

      //set refernce and valid countries the same for whole group
      editValuesType=editValues[0].type
      reference=editValues[0].reference
      $scope.editValues=editValues
      $scope.editValuesCountries=angular.fromJson(JSON.stringify(editValues[0].validCountries))
      for (valueIndex in editValues){
        editValues[valueIndex].validCountries=$scope.editValuesCountries
      }
      $scope.editValuesReference=reference
      $scope.editValuesType=editValuesType
  }

  //toggles the field in group extender to add another value
  $scope.togglePostField = function(){
    $scope.showPostField=!$scope.showPostField
  }


  $scope.toggleValueExtender = function(editValue, extenderSwitch){
    console.log("toggledValueExtender")
    console.log(JSON.stringify($scope.editValues))
    extenderSwitches.forEach(function(o){
        //make sure only one extender is visible
        if(o===extenderSwitch){
          $scope[o]=true
        }
        else{
          $scope[o]=false
        }
      },extenderSwitch)
    delete editValue.referenceId
    editValues=[editValue]
    if(editValue.derived){
      $scope.withBaseValue=true
      //get baseValue from server
      httpGetAsync(baseURL.concat('/values/').concat(editValue.baseValue), function(response){
        $scope.co2BaseValueProductId=angular.fromJson(response)['product']
      })
    }
    else{
      $scope.withBaseValue=false
    }
    $scope.extenderVisible=!$scope.extenderVisible||JSON.stringify(editValues)!==JSON.stringify($scope.editValues)
    console.log($scope.extenderVisible)
    $scope.editValues=editValues
    $scope.editValuesType=editValue['type']
    $scope.baseValueBackup=null
  }

  //to delete the value in ValueExtender
  $scope.deleteSingleValue =function(){
    $scope.toggleValueExtender(editValues[0],"none")
    $scope.deleteValue(editValues[0])
  }

  //store the values of the chosen baseValueProduct
  $scope.$watch('baseValueProductId', function() {
    if($scope.baseValueProductId===undefined){
      //if co2 value has base value but base value product isnt set
      if($scope.editValues[0]['baseValue']!==null){
          httpGetSync(baseURL.concat('/values/').concat($scope.editValues[0]['baseValue']), function(response){
            $scope.baseValue=angular.fromJson(response)
            $scope.baseValueProductId= $scope.baseValue['product']
        })
      }
    }
    if($scope.baseValueProductId!==undefined){
      httpGetAsync(baseURL.concat('/products/').concat($scope.baseValueProductId), function(response){
        $scope.baseProduct=angular.fromJson(response)
        $scope.baseProcuctCo2Values=$scope.baseProduct.co2Values
        console.log("co2Values of baseProduct: "+JSON.stringify($scope.baseProcuctCo2Values))
        $scope.$apply()
      })
    }
  })

  $scope.addCountryToEditValues = function(newCountry){
    if ($scope.editValuesCountries.indexOf(newCountry)>=0){
    }
    else{
      $scope.editValuesCountries.push(newCountry)
      for(valueIndex in editValues){
        $scope.putValue(editValues[valueIndex],false)
      }
      $scope.updateAllFromServer()
      newCountry=""
    }
  }

  $scope.deleteCountryFromEditValues = function(country){
    $scope.editValuesCountries.splice($scope.editValuesCountries.indexOf(country),1)
    for(valueIndex in editValues){
      $scope.putValue(editValues[valueIndex],false)
    }
    $scope.updateAllFromServer()
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
.directive("nutrientProcessExtender",function(){
  return({
    templateUrl:"snippets/extender/nutrientProcessExtender.html"
  })
})

.directive("extender", function(){
  return({
    templateUrl:"snippets/extender.html"
  })
})

