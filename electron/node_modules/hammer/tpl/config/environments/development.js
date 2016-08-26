module.exports = function(app, express){
  //Load the common configuration
  require("./all")(app, express);

  app.configure("development", function(){
      app.use(express.logger());
      app.use(express.errorHandler({ dumpException: true, showStack: true}));
  });
};