SOLID_FORTNIGHT_BA documentation
this software is also available under https://github.com/schinke/solid-fortnight-ba
BACHELOR THESIS PROJECT
JENS HINKELMANN - KAPPEL SO, SWITZERLAND

This project contains:
- A backend built on flask, providing a database model and a REST-API.
- A frontend built on electron which, when launched, launches the backend as well.

_______________________________________
Requirements:
- PostgreSQL: http://www.enterprisedb.com/products-services-training/pgdownload
- Python 2.7.9+: https://www.python.org/downloads/
- Virtualenv: pip install virtualenv
- Electron: http://electron.atom.io/releases/
The project is runnable on microsoft platforms, the install procedure varies slightly.
_______________________________________
Install procedure:
- Start PostgreSQL and create database 'edbdev'
- In the folder 'flask' of this project execute:
- - venv/bin/activate
- - pip install -r requirements.txt
- - python manage.py db init
- - python manage.py db migrate
- - python manage.py db upgrade

_______________________________________
Launch procedure:
-In the folder electron type:
- - electron .

_______________________________________
FOLDER STRUCTURE:
- flask: contains the backend component
- - project
- - venv
- - - ...
- electron: contains the frontend component
- - allmighty-autocomplete
- - - script
- - - style
- - node_modules
- - static
- - views
- - - snippets
- - - - extender

_______________________________________
API overview
- resources:
- - http://localhost:5000/products?fields=<field1>,<field2>, methods=[GET, POST]
- - http://localhost:5000/products/<id>, methods=[GET, PUT, DELETE]

- - http://localhost:5000/values, methods=[GET, POST]
- - http://localhost:5000/values/<id>, methods=[GET, PUT, DELETE]

- - http://localhost:5000/references, methods=[GET, POST]
- - http://localhost:5000/references/<id>, methods=[PUT]

- - http://localhost:5000/allergenes, methods=[GET]

- - http://localhost:5000/nutrients, methods=[GET]

- - http://localhost:5000/processes, methods=[GET]

_______________________________________
API resource representation:
- product JSON representation (values are examples):
    {
      "allergenes": [
        {
          "allergeneId": 2,
          "allergeneName": "milk",
          "amount": null,
          "comment": null,
          "derived": false,
          "id": 16604,
          "product": 3,
          "type": "ProductAllergeneAssociation",
          "unit": null,
          "validCountries": []
        }
      ],
      "alternatives": [12,13],
      "co2Values": [
        {
          "amount": 1.32,
          "comment": "co2-calculation: Value directly from reference (1). FU = 500 g packaged margarine, Germany 0.66*2 = 1.32 kg CO2Äq/kg calculation-process-documentation: cradle to main distribution centre, storage at distribution centre not included. \r\nProduction in Germany. Margarine composition 70% fat: 36% rape seed oil, 3.5 sunflower oil, 3.5 maize oil, 26.5% palm oil and the rest water. \r\n",
          "derived": false,
          "id": 110,
          "product": 4,
          "type": "Co2Value",
          "unit": "kg CO2 Äq/kg",
          "validCountries": []
        }
      ],
      "commentsOnDensityAndUnitWeight": "",
      "densities": [
        {
          "amount": null,
          "comment": "",
          "derived": false,
          "id": 112,
          "product": 4,
          "reference": "http://stason.org/TULARC/food/cooking/2-7-5-Weight-Volume-Conversion-Chart.html",
          "referenceId": 8,
          "type": "ProductDensity",
          "unit": null,
          "validCountries": []
        }
      ],
      "edb": true,
      "endOfLocalSeason": "31-12-0000",
      "englishName": "margarine",
      "foodWasteData": [
      ],
      "frenchName": null,
      "id": 4,
      "infoTextForCook": "depending on oil composition CO2-value differs per margarine. Sunflower oil has the highest CO2-impact. They did a sensitivity analysis with a worst case scenario for palm oil production 50% from deforestated land and 50% from peat soils. In this scenario the margarine does still not exceed 50% of the best butter. Emissions from milk are at farm gate higher than that of oil crops, mainly due to methane, fodder production and manure handling. ",
      "name": "Margarine",
      "nutrientProcesses": [],
      "nutrients": [
        {
          "amount": 2980,
          "comment": null,
          "derived": false,
          "id": 109,
          "nutrientId": 7,
          "nutrientName": "ENERC",
          "product": 4,
          "reference": "EuroFIR831076 Margarine",
          "referenceId": 7,
          "type": "ProductNutrientAssociation",
          "unit": "kJ",
          "validCountries": [
            null
          ]
        }
      ],
      "possibleOrigins": ["France, Germany"],
      "processes": [
        {
          "description": null,
          "id": 1,
          "name": "cooking",
          "type": null
        }
      ],
      "processesCo2": [
        {
          "amount": 0.3,
          "comment": null,
          "derived": false,
          "id": 16610,
          "processId": 1,
          "processName": "cooking",
          "product": 3,
          "type": "ProductProcessCO2Association",
          "unit": null,
          "validCountries": []
        }
      ],
      "specification": "not plant based",
      "startOfLocalSeason": "1-1-0000",
      "synonyms": ["falsche Butter"],
      "tags": ["fett"],
      "texture": "zäh",
      "unitWeights": [
        {
          "amount": null,
          "comment": "",
          "derived": false,
          "id": 111,
          "product": 4,
          "reference": "http://stason.org/TULARC/food/cooking/2-7-5-Weight-Volume-Conversion-Chart.html",
          "referenceId": 8,
          "type": "ProductUnitWeight",
          "unit": null,
          "validCountries": []
        }
      ]
    }
- value JSON representation (values are examples):
  {
    "amount": 0,
    "comment": null,
    "derived": false,
    "id": 77,
    "product": 3,
    "reference": "EuroFIR1001137 Sunflower oil",
    "referenceId": 5,
    "type": "",
    "unit": "g",
    "validCountries": [
      null
    ]
  }

- - if the value object is given an attribute "baseValue" with a valid id as value which does not create a circular dependency, the "derived" attribute is set to true by the server and "baseValue" is stored.
- - for following values of attribute "type", there are no additional fields to a standard value:
- - - "Co2Value"
- - - "ProductDensity"
- - - "ProductUnitWeight"
- - for following value resources there may be following additional fields (values are examples):
- - - if "type" is "ProductNutrientAssociation": "nutrientId": 5, "nutrientName": "CHOT"
- - - if "type" is "FoodWasteData": "field":"production-avoidable"
- - - if "type" is "ProductAllergeneAssociation": "allergeneId":2, allergeneName:"fish"
- - - if "type" is "ProductProcessNutrientAssociation": "processId":1, "processName":"cooking", "nutrientId": 5 "nutrientName": "CHOT"
- - - if "type" is "ProductProcessCO2Association": "processId":1, "processName":"cooking"
- process JSON representation (values are examples):
  {
    "description": "putting product in hot water",
    "id": 1,
    "name": "cooking",
    "type": "processing"
  }
- allergene JSON representation (values are examples):
  {
    "abbreviation": null,
    "name": "milk"
  }
- nutrient JSON representation (values are examples):
  {
    "abbreviation": "ALC",
    "name": "Alcohol"
  }

_______________________________________
API usage
- to add a product:
  POST a product with at least the attribute "name" according to afforementioned representation
- to edit simple product attribute:
  PUT the resource with the changed attributes. The "id" attribute can not be changed.
- to add a value to a product:
  POST a value with at least the attribute "type" the attribute "product" and the required additional fields (compare previous section)
- to edit a value:
- -PUT the value represenation with changed attributes. The "id", "type" and "derived" attributes can not be changed but "derived" changes if no "baseValue" attribute is provided. New allergenes, nutrients, processes and references may be created as side effect.
- -or: PUT the related product with a changed representation of the value. The "id" has to be the same. New allergenes, nutrients, processes and references may be created as side effect.
- to remove a product or value:
  DELETE the respective resource
- to create a reference:
  mention name the first time in a value (side effect)
  or POST a reference with at least the attribute "name"
- to edit a reference:
  PUT the value represenation with changed attributes. The "id" attribute can not be changed.

_______________________________________
FRONTEND usage
- MainWindow
- - choose and filter products.
- - click on "open_in_new" icon next to a product to show details in productForm window.
- - click on the hovering "add" icon to add a product. press "save" to return to list. press "save and edit" to open productForm window.
- ProductForm:
- - edit text fields
- - while the "save" icon is marked red, changes need to be saved. Click it to save.
- - click on "input" icon next to a CO2 value or nutrient group to open the edit side bar.
- - click on "add" below the list of CO2 values to post a new, empty CO2 value for the product
- - click on "add" after entering a reference name below nutrient groups to create a new nutrient group for the product and group
- - when the edit side bar is open from clicking the "input" icon next to a co2 value, a co2 value can be marked as derived and a product can be chosen in the autocomplete text field to derive the value from. After choosing a value out of the list which appears below the text field when a product was chosen, the "derived" row in the center list representation of the edited value is set to "YES".
- - when the edit side bar is open from clicking the "input" icon next to a nutrient value group, the contained values can be edited, new values can be added, existing values can be deleted. Clicking the "show countries"-link makes a text field appear over which one can enter where the respective set of nutrient values is valid. These countries can be deleted again as well.

- - click on the "upload" icon to display a modal with upload fields. If all requested files are provided, a button appears to convert the legacy files and save them on the server. This process may take up to 5 minutes on a mediocre CPU in 2016.

_______________________________________
CODE documentation Flask

- flask/models.py: Defines the model for SQLAlchemy. All classes implement toDict() for API usage:
     11: class Visits(db.Model)
     26: class Value(db.Model)
    102: class Location(db.Model)
    108: class FoodWasteField(db.Model)
    113: class FoodWasteData(Value)
    134: class Process(db.Model)
    147: class Allergene(db.Model)
    157: class Nutrient(db.Model)
    165: class Tag(db.Model)
    170: class Synonym(db.Model)
    175: class Co2Value(Value)
    191: class Reference(db.Model)
    209: class TagProductAssociation(db.Model)
    215: class SynonymProductAssociation(db.Model)
    221: class ProductAllergeneAssociation(Value)
    252: class LocationProductAssociation(db.Model)
    259: class ProductProcessNutrientAssociation(Value)
    283: class ProductProcessCO2Association(Value)
    301: class ProductNutrientAssociation(Value)
    319: class ProductDensity(Value)
    332: class ProductUnitWeight(Value)
    346: class ProductAlternative(db.Model)
    352: class LocationProductAssociation(db.Model)
    358: class LocationValueAssociation(db.Model)
    364: class Product(db.Model)
    459: class EdbProduct(Product)
    472: class TemplateProduct(Product)

- flask/app.py: Python entry point. Defines the endpoints of the API and refactored functions:
  19: @app.route('/', methods = ['GET'])
  23: @app.route('/rollback', methods = ['GET'])
  32: @app.route('/products', methods = ['GET'])
  62: @app.route('/products/<id>', methods = ['GET'])
  78: @app.route('/products', methods = ['POST'])
  98: @app.route('/products/<id>', methods = ['PUT'])
  111: @app.route('/products/<id>', methods = ['DELETE'])
  124: @app.route('/values/<id>', methods = ['GET'])
  135: @app.route('/values', methods=['POST'])
  168: @app.route('/values/<id>', methods = ['PUT'])
  181: @app.route('/values/<id>', methods = ['DELETE'])
  194: @app.route('/values', methods = ['GET'])
  198: @app.route('/references', methods = ['GET'])
  207: @app.route('/references', methods = ['POST'])
  220: @app.route('/references/<id>', methods = ['PUT'])
  241: @app.route('/allergenes', methods = ['GET'])
  245: @app.route('/nutrients', methods = ['GET'])
  249: @app.route('/processes', methods = ['GET'])
  253: @app.route('/processes', methods = ['POST'])
  268: def editProduct(id,jsonData): returns an edited Product object
  430: def editValue(value,valueDict): returns an edited value object
  553: def editReference(id, jsonData): returns an edited reference object

_______________________________________
CODE documentation Electron

- electron/main.js is electron's entry point:
  1.checks if server at 'http://localhost:5000' is responding, else try to run "python ../flask/app.py"
  2.creates BrowserWindow mainWindow and BrowserWindow productForm
  3.shows mainWindow
  4.On inter process signal "show-prod-form" with id sends the id to productForm window as 'prodFormId'

_______________________________________
CODE documentation AngularJS

- electron/viewProductController.js is Angular controller for electron/views/mainWindow.html
- electron/productFormController.js is Angular controller for electron/views/productForm.html
- electron/legacyImporter.js is extracted function of electron/viewProductController.js to convert JSON data in the format of the old EDB solution and post to the server:
  1.Product files are converted to API Product entities, posted on server and id changes are logged to legacyLog.txt
  2.Nutrient files are parsed and for each entry a ProductNutrientAssociation entity is posted on server and the new value is saved to the old file object. Reference names are generated from name and id of the nutrient data objects as <id><name>. A comment "generated at legacy import" is added. References are posted if not yet done for previous.
  3.If a co2-value is saved with a product, CO2Values are extracted from product files and posted to server. A reference is generated if the attribue "references" of the product has a value.
  4.If a co2-value is only a link to another product the product is posted without CO2-Value and marked for later to make sure the linked product is posted first.
  5.after all products are posted, the missing co2-values are created, linked to their base values and posted
  6. A log file called ../legacylog is created to protocol the inevitable changes of ids and incorrect JSON data which might cause products no to be updated.
- electron/backUpService.js is an extracted function of electron/viewProductController.js to save JSON data to local file system:
  1.creates a folder at ../../export<id> where <id> is an increasing number to avoid overwriting
  2.creates subfolders "processes", "allergenes", "nutrients", "references", "products"
  3.gets products from server and saves them into a file named <id><name>.json
  4.gets references and saves them
  5.gets allergenes and saves them
  6.gets nutrients and saves them
  7.gets processes and saves them

- electron/static/ folder contains materialize css and javascript for website layout. see respective files for license information

- electron/views contains .html for frontend

- electron/allmighty-autocomplete contains a modified version of JustGoscha's allmighty-autocomplete directive. Instead of taking a list of literals, it takes a list of any objects in the ng-data attribute of the html tag. The autosearchfield attribute takes the name of the objects' field which should be put into the input field. The attribute autoshowfields takes an array of strings or function objects for additional information to be shown in the dropdown list of the auto-complete. The function objects get the single objects of the array as argument and must return one value to be shown next to the autosearchfield.


