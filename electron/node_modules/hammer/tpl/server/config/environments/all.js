var path = require("path");
module.exports = function(app, express){
	app.set("app_root", path.join(__dirname, "../", "../", "../"));

	app.configure(function(){
		app.use(express.bodyParser());
		app.use(express.methodOverride());
		app.use(app.router);
		app.use(express.static(path.join(app.set("app_root"), "build")));
	});
};
