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

function ProductFormController($scope) {

  ipcRenderer.on('prodFormId' , function(event, id){
    $scope.id=id;
    $scope.postData={}
    $scope.productURL='http://localhost:5000/product/'.concat(id)
    httpGetAsync($scope.productURL, function(response){
      $scope.fromServer=angular.fromJson(response);
      $scope.$apply();
    });
    $scope.$apply()
    console.log($scope.id);
  });
  // $scope.emails = [
  //   { from: 'John', subject: 'I love angular', date: 'Jan 1' },
  //   { from: 'Jack', subject: 'Angular and I are just friends', date: 'Feb 15' },
  //   { from: 'Ember', subject: 'I hate you Angular!', date: 'Dec 8' }
  // ];
  $scope.showPopup = function(arg){
    ipcRenderer.send('show-prod-form', arg)
    console.log(arg)
  }


  var bla;
  

}