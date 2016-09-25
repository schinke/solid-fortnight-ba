// var remote = require('remote')
// var menu = remote.require('menu')
const {ipcRenderer} = require('electron')
const baseURL = 'http://localhost:5000'
const debug=false
const myStorage=localStorage;
const path=require("path")
const fs=require("fs")
const legacyImporter=require("../legacyImporter")
const backUpService=require("../backUpService")
var exportPath=path.join(__dirname,"..","..","export")


function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }

  function httpPostSync(theUrl, jsonData, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status >= 200 && xmlHttp.status<=300)
        callback(xmlHttp.responseText);
    }
  xmlHttp.open("POST", theUrl, false); // true for asynchronous 
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

angular.module('mainWindowApp', [])
.controller('MainWindowController', function($scope) {
  $scope.visibleClass='Product' // set the default table
  $scope.productSortField     = 'id'; // set the default product sort type
  $scope.productSortField     = 'id'; // set the default product sort type
  $scope.productSortReverse  = false;  // set the default sort order
  $scope.searchTerm   = '';

  $scope.convertLegacy = legacyImporter.convertLegacy

  $scope.showPopup = function(arg){
    ipcRenderer.send('show-prod-form', arg)
    console.log(arg)
  }
  $scope.dumpJson = backUpService.dumpJson

  //take files from html element and read them into scope's legacyNutritionChanges
  $scope.legacyNutritionChangeFilesLoaded = function (ele) {
    if(debug==true){
      console.log("legacy nutrient change data file load triggered")
    }
    var files = ele.files;
    var l = files.length;
    $scope.l=l;
    var namesArr = [];
    $scope.legacyNutritionChanges={}
    var loadFile = function(index){
      var a = new FileReader();
      a.onloadend = function () {
        try{
          newNutrChange=angular.fromJson(a.result)
          if($scope.legacyNutritionChanges[newNutrChange.id]==null){
            $scope.legacyNutritionChanges[newNutrChange.id]=newNutrChange;
          }
          else{
            console.log(newNutrChange.id+": duplicate product id in file "+files[index].name+" and product "+$scope.legacyNutritionChanges[newNutrChange.id].name)
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
      console.log(JSON.stringify($scope.legacyNutritionChanges))
    }
    $scope.legacyNutritionChangesReady=true
    console.log("done with local legacy import")
    $scope.$apply()
  }

  //take files from html element and read them into scope's legacyNutrients
  $scope.legacyNutrientFilesLoaded = function (ele) {
    console.log("legacy nutrient data file load triggered")
    var files = ele.files;
    var l = files.length;
    $scope.l=l;
    var namesArr = [];
    $scope.legacyNutrients={}
    var loadFile = function(index){
      var a = new FileReader();
      a.onloadend = function () {
        try{
          newNutr=angular.fromJson(a.result)
          if($scope.legacyNutrients[newNutr.id]==null){
            $scope.legacyNutrients[newNutr.id]=newNutr;
          }
          else{
            console.log(newNutr.id+": duplicate product id in file "+files[index].name+" and product "+$scope.legacyNutrients[newNutr.id].name)
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
      console.log(JSON.stringify($scope.legacyNutrients))
    }
    $scope.legacyNutrientsReady=true

    console.log("done with local legacy import")
    $scope.$apply()
  }

  //take files from html element and read them into scope's legacyProcesses
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
      console.log(JSON.stringify($scope.legacyProcesses))
    }
    $scope.legacyProcessesReady=true
    console.log("done with local legacy import")
    $scope.$apply()
  }

  //take files from html element and read them into scope's legacyProducts
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
    $scope.legacyProductsReady=true
    console.log("done with local legacy import")
    $scope.$apply()
  }

  //take files from html element and read them into scope's legacyFoodWastes
  $scope.legacyFoodWasteFilesLoaded = function (ele) {
    console.log("legacy food waste data file load triggered")
    var files = ele.files;
    var l = files.length;
    $scope.l=l;
    var namesArr = [];
    $scope.legacyFoodWastes={}
    var loadFile = function(index){
      var a = new FileReader();
      a.onloadend = function () {
        try{
          newFoodWaste=angular.fromJson(a.result)
          if($scope.legacyFoodWastes[newFoodWaste.id]==null){
            $scope.legacyFoodWastes[newFoodWaste.id]=newFoodWaste;
          }
          else{
            console.log(newFoodWaste.id+": duplicate product id in file "+files[index].name+" and product "+$scope.legacyFoodWastes[newFoodWaste.id].name)
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
      console.log(JSON.stringify($scope.legacyFoodWastes))
    }
    $scope.legacyFoodWastesReady=true
    console.log("done with local legacy import")
    $scope.$apply()
  }

  //this either enables one of the scope's show-X-Modal or disables them all
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
    var newProduct={name:$scope.newProductName, specification:$scope.newProductSpecification}
    httpPostAsync('http://localhost:5000/products', JSON.stringify(newProduct),function(response){
      console.log("response")
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
    console.log("attempting product list update")
    httpGetAsync(baseURL.concat("/products?fields=name,id,specification"), function(response){
      $scope.productsFromServer=angular.fromJson(response);
      myStorage.setItem("products",JSON.stringify($scope.productsFromServer))
      if(debug){
        console.log("storage: "+JSON.stringify(myStorage.getItem("products")))
      }
      $scope.$apply();
    });
  }

  $scope.updateProducts()


  $scope.updateReferences = function(){
    console.log("attempting reference list update")
    httpGetAsync('http://localhost:5000/references?fields=name,comment', function(response){
      $scope.referencesFromServer=angular.fromJson(response);
      myStorage.setItem("references",JSON.stringify($scope.referencesFromServer))
      if(debug){
       console.log("storage: "+JSON.stringify(myStorage.getItem("references")))
     }
      $scope.$apply();
    });
  }
  $scope.updateReferences()
})

.controller('ProductModalController', function($scope){
})

.directive('addProductModal', function(){
  return({
    templateUrl:"snippets/addProductModal.html",
  })
})
.directive(('uploadModal'), function(){
  return({
    templateUrl:"snippets/uploadModal.html"
  })
})