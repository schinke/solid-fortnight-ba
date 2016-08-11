const electron = require('electron');
const {ipcMain}=require('electron')
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;


var mainWindow = null;

app.on('window-all-closed', function() {
  //if (process.platform != 'darwin') {
    app.quit();
  //}
});

app.on('ready', function() {
  // call python to start server
  var subpy = require('child_process').spawn('./../flask/venv/bin/python', ['../flask/app.py']);
  var rq = require('request-promise');
  var mainAddr = 'http://localhost:5000/products';

  var openWindow = function(){
    mainWindow = new BrowserWindow({width: 1024, height: 578});
    mainWindow.loadURL(`file://${__dirname}/views/viewproducts.html`)
    mainWindow.webContents.openDevTools();
    mainWindow.on('closed', function() {
      mainWindow = null;
      subpy.kill('SIGINT');
      app.quit();
    });
  };

  var startUp = function(){
    rq(mainAddr)
      .then(function(htmlString){
        console.log('server started!');
        openWindow();
      })
      .catch(function(err){
        console.log('waiting for the server start...');
        console.log(err);
        startUp();
      });

  };

  var openProductForm = function(arg){
    productForm = new BrowserWindow({width: 600, height:400, show:false});
    productForm.loadURL(`file://${__dirname}/views/productForm.html`)
    // productForm.webContents.openDevTools();
    console.log('sent id to window')
    productForm.on('ready-to-show',function(){
      productForm.webContents.send('id',arg)
      productForm.show()
    })
    productForm.on('closed', function() {
      productForm = null;
    });
  }
  ipcMain.on('show-prod-form', (evenet, arg) => {
    openProductForm(arg);
    console.log(arg);
  })
  // fire!
  startUp();
});