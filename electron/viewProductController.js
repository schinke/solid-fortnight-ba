// var remote = require('remote')
// var menu = remote.require('menu')
const {ipcRenderer} = require('electron')
const baseURL = 'http://localhost:5000'
const debug=false
const myStorage=localStorage;
const path=require("path")
const fs=require("fs")
var exportPath=path.join(__dirname,"..","..","export")


function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
  }

  function httpPostSync(theUrl, jsonData, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        callback(xmlHttp.responseText);
    }
  xmlHttp.open("POST", theUrl, false); // true for asynchronous 
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
  $scope.dumpJson =function(){
    try{
      fs.mkdirSync(exportPath)
    }
    catch(err){
      console.error(err.message)
    }
    console.log("attempting JSON dump")
    httpGetAsync(baseURL.concat("/products"),function(response){
      var products=angular.fromJson(response)
      for(i in products){
        (function(productIndex){
          var product=products[productIndex]
          var fileName=String(product.id).concat(product.name).concat(".json")
          var absFileName=path.normalize(path.join(exportPath,fileName))
          fs.exists(absFileName, function(exists) {
            if (exists) {
              fs.stat(absFileName, function(error, stats) {
                fs.open(absFileName, "r", function(error, fd) {
                  var buffer = new Buffer(stats.size);

                  fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                    var data = buffer.toString("utf8", 0, buffer.length);

                    console.log(data);
                    fs.close(fd);
                  });
                });
              });
            }
            else{
              fs.writeFile(absFileName, JSON.stringify(product))
              console.log("wrote file: "+absFileName)
            }
          });
        })(i)
      }
    })
  }
  //generate and post data from loaded legacy data
  $scope.convertLegacy = function(legacyProducts,legacyProcesses,legacyNutrients,legacyNutritionChanges,legacyFoodWastes){
    // Post all products and store their new representation
    var prodsToPost=[]
    var referencesToPost=[]
    var productNutrientAssociationsToPost=[]
    var productAllergeneAssociationsToPost=[]
    var co2ValuesToPost=[]
    var co2ValuesLinkedToPost=[]
    var foodWasteDatasToPost=[]
    var productDensitiesToPost=[]
    var productProcessNutrientAssociationsToPost=[]
    var productProcessCO2AssociationsToPost=[]
    var productUnitWeightsToPost=[]

    for (nutrientDataId in legacyNutrients){
      nutrientDataSet=legacyNutrients[nutrientDataId]
    }

    for (productId in legacyProducts){
      try{
        var legacyProduct=legacyProducts[productId]
        var allergenes=[]
        var alternatives=[]
        var prodToPost={
          "allergenes": [],
          "alternatives": [],
          "co2Values": [],
          "commentsOnDensityAndUnitWeight": legacyProduct["quantity-comments"],
          "densities": [],
          "edb": true,
          "endOfLocalSeason": "None",
          "englishName": legacyProduct["name-english"],
          "foodWasteData": [],
          "frenchName": legacyProduct["name-french"],
          "id": legacyProduct.id,
          "infoTextForCook": legacyProduct["info-text"],
          "name": legacyProduct.name,
          "nutrientProcesses": [],
          "nutrients": [],
          "possibleOrigins": [],
          "processesCo2": [],
          "specification": legacyProduct["specification"],
          "startOfLocalSeason": "None",
          "synonyms": [],
          "tags": [],
          "texture": null,
          "unitWeights": []
        }

        // store for later use
        prodsToPost.push(prodToPost)
        legacyProduct['prodToPost']=prodToPost

        // post this product, sync to make sure the server is not overwhelmed:
        httpPostSync(baseURL+'/products', JSON.stringify(prodToPost),function(response){
          if(debug==true){
            console.log("posted product: "+JSON.stringify(prodToPost))
            console.log("response: "+response)
          }
          prodToPost['newProd']=angular.fromJson(response)
        })

        //convert nutrition data set to values
        if(legacyProduct['nutrition-id']){
          nutritionData=legacyNutrients[legacyProduct['nutrition-id']]

          referenceToPost={
            name: "Euro4 "+nutritionData['id']+" "+nutritionData['name'],
            comment: "generated at legacy import"
          }
          // check if there is a reference for this file
          if(nutritionData['referencesToPost']==null){
            nutritionData['referencesToPost']=[]
            nutritionData['referencesToPost'].push(referenceToPost)
            referencesToPost.push(referenceToPost)

            // post reference to server
            httpPostSync(baseURL+'/references',JSON.stringify(referenceToPost),function(response){
              if(debug==true){
                console.log("posted reference: "+JSON.stringify(referenceToPost))
                console.log("response: "+response)
              }
            })
          }

          for(counter in nutritionData['nutr-vals']){
            val=nutritionData['nutr-vals'][counter]
            productNutrientAssociationToPost={
              type:"ProductNutrientAssociation",
              reference:referenceToPost.name,
              nutrientName:val['component-id'],
              amount:val.value,
              unit:val.unit,
              validCountries:[val.country],
              product:prodToPost['newProd']['id']
            }

            // store for later use
            if(nutritionData['productNutrientAssociationsToPost']==null){
              nutritionData['productNutrientAssociationsToPost']=[]
            }
            nutritionData['productNutrientAssociationsToPost'].push(productNutrientAssociationToPost)
            productNutrientAssociationsToPost.push(productNutrientAssociationToPost)

            // post Product Nutrient Association to server
            httpPostSync(baseURL+'/values',JSON.stringify(productNutrientAssociationToPost),function(response){
              if(debug==true){
                console.log("posted productNutrientAssociation: "+JSON.stringify(productNutrientAssociationToPost))
                console.log("response: "+response)
              }
              productNutrientAssociationToPost['newValue']=angular.fromJson(response)
            })
          }


          co2ValueToPost={
            type:"Co2Value",
            product:prodToPost['newProd']['id'],
            amount:legacyProduct['co2-value']||null,
            unit:"kg CO2 Äq/kg",
            referenceName:legacyProduct['references'],
            comment:"co2-calculation: ".concat(legacyProduct['co2-calculation']||"-").concat(" calculation-process-documentation: ").concat(legacyProduct['calculation-process-documentation']||"-")
          }
        // store for later use
        legacyProduct['co2ValueToPost']=co2ValueToPost

        //products with only basic co2 value get their value put immediately
        if(legacyProduct['linked-id']==null){
          httpPostSync(baseURL+'/values',JSON.stringify(co2ValueToPost),function(response){
            if(debug==true){
              console.log("posted Co2Value: "+JSON.stringify(co2ValueToPost))
              console.log("response: "+response)
            }co2ValueToPost['newValue']=angular.fromJson(response)
          })
        }

        // products with linked co2 value are stored, so they can later be linked and put
        else{
          //store the old id of the base value product
          co2ValueToPost['legacyBaseValueId']=legacyProduct['linked-id']
          co2ValuesLinkedToPost.push(co2ValueToPost)
          if(debug==true){
            console.log("linked co2-value detected. Id: "+legacyProduct['id'])
          }
        }
      }
    }
    catch(err){
      console.error(err.message+" for product: "+productId)
    }
  }

  // link and post linked co2Values
  for(counter in co2ValuesLinkedToPost){
    co2ValueLinkedToPost=co2ValuesLinkedToPost[counter]
    baseProduct=legacyProducts[co2ValueLinkedToPost['legacyBaseValueId']]
    try{
      co2ValueLinkedToPost['baseValue']=baseProduct['co2ValueToPost']['newValue']['id']
      httpPostSync(baseURL+'/values',JSON.stringify(co2ValueLinkedToPost),function(response){
              if(debug==true){
                console.log("posted Co2Value: "+JSON.stringify(co2ValueLinkedToPost))
                console.log("response: "+response)
              }co2ValueLinkedToPost['newValue']=angular.fromJson(response)
            })
    }
    catch(err){
      console.error(JSON.stringify(baseProduct))
      console.error(err)
    }
    console.log("linked co2 counter: "+counter)
  }
}

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
    newProduct={name:$scope.newProductName, specification:$scope.newProductSpecification}
    httpPostSync('http://localhost:5000/products', JSON.stringify(newProduct),function(response){
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
    httpGetAsync('http://localhost:5000/references', function(response){
      $scope.referencesFromServer=angular.fromJson(response);
      myStorage.setItem("references",JSON.stringify($scope.referencesFromServer))
      if(debug){
       console.log("storage: "+JSON.stringify(myStorage.getItem("references")))
     }
      $scope.$apply();
    });
  }
  $scope.dumpJson()
  $scope.updateReferences()
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