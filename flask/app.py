
from flask import jsonify, Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import time
import json

auth = HTTPBasicAuth()
import os
"""Provides an API for models, intended for use with javascript and electron"""
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

value_types=None
@app.route('/', methods = ['GET'])
def home():
    return("server up")

@app.route('/rollback', methods = ['GET'])
def rollback():
    responseString=[]
    try:
        db.session.rollback()
    except Exception as e:
        return responseString.append(e.args), 500
    return  str(responseString)

@app.route('/products', methods = ['GET'])
def get_products():

    start = time.time()
    #TODO: log visits automatically
    visit = Visits("/products")
    db.session.add(visit)
    db.session.commit()
    result=[]
    edbString=request.args.get('edb')
    if not edbString:
        allProducts=Product.query.all()
    if edbString:
        if edbString == "true":
            allProducts=EdbProduct.query.all()
        elif edbString == "false":
            allProducts=TemplateProduct.query.all()
        else:
            allProducts=Product.query.all()
    fieldsString=request.args.get('fields')
    if fieldsString:
        fields=fieldsString.split(",")
    else:
        fields=None
    result = [a.toDict(fields=fields) for a in allProducts]
    end = time.time()
    print (end-start)
    return jsonify(result)


@app.route('/products/<id>', methods = ['GET'])
def get_product(id):
    visit = Visits("/products")
    db.session.add(visit)
    db.session.commit()
    try:
        product = Product.query.get(id)
    except Exception as e:
        product = None
    if not product or product is None:
        db.session.rollback()
        return "resource "+str(id)+" not found", 404
    else:
        return jsonify(product.toDict())


@app.route('/products', methods = ['POST'])
def post_product():
    if 'edb' in request.json:
        if request.json['edb']:
            product = EdbProduct()
        else:
            product = TemplateProduct()
    else:
        product = TemplateProduct()
    # if 'id' in request.json and Product.query.get(request.json['id']) is None:
    #     product.id=request.json['id']
    if not 'name' in request.json:
        return "name missing", 400
    else:
        product.name = request.json['name']
    db.session.add(product)
    db.session.commit()
    id = editProduct(product.id,request.json)
    return jsonify(product.toDict()),201

@app.route('/products/<id>', methods = ['PUT'])
def put_product(id):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource "+str(id)+" not found", 404
    else:
        editProduct(id,request.json)
        
        return jsonify(product.toDict())

@app.route('/products/<id>', methods = ['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource "+str(id)+" not found", 404
    else:
        db.session.delete(product)
        db.session.commit()
        return "",204

@app.route('/values/<id>', methods = ['GET'])
def get_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource "+str(id)+" not found", 404
    else:
        return jsonify(value.toDict())

@app.route('/values', methods=['POST'])
def post_value():
    value_types={
    'ProductNutrientAssociation':ProductNutrientAssociation,
    'ProductAllergeneAssociation': ProductAllergeneAssociation,
    'Co2Value':Co2Value,
    'FoodWasteData':FoodWasteData,
    'ProductDensity':ProductDensity,
    'ProductProcessNutrientAssociation':ProductProcessNutrientAssociation,
    'ProductProcessCO2Association':ProductProcessCO2Association,
    'ProductUnitWeight':ProductUnitWeight}
    if 'product' in request.json and 'type' in request.json:
        try:
            product=Product.query.get(request.json['product'])
        except:
            product=None
        if not product:
            print("product "+str(request.json['product'])+" not found")
            return "product "+str(request.json['product'])+" not found", 404
        elif request.json['type'] in value_types:
            value=value_types[request.json['type']]()
            value.product=product
            db.session.add(value)
            try:
                editValue(value, request.json)
            except TypeError as e:
                return str(e.args),400;
            db.session.commit()
            return jsonify(value.toDict()), 201
    return "must provide product and type",400


@app.route('/values/<id>', methods = ['PUT'])
def put_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource "+str(id)+" not found", 404
    else:
        editValue(value,request.json)
        db.session.add(value)
        return jsonify(value.toDict())

@app.route('/values/<id>', methods = ['DELETE'])
def delete_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource "+str(id)+" not found", 404
    else:
        db.session.delete(value)
        db.session.commit()
        return "",204

@app.route('/values', methods = ['GET'])
def get_values():
    return jsonify([a.toDict() for a in Value.query.all()])

@app.route('/references', methods = ['GET'])
def get_references():
    fieldsString=request.args.get('fields')
    if fieldsString:
        fields=fieldsString.split(",")
    else:
        fields=None
    return jsonify([a.toDict(fields=fields) for a in Reference.query.all()])

@app.route('/references', methods = ['POST'])
def post_reference():
    if 'name' in request.json:
        reference=Reference()
        reference.name=request.json['name']
        if 'comment' in request.json:
            reference.comment=request.json['comment']
        db.session.add(reference)
        db.session.commit()
        return jsonify(reference.toDict()), 201
    else:
        return ("name required"), 400

@app.route('/references/<id>', methods = ['PUT'])
def put_reference(id):
    try:
        reference = Reference.query.get(id)
    except:
        reference = None
    if not reference:
        return "resource "+str(id)+" not found", 404
    else:
        editReference(reference.id,request.json)
        return jsonify(reference.toDict())
# # authentication example
# @app.route('/<name>')
# @auth.login_required
# def hello_name(name):
#     print(name)

# @auth.verify_password
# def verify_password(username, password):
#     return True

@app.route('/allergenes', methods = ['GET'])
def get_allergenes():
    return jsonify([a.toDict() for a in Allergene.query.all()])

@app.route('/nutrients', methods = ['GET'])
def get_nutrients():
    return jsonify([a.toDict() for a in Nutrient.query.all()])

@app.route('/processes', methods = ['GET'])
def get_processes():
    return jsonify([a.toDict() for a in Process.query.all()])

@app.route('/processes', methods = ['POST'])
def post_process():
    if 'name' in request.json:
        process=Process()
        process.name=request.json['name']
        if 'type' in request.json:
            process.type=request.json['type']
        if 'description' in request.json:
            process.description=request.json['description']
        db.session.add(reference)
        db.session.commit()
        return jsonify(reference.toDict()), 201
    else:
        return "name required", 400

def editProduct(id,jsonData):
    product = Product.query.get(id)
    if 'allergenes' in jsonData:
        for allergeneDict in jsonData['allergenes']:
            if 'id' in allergeneDict:
                try:
                    association = ProductAllergeneAssociation.query.get(allergeneDict['id'])
                    editValue(association, allergeneDict)
                except:
                    raise TypeError('no allergene with'+str(allergeneDict['id']))
    if 'alternatives' in jsonData:
        for alternative in jsonData['alternatives']:
            try:
                alternative = Product.query.get(alternative['id'])
                if not alternative in product.alternatives:
                    product.alternatives.append(alternative)
            except:
                pass
    if 'co2Values' in jsonData:
        for co2Dict in jsonData['co2Values']:
            if 'id'  in co2Dict:
                try:
                    value=Co2Value.query.get(co2Dict['id'])
                    editValue(value, co2Dict)
                except:
                    value=None
    if 'commentsOnDensityAndUnitWeight' in jsonData:
        product.commentsOnDensityAndUnitWeight=jsonData['commentsOnDensityAndUnitWeight']
    if 'densities' in jsonData:
        for densityDict in jsonData['densities']:
             if 'id'  in densityDict:
                try:
                    value=ProductDensity.query.get(densityDict['id'])
                    editValue(value, densityDict)
                except:
                    value=None
    if 'endOfLocalSeason' in jsonData:
        #TODO: parse date, check, add
        pass
    if 'englishName' in jsonData:
        product.englishName = jsonData['englishName']
    if 'foodWasteData' in jsonData:
        for foodWasteDict in jsonData['foodWasteData']:
             if 'id'  in foodWasteDict:
                try:
                    value=FoodWasteData.query.get(foodWasteDict['id'])
                    editValue(value, foodWasteDict)
                except:
                    value=None
    if 'frenchName' in jsonData:
        product.frenchName = jsonData['frenchName']
    if 'infoTextForCook' in jsonData:
        product.infoTextForCook = jsonData['infoTextForCook']
    if 'name' in jsonData:
        product.name = jsonData['name']
        #add ProductProcessNutrientAssociation (if not existing) and if necessary create respective Nutrient and Process (side effect) 
    if 'nutrientProcesses' in jsonData:
        for processDict in jsonData['nutrientProcesses']:
             if 'id' in processDict:
                try:
                    value=ProductProcessNutrientAssociation.query.get(processDict['id'])
                    editValue(value, processDict)
                except:
                    value=None
    #add ProductNutrientAssociation (if not existing) and if necessary create respective Nutrient (side effect)
    if 'nutrients' in jsonData:
        for nutrientDict in jsonData['nutrients']:
             if 'id'  in nutrientDict:
                try:
                    value=ProductNutrientAssociation.query.get(nutrientDict['id'])
                    editValue(value, nutrientDict)
                except:
                    value=None
    if 'possibleOrigins' in jsonData:
        for originName in jsonData['possibleOrigins']:
            try:
                location = Location.query.filter(Location.name == originName).all()[0]
            except:
                location = None
            if not location:
                location = Location()
                location.name = originName
                db.session.add(location)
            if not location in product.possibleOrigins:
                product.possibleOrigins.append(location)

    if 'processes' in jsonData:
        product.processes=[]
        for processDict in jsonData['processes']:
            if 'id' in processDict:
                try:
                    process = Process.query.get(processDict['id'])
                except:
                    process = None
                if process:
                    product.processes.append(process)

    if 'processesCo2' in jsonData:
        for processDict in jsonData['processesCo2']:
             if 'id'  in processDict:
                try:
                    value=ProductProcessCO2Association.query.get(processDict['id'])
                    editValue(value, processDict)
                except:
                    value=None
    if 'specification' in jsonData:
        product.specification = jsonData['specification']
    if 'standardOrigin' in jsonData:
        try:
            location = Location.query.filter(Location.name == jsonData['standardOrigin']).all()[0]
        except:
            location = None
        if not location:
            location = Location()
            location.name = jsonData['standardOrigin']
            db.session.add(location)
            product.standardOrigin = location
    if 'startOfLocalSeason' in jsonData:
        product.startOfLocalSeason = jsonData['startOfLocalSeason']
    if 'synonyms' in jsonData:
        for synonymName in jsonData['synonyms']:
            try:
                synonym = Synonym.query.get(synonymName)
            except:
                synonym = None
            if not synonym:
                synonym = Synonym(synonymName)
                #side effect
                db.session.add(synonym)
            product.synonyms.append(synonym)
    if 'tags' in jsonData:
        for tagName in jsonData['tags']:
            try:
                tag = Tag.query.get(tagName)
            except:
                tag = None
            if not tag:
                tag = Tag()
                tag.name = tagName
                #side effect
                db.session.add(tag)
            product.tags.append(tag)
    if 'texture' in jsonData:
        product.texture = jsonData['texture']
    if 'unitWeights' in jsonData:
        for unitWeightDict in jsonData['unitWeights']:
            if 'id'  in unitWeightDict:
                try:
                    value=ProductUnitWeight.query.get(unitWeightDict['id'])
                    editValue(value, unitWeightDict)
                except:
                    value=None
    db.session.add(product)
    db.session.commit()
    return product.id

def editValue(value,valueDict):
    #common fields for values
    if 'amount' in valueDict:
        value.amount = valueDict['amount']
        value.baseValue = None
    if 'comment' in valueDict:
        value.comment=valueDict['comment']
    if 'unit' in valueDict:
        value.unit = valueDict['unit']
    if 'referenceId' in valueDict:
        try:
            reference = Reference.query.get(valueDict['referenceId'])
        except:
            reference = None
        if reference:
            value.reference=reference
    elif 'reference' in valueDict:
        try:
            reference = Reference.query.filter(Reference.name == valueDict['reference']).all()[0]
        except:
            reference = None
        if not reference:
            reference = Reference()
            reference.name = valueDict['reference']
        value.reference = reference
        db.session.add(reference)
    if 'validCountries' in valueDict:
        value.validCountries=[]
        for countryName in valueDict['validCountries']:
            try:
                location=Location.query.filter(Location.name==countryName).get[0]
            except:
                location=None
            if not location:
                location=Location()
                location.name=countryName
                db.session.add(location)
            value.validCountries.append(location)
    if 'baseValue' in valueDict:
        try:
            baseValue = Value.query.get(valueDict['baseValue'])
            if not baseValue==value:
                value.baseValue=baseValue
        except:
            pass

    #type specific fields
    if not 'type' in valueDict:
        raise TypeError
        db.session.rollback()
    elif valueDict['type']=='Co2Value' and type(value)==Co2Value:
        # no additonal fields
        pass
    elif valueDict['type']=='FoodWasteData' and type(value)==FoodWasteData and 'field' in valueDict:
        try:
            field=FoodWasteField.query.get(valueDict['field'])
        except:
            field=None
        if not field:
            field=FoodWasteField()
            field.name=valueDict['field']
            db.session.add(field)
        value.field=field
    elif valueDict['type']=='ProductDensity' and type(value)==ProductDensity:
        # no additonal fields
        pass
    elif valueDict['type']=='ProductAllergeneAssociation' and type(value)==ProductAllergeneAssociation and 'allergeneName' in valueDict:
        try:
            allergene = Allergene.query.filter(Allergene.name == valueDict['allergeneName']).all()[0]
        except:
            allergene = None
        if not allergene:
            allergene = Allergene()
            allergene.name = valueDict['allergeneName']
            db.session.add(allergene)
        value.allergene=allergene
    elif valueDict['type']=='ProductProcessCO2Association' and type(value)==ProductProcessCO2Association and 'processName' in valueDict:
        try:
            process = Process.query.filter(Process.name == valueDict['processName']).all()[0]
        except:
            process = None
        if not process:
            process = Process()
            process.name = valueDict['processName']
            db.session.add(process)
        value.Process=process
    elif valueDict['type']=='ProductNutrientAssociation' and type(value)==ProductNutrientAssociation and 'nutrientName' in valueDict:
        try:
            nutrient = Nutrient.query.filter(Nutrient.name == valueDict['nutrientName']).all()[0]
        except:
            nutrient = None
        if not nutrient:
            nutrient = Nutrient()
            nutrient.name = valueDict['nutrientName']
            db.session.add(nutrient)
        value.nutrient=nutrient
    elif valueDict['type']=='ProductProcessNutrientAssociation' and type(value)==ProductProcessNutrientAssociation and 'nutrientName' in valueDict and 'processName' in valueDict:
        try:
            process = Process.query.filter(Process.name == valueDict['processName']).all()[0]
        except:
            process = None
        if not process:
            process = Process()
            process.name = valueDict['processName']
            db.session.add(process)
        value.Process=process
        try:
            nutrient = Nutrient.query.filter(Nutrient.name == valueDict['nutrientName']).all()[0]
        except:
            nutrient = None
        if not nutrient:
            nutrient = Nutrient()
            nutrient.name = valueDict['nutrientName']
            db.session.add(nutrient)
        value.nutrient=nutrient
    elif valueDict['type']=='ProductUnitWeight' and type(value)==ProductUnitWeight:
        # no additonal fields
        pass
    else:
        raise TypeError('missing arguments for type '+value.type)
    db.session.commit()
    return value.id

def editReference(id, jsonData):
    reference = Reference.query.get(id)
    if 'name' in jsonData:
        reference.name = jsonData['name']
    if 'comment' in jsonData:
        reference.comment = jsonData['comment']
    db.session.add(reference)
    db.session.commit()
    return reference.id

if __name__ == '__main__':
    app.run(threaded=True)