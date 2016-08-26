var express = require('express');
var app = module.exports = express();

app.set('views', __dirname);
app.set('view enginee', 'hbs');

app.get('/', function(req, res){
	console.log('ss');
	res.render('index.hbs');
});

