module.exports = {
  dumpJson : function(){
    var logFileName
    var createExportFolder = function(index){
      try{
        var tryPath=exportPath.concat(index)
        fs.mkdirSync(tryPath)
        exportPath=tryPath;
        logFileName=path.normalize(path.join(exportPath,"log.txt"))
        fs.writeFile(logFileName, "new log file \n")
      }
      catch(err){
        console.error(err.message)
        if(index<100){
          createExportFolder(index+1)
        }
        else{
          throw("100 export folders: maximum reached")}
      }
    }
    createExportFolder(0)
    var subDirectories=["processes", "allergenes", "nutrients", "references", "products"]
    for(index in subDirectories){
      try{
        fs.mkdirSync(path.join(exportPath,subDirectories[index]))
      }
      catch(err){

      }
    }
    console.log("attempting JSON dump")
    // download and save products
    httpGetAsync(baseURL.concat("/products"),function(response){
      var products=angular.fromJson(response)
      for(i in products){
        try{
          (function(productIndex){
            var product=products[productIndex]
            var fileName=String(product.id).concat(product.name).concat(".json")
            var absFileName=path.normalize(path.join(exportPath,"products",fileName.replace(/\//g,"_")))
            fs.exists(absFileName, function(exists) {
              if (exists) {
                fs.stat(absFileName, function(error, stats) {
                  fs.open(absFileName, "r", function(error, fd) {
                    var buffer = new Buffer(stats.size);

                    fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                      var data = buffer.toString("utf8", 0, buffer.length);

                      console.log(data);
                      fs.close(fd);
                    });
                  });
                });
              }
              else{
                fs.writeFile(absFileName, JSON.stringify(product))
                console.log("wrote file: "+absFileName)
              }
            });
          })(i)
        }
        catch(err){
          fs.appendFile(logFileName,err)
        }
      }
    })
    // download and save references
    httpGetAsync(baseURL.concat("/references"),function(response){
      var references=angular.fromJson(response)
      for(i in references){
        try{
          (function(productIndex){
            var reference=references[productIndex]
            var fileName=String(reference.id).concat(reference.name).concat(".json")
            var absFileName=path.normalize(path.join(exportPath,"references",fileName.replace(/\//g,"_")))
            fs.exists(absFileName, function(exists) {
              if (exists) {
                fs.stat(absFileName, function(error, stats) {
                  fs.open(absFileName, "r", function(error, fd) {
                    var buffer = new Buffer(stats.size);

                    fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                      var data = buffer.toString("utf8", 0, buffer.length);

                      console.log(data);
                      fs.close(fd);
                    });
                  });
                });
              }
              else{
                fs.writeFile(absFileName, JSON.stringify(reference))
                console.log("wrote file: "+absFileName)
              }
            });
          })(i)
        }
        catch(err){
          fs.appendFile(logFileName,err)
        }
      }
    })

    // download and save nutrients
    httpGetAsync(baseURL.concat("/nutrients"),function(response){
      var nutrients=angular.fromJson(response)
      for(i in nutrients){
        try{
          (function(productIndex){
            var nutrient=nutrients[productIndex]
            var fileName=String(nutrient.id).concat(nutrient.name).concat(".json")
            var absFileName=path.normalize(path.join(exportPath,"nutrients",fileName.replace(/\//g,"_")))
            fs.exists(absFileName, function(exists) {
              if (exists) {
                fs.stat(absFileName, function(error, stats) {
                  fs.open(absFileName, "r", function(error, fd) {
                    var buffer = new Buffer(stats.size);

                    fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                      var data = buffer.toString("utf8", 0, buffer.length);

                      console.log(data);
                      fs.close(fd);
                    });
                  });
                });
              }
              else{
                fs.writeFile(absFileName, JSON.stringify(nutrient))
                console.log("wrote file: "+absFileName)
              }
            });
          })(i)
        }
        catch(err){
          fs.appendFile(logFileName,err)
        }
      }
    })
    // download and save allergenes
    httpGetAsync(baseURL.concat("/allergenes"),function(response){
      var allergenes=angular.fromJson(response)
      for(i in allergenes){
        try{
          (function(productIndex){
            var allergene=allergenes[productIndex]
            var fileName=String(allergene.id).concat(allergene.name).concat(".json")
            var absFileName=path.normalize(path.join(exportPath,"allergenes",fileName.replace(/\//g,"_")))
            fs.exists(absFileName, function(exists) {
              if (exists) {
                fs.stat(absFileName, function(error, stats) {
                  fs.open(absFileName, "r", function(error, fd) {
                    var buffer = new Buffer(stats.size);

                    fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                      var data = buffer.toString("utf8", 0, buffer.length);

                      console.log(data);
                      fs.close(fd);
                    });
                  });
                });
              }
              else{
                fs.writeFile(absFileName, JSON.stringify(allergene))
                console.log("wrote file: "+absFileName)
              }
            });
          })(i)
        }
        catch(err){
          fs.appendFile(logFileName,err)
        }
      }
    })

    // download and save processes
    httpGetAsync(baseURL.concat("/processes"),function(response){
      var allergenes=angular.fromJson(response)
      for(i in allergenes){
        (function(productIndex){
          var allergene=allergenes[productIndex]
          var fileName=String(allergene.id).concat(allergene.name).concat(".json")
          var absFileName=path.normalize(path.join(exportPath,"allergenes",fileName.replace(/\//g,"_")))
          fs.exists(absFileName, function(exists) {
            if (exists) {
              fs.stat(absFileName, function(error, stats) {
                fs.open(absFileName, "r", function(error, fd) {
                  var buffer = new Buffer(stats.size);

                  fs.read(fd, buffer, 0, buffer.length, null, function(error, bytesRead, buffer) {
                    var data = buffer.toString("utf8", 0, buffer.length);

                    console.log(data);
                    fs.close(fd);
                  });
                });
              });
            }
            else{
              fs.writeFile(absFileName, JSON.stringify(allergene))
              console.log("wrote file: "+absFileName)
            }
          });
        })(i)
      }
    })
  }
}