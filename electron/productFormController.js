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
    xmlHttp.open("POST", theUrl, true); // true for asynchronous 
    xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    xmlHttp.send(jsonData);
  }

function ProductFormController($scope) {

  ipcRenderer.on('prodFormId' , function(event, id){
    $scope.id=id;
    $scope.productURL='http://localhost:5000/product/'.concat(id)
    httpGetAsync($scope.productURL, function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.localData=angular.fromJson(response);
      $scope.$apply();
    });
    $scope.$apply()
  });
  $scope.postData = function(){
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
  

}