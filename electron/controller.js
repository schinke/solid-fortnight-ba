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

function ContentController($scope) {
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
  httpGetAsync('http://localhost:5000/products', function(response){

  $scope.fromServer=angular.fromJson(response);
  $scope.responseRaw=response;
  $scope.parsedWJSON=JSON.parse(response);
  $scope.$apply();
  });

}