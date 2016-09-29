module.exports = {
  convertLegacy : function(legacyProducts,legacyProcesses,legacyNutrients,legacyNutritionChanges,legacyFoodWastes){
      var createUniqueFile = function(index,basePath,baseName){

        var tryPath=path.join(basePath,baseName.concat(String(index)))
        try{
          var pathStat=fs.statSync(tryPath)
          if (pathStat.isFile() || pathStat.isDirectory()){
            return(createUniqueFile(index+1,basePath,baseName))
          }
          else{
            return(tryPath)
          }
        }catch(err){
          return(tryPath)
        }
      }

      var logToFile = function(text,path){
        fs.appendFile(path,text+"\n")
      }

      var legacyLogBasePath = path.join(__dirname,"..")
      var logPath=createUniqueFile(0,legacyLogBasePath,"legacyLog")
      

      // Post all products and store their new representation
      var prodsToPost=[]
      var referencesToPost=[]
      var productNutrientAssociationsToPost=[]
      var productAllergeneAssociationsToPost=[]
      var co2ValuesToPost=[]
      var co2ValuesLinkedToPost=[]
      var foodWasteDatasToPost=[]
      var productDensitiesToPost=[]
      var productProcessNutrientAssociationsToPost=[]
      var productProcessCO2AssociationsToPost=[]
      var productUnitWeightsToPost=[]

      for (nutrientDataId in legacyNutrients){
        nutrientDataSet=legacyNutrients[nutrientDataId]
      }

      //create template products for nutr-change files
      for (legacyNutritionChangeIndex in legacyNutritionChanges){
        legacyNutritionChange=legacyNutritionChanges[legacyNutritionChangeIndex]
        var nutrProcessProdToPost={
          name:legacyNutritionChange['name'],
          specification:"nutrition change template product",
          edb:false
        }
        legacyNutritionChange['nutrProcessProdToPost']=nutrProcessProdToPost
        httpPostSync(baseURL+'/products',JSON.stringify(nutrProcessProdToPost),function(response){
          if(debug==true){
            console.log("posted nutrProcessProdToPost: "+JSON.stringify(productDensityToPost))
            console.log("response: "+response)
          }
          nutrProcessProdToPost['newProd']=angular.fromJson(response)
        })
        for(componentIndex in legacyNutritionChange['nutr-change-vector']){

          var productProcessNutrientAssociationToPost={
            type:"ProductProcessNutrientAssociation",
            amount:['nutr-change-vector'][componentIndex]["value"],
            nutrientName:legacyNutritionChange['nutr-change-vector'][componentIndex]["component-id"],
            product:nutrProcessProdToPost['newProd']['id'],
            processName:legacyNutritionChange["process"],
            unit:""
          }
          if(legacyNutritionChange["valuesToPost"]){
            legacyNutritionChange["valuesToPost"].push(productProcessNutrientAssociationToPost)
          }
          else{
            legacyNutritionChange["valuesToPost"]=[productProcessNutrientAssociationToPost]
          }
          httpPostSync(baseURL+'/values',JSON.stringify(productProcessNutrientAssociationToPost),function(response){
            if(debug==true){
              console.log("posted nutrProcessProdToPost: "+JSON.stringify(productDensityToPost))
              console.log("response: "+response)
            }
            productProcessNutrientAssociationToPost['newValue']=angular.fromJson(response)
          })
        }
      }
      // create Product from a product File
      for (productId in legacyProducts){
        try{
          var legacyProduct=legacyProducts[productId]
          var allergenes=[]
          var alternatives=[]
          var prodToPost={
            "allergenes": [],
            "alternatives": [],
            "co2Values": [],
            "commentsOnDensityAndUnitWeight": legacyProduct["quantity-comments"],
            "densities": [],
            "edb": true,
            "endOfLocalSeason": "None",
            "englishName": legacyProduct["name-english"],
            "foodWasteData": [],
            "frenchName": legacyProduct["name-french"],
            "id": legacyProduct.id,
            "infoTextForCook": legacyProduct["info-text"],
            "name": legacyProduct.name,
            "nutrientProcesses": [],
            "nutrients": [],
            "possibleOrigins": [],
            "processesCo2": [],
            "specification": legacyProduct["specification"],
            "startOfLocalSeason": legacyProduct[""],
            "synonyms": [],
            "tags": [],
            "texture": legacyProduct["consistency"],
            "unitWeights": []
          }

          // store for later use
          prodsToPost.push(prodToPost)
          legacyProduct['prodToPost']=prodToPost

          // post this product, sync to make sure the server is not overwhelmed:
          httpPostSync(baseURL+'/products', JSON.stringify(prodToPost),function(response){
            if(debug==true){
              console.log("posted product: "+JSON.stringify(prodToPost))
              console.log("response: "+response)
            }
            // store the server representation with the local product object 
            prodToPost['newProd']=angular.fromJson(response)
            if(prodToPost.id!==prodToPost['newProd']['id']){
              logToFile(JSON.stringify({"oldProductId":prodToPost.id, "newProductId": prodToPost['newProd']['id']}),logPath)
            }
          })


          //convert nutrition data set to multiple ProductNutrientAssociations and a single Reference
          if(legacyProduct['nutrition-id']){
            nutritionData=legacyNutrients[legacyProduct['nutrition-id']]

            var referenceToPost={
              name: "EuroFIR"+nutritionData['id']+" "+nutritionData['name'],
              comment: "generated at legacy import"
            }
            // check if there is a reference for this file
            if(nutritionData['referencesToPost']==null){
              nutritionData['referencesToPost']=[]
              nutritionData['referencesToPost'].push(referenceToPost)
              referencesToPost.push(referenceToPost)

              // post reference to server
              httpPostSync(baseURL+'/references',JSON.stringify(referenceToPost),function(response){
                referenceToPost['newRef']=angular.fromJson(response)
                if(debug==true){
                  console.log("posted reference: "+JSON.stringify(referenceToPost))
                  console.log("response: "+response)
                }
              })
            }

            for(counter in nutritionData['nutr-vals']){
              val=nutritionData['nutr-vals'][counter]
              productNutrientAssociationToPost={
                type:"ProductNutrientAssociation",
                reference:referenceToPost.name,
                nutrientName:val['component-id'],
                amount:val.value,
                unit:val.unit,
                validCountries:[val.country],
                product:prodToPost['newProd']['id']
              }

              // store the Nutrition Value with the nutrition file for later use
              if(nutritionData['productNutrientAssociationsToPost']==null){
                nutritionData['productNutrientAssociationsToPost']=[]
              }
              nutritionData['productNutrientAssociationsToPost'].push(productNutrientAssociationToPost)
              productNutrientAssociationsToPost.push(productNutrientAssociationToPost)

              // post Product Nutrient Association to server
              httpPostSync(baseURL+'/values',JSON.stringify(productNutrientAssociationToPost),function(response){
                if(debug==true){
                  console.log("posted productNutrientAssociation: "+JSON.stringify(productNutrientAssociationToPost))
                  console.log("response: "+response)
                }
                //save the server representation with the value
                productNutrientAssociationToPost['newValue']=angular.fromJson(response)
              })
            }


            co2ValueToPost={
              type:"Co2Value",
              product:prodToPost['newProd']['id'],
              amount:legacyProduct['co2-value']||null,
              unit:"kg CO2 Äq/kg",
              referenceName:legacyProduct['references'],
              comment:"co2-calculation: ".concat(legacyProduct['co2-calculation']||"-").concat(" calculation-process-documentation: ").concat(legacyProduct['calculation-process-documentation']||"-")
            }
          // store for later use
          legacyProduct['co2ValueToPost']=co2ValueToPost

          //products with only basic co2 value get their value put immediately
          if(legacyProduct['linked-id']==null){
            httpPostSync(baseURL+'/values',JSON.stringify(co2ValueToPost),function(response){
              if(debug==true){
                console.log("posted Co2Value: "+JSON.stringify(co2ValueToPost))
                console.log("response: "+response)
              }co2ValueToPost['newValue']=angular.fromJson(response)
            })
          }

          //products with linked co2 value are stored, so they can later be linked and put
          else{
            //store the old id of the base value product
            co2ValueToPost['legacyBaseValueId']=legacyProduct['linked-id']
            co2ValuesLinkedToPost.push(co2ValueToPost)
            if(debug==true){
              console.log("linked co2-value detected. Id: "+legacyProduct['id'])
            }
          }

          //create quantityReference, post it and add density and unit weight in callback
          if (legacyProduct['unit-weight']||legacyProduct['density']){
            logToFile("found unit-weight or density in file: "+String(legacyProduct.id),logPath)
            var quantityReferenceToPost={
              name: legacyProduct['quantity-references'],
              comment: "generated at legacy import"
            }

            httpPostSync(baseURL+'/references',JSON.stringify(quantityReferenceToPost),function(response){
              quantityReferenceToPost['newRef']=angular.fromJson(response)
              logToFile("posted quantity reference",logPath)
              // unitWeight
              try{
                var productUnitWeightToPost={
                  type:"ProductUnitWeight",
                  comment:legacyProduct["quantity-comments"],
                  product:legacyProduct['prodToPost']['newProd']['id'],
                  amount: legacyProduct['unit-weight'],
                  referenceId:quantityReferenceToPost['newRef']['id']
                }
                httpPostSync(baseURL+'/values',JSON.stringify(productUnitWeightToPost),function(response){
                  // if(debug==true){
                    console.log("posted UnitWeight: "+JSON.stringify(productUnitWeightToPost))
                    console.log("response: "+response)
                  // }
                  productUnitWeightToPost['newValue']=angular.fromJson(response)
                })
              }catch(err){logToFile(err.message+" for unit weight in product: "+productId,logPath)}
              // density
              try{
                var productDensityToPost={
                  type:"ProductDensity",
                  comment:legacyProduct["quantity-comments"],
                  product:legacyProduct['prodToPost']['newProd']['id'],
                  amount: legacyProduct['unit-weight'],
                  referenceId:quantityReferenceToPost['newRef']['id']
                }
                httpPostSync(baseURL+'/values',JSON.stringify(productDensityToPost),function(response){
                  if(debug==true){
                    console.log("posted density: "+JSON.stringify(productDensityToPost))
                    console.log("response: "+response)
                  }
                  productDensityToPost['newValue']=angular.fromJson(response)
                })
              }catch(err){logToFile(err.message+" for density in product: "+productId,logPath)}

              if(debug==true){
                console.log("posted quantity reference: "+JSON.stringify(quantityReferenceToPost))
                console.log("response: "+response)
              }
            })
          }

          // post productProcessNutrientAssociation per nutrient per process for a template product and derive from it
          for(processIndex in legacyProduct.processes){
            var legacyProductProcess=legacyProduct.processes[processIndex]
            var legacyNutritionChange=legacyNutritionChanges[legacyProcess['nutr-change-id']]
            if(legacyNutritionChange['nutrProcessProdToPost']===null){

            }
          }
        }
      }
      catch(err){
        logToFile(err.message+" for product: "+productId,logPath)
      }
    }
    // link and post linked co2Values
    for(counter in co2ValuesLinkedToPost){
      co2ValueLinkedToPost=co2ValuesLinkedToPost[counter]
      baseProduct=legacyProducts[co2ValueLinkedToPost['legacyBaseValueId']]
      try{
        co2ValueLinkedToPost['baseValue']=baseProduct['co2ValueToPost']['newValue']['id']
        httpPostSync(baseURL+'/values',JSON.stringify(co2ValueLinkedToPost),function(response){
                if(debug==true){
                  console.log("posted Co2Value: "+JSON.stringify(co2ValueLinkedToPost))
                  console.log("response: "+response)
                }co2ValueLinkedToPost['newValue']=angular.fromJson(response)
              })
      }
      catch(err){
        console.error(JSON.stringify(baseProduct))
        console.error(err)
      }
      console.log("linked co2 counter: "+counter)
    }
  }
}