const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

console.log("render process started");

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}
var responseText;
httpGetAsync('http://localhost:5000', function(response){
	responseText=response;
	//document.write(responseText);
	console.log(response);
})