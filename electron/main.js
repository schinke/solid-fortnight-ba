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
  var mainAddr = 'http://localhost:5000/';

  let willQuitApp = false;
  app.on('before-quit', () => willQuitApp = true);

  productForm = new BrowserWindow({minWidth: 600, height:800, show:false, title:"Product details"});
  productForm.loadURL(`file://${__dirname}/views/productForm.html`)
  productForm.on('close', (e) => { //   <---- Catch close event
    if(willQuitApp){
      productForm=null
    }
    else{
      e.preventDefault();
      productForm.hide();
      console.log("productForm hidden")
    }
  });

  valueForm = new BrowserWindow({minWidth: 600, height:800, show:false, title:"Value details"});
  valueForm.loadURL(`file://${__dirname}/views/valueForm.html`)
  valueForm.on('close', (e) => { //   <---- Catch close event
    if(willQuitApp){
      valueForm=null
    }
    else{
      e.preventDefault();
      valueForm.hide();
      console.log("valueForm hidden")
    }
  });

  var openWindow = function(){
    mainWindow = new BrowserWindow({width: 1024, minWidth: 800, height: 578});
    mainWindow.loadURL(`file://${__dirname}/views/mainWindow.html`)
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

  var showProductForm = function(arg){
    productForm.webContents.openDevTools();
    console.log('sent id to window')
    //productForm.on('ready-to-show',function(){
    productForm.webContents.send('prodFormId',arg)
    productForm.show()
  }

  ipcMain.on('show-prod-form', (event, arg) => {
    showProductForm(arg);
    console.log(arg);
  })

  var showValueForm = function(arg){
    valueForm.webContents.openDevTools();
    console.log('sent id to window')
    //productForm.on('ready-to-show',function(){
    valueForm.webContents.send('valueFormId',arg)
    valueForm.show()
  }

  ipcMain.on('show-val-form', (event, arg) => {
    showValueForm(arg);
    console.log(arg);
  })
  // fire!
  startUp();
});