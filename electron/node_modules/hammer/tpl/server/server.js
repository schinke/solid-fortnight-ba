var express = require('express');
var config = require('../config');

var server;
var app = express();
var env = config.debug ? 'development' : 'production';
var port = config.site.port;
var modulePath = './lib/';

var index = require(modulePath + 'index');

app.use(index);

require('./config/environments/' + env)(app, express);
require('./config/routes')(app, express);

function startServer(){
  server = app.listen(port)
  console.log('Express server listening on port %d in %s mode', port, env);
}

function stopServer(){
  if(typeof server !== undefined){
    server.close();
    console.log('Server has been stopped!')
  }
}

exports.startServer = startServer;
exports.stopServer = stopServer;
