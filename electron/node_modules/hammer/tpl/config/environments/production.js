module.exports = function(app, express){
  //Load the common configuration
  require("./all")(app, express);

  app.configure("production", function(){
    app.use(express.errorHandler());
  });
};