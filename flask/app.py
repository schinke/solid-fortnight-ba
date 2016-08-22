
from flask import jsonify, Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
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

@app.route('/rollback', methods = ['GET'])
def rollback():
    db.session.rollback()
    return "rolled back"

@app.route('/products', methods = ['GET'])
def get_products():

    #TODO: log visits automatically
    visit = Visits("/products")
    db.session.add(visit)
    db.session.commit()
    return jsonify([a.toDict() for a in Product.query.all()])


@app.route('/products/<id>', methods = ['GET'])
def get_product(id):
    visit = Visits("/product")
    db.session.add(visit)
    db.session.commit()
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource not found"#TODO: add appropriate status code
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

    if not 'name' in request.json:
        return "name missing"#TODO: add appropriate status code
    else:
        product.name = request.json['name']
    db.session.add(product)
    db.session.commit()
    id = editProduct(product.id,request.json)
    return jsonify(product.toDict())

@app.route('/products/<id>', methods = ['PUT'])
def put_product(id):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource not found"#TODO: add appropriate status code
    else:
        editProduct(id,request.json)
        return jsonify(product.toDict())

@app.route('/product/<id>', methods = ['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource not found"#TODO: add appropriate status code
    else:
        db.session.delete(product)
        db.session.commit()
        return "ok"

@app.route('/values/<id>', methods = ['GET'])
def get_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource not found"#TODO: add appropriate status code
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
            return "resource not found"#TODO: add appropriate status code
        elif request.json['type'] in value_types:
            value=value_types[request.json['type']]()
            value.product=product
            db.session.add(value)
            editValue(value, request.json)
            db.session.commit
            return jsonify(value.toDict())
        else:
            return str(value_types['ProductProcessNutrientAssociation'])

@app.route('/values/<id>', methods = ['PUT'])
def put_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource not found"#TODO: add appropriate status code
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
        return "resource not found"#TODO: add appropriate status code
    else:
        db.session.delete(value)
        db.session.commit()
        return "ok"

@app.route('/values', methods = ['GET'])
def get_values():
    return jsonify([a.toDict() for a in Value.query.all()])

@app.route('/references', methods = ['GET'])
def get_references():
    return jsonify([a.toDict() for a in Reference.query.all()])

@app.route('/references/<id>', methods = ['PUT'])
def put_reference(id):
    try:
        reference = Reference.query.get(id)
    except:
        reference = None
    if not reference:
        return "resource not found"#TODO: add appropriate status code
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

def editProduct(id,jsonData):
    product = Product.query.get(id)
    if 'allergenes' in jsonData:
        product.allergenes=[]
        for allergeneDict in jsonData['allergenes']:
            if 'id' in allergeneDict:
                try:
                    association = ProductAllergeneAssociation.query.get(ProductAllergeneAssociation.id == allergeneDict['id']).all()[0]
                except:
                    association = None
                if association:
                    association.product=product
                    db.session.add(association)
                    editValue(association, allergeneDict)
    if 'alternatives' in jsonData:
        for alternative in jsonData['alternatives']:
            try:
                alternative = Product.query.get(alternative['id'])
                if not alternative in product.alternatives:
                    product.alternatives.append(alternative)
            except:
                pass
    if 'co2Values' in jsonData:
        product.Co2Values=[]
        for co2Dict in jsonData['co2Values']:
            if 'id'  in co2Dict:
                try:
                    value=Co2Value.query.get(co2Dict['id'])
                except:
                    value=None
                if value:
                    product.co2Values.append(value)
                    db.session.add(value)
                    editValue(value, co2Dict)
    if 'commentsOnDensityAndUnitWeight' in jsonData:
        product.commentsOnDensityAndUnitWeight=jsonData['commentsOnDensityAndUnitWeight']
    if 'densities' in jsonData:
        for densityDict in jsonData['densities']:
             if 'id'  in densityDict:
                try:
                    value=ProductDensity.query.get(densityDict['id'])
                except:
                    value=None
                if value:
                    product.densities.append(value)
                    db.session.add(value)
                    editValue(value, densityDict)
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
                except:
                    value=None
                if value and 'field' in foodWasteDict:
                    value.FoodWasteField=FoodWasteField.query.get(foodWasteDict['field'])
                    product.foodWasteData.append(value)
                    db.session.add(value)
                    editValue(value, foodWasteDict)
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
                except:
                    value=None
                if value and 'name' in processDict and 'nutrient' in processDict:
                    try:
                        process = Process.query.filter(Process.name == processDict['name']).all()[0]
                    except:
                        process = None
                    if not process:
                        process = Process()
                        process.name = processDict['name']
                        db.session.add(process)
                    value.Process=process
                    try:
                        nutrient = Nutrient.query.filter(Nutrient.name == processDict['nutrient']).all()[0]
                    except:
                        nutrient = None
                    if not nutrient:
                        nutrient = Nutrient()
                        nutrient.name = processDict['nutrient']
                        db.session.add(nutrient)
                    value.nutrient=nutrient
                    product.processes.append(value)
                    db.session.add(value)
                    editValue(value, processDict)
    #add ProductNutrientAssociation (if not existing) and if necessary create respective Nutrient (side effect)
    if 'nutrients' in jsonData:
        for nutrientDict in jsonData['nutrients']:
             if 'id'  in nutrientDict:
                try:
                    value=ProductNutrientAssociation.query.get(nutrientDict['id'])
                except:
                    value=None
                if value and 'nutrient' in nutrientDict:
                    try:
                        nutrient = Nutrient.query.filter(Nutrient.name == nutrientDict['nutrient']).all()[0]
                    except:
                        nutrient = None
                    if not nutrient:
                        nutrient = Nutrient()
                        nutrient.name = nutrientDict['nutrient']
                        db.session.add(nutrient)
                    value.nutrient=nutrient
                    product.nutrientProcesses.append(value)
                    db.session.add(value)
                    editValue(value, nutrientDict)
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
    if 'processesCo2' in jsonData:
        for processDict in jsonData['processesCo2']:
             if 'id'  in processDict:
                try:
                    value=ProductProcessCO2Association.query.get(processDict['id'])
                except:
                    value=None
                if value and 'name' in processDict:
                    try:
                        process = Process.query.filter(Process.name == processDict['name']).all()[0]
                    except:
                        process = None
                    if not process:
                        process = Process()
                        process.name = processDict['name']
                        db.session.add(process)
                    value.Process=process
                    product.processesCo2.append(value)
                    db.session.add(value)
                    editValue(value, processDict)
           
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
        #TODO: parse date, check, add
        pass
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
                except:
                    value=None
                if value:
                    product.unitWeights.append(value)
                    db.session.add(value)
                    editValue(value, unitWeightDict)
    db.session.add(product)
    db.session.commit()
    return product.id

def editValue(value,valueDict):
    #common fields for values
    if 'amount' in valueDict:
        value.amount = valueDict['amount']
        value.baseValue = None
    if 'unit' in valueDict:
        value.unit = valueDict['unit']
    if 'reference' in valueDict:
        if 'id' in valueDict['reference']:
            try:
                reference = Reference.query.get(valueDict['reference']['id'])
            except:
                reference = None
            if reference:
                value.reference = reference
        elif 'name' in valueDict['reference']:
            try:
                reference = Reference.query.filter(Reference.name == valueDict['reference']['name']).all()[0]
            except:
                reference = None
            if not reference:
                reference = Reference()
                reference.name = valueDict['reference']['name']
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
        value.baseValue = Value.query.get(valueDict['baseValue'])
    #type specific fields
    if not 'type' in valueDict:
        return "no type specified"
        db.session.rollback()
    elif valueDict['type']=='Co2Value' and type(value)==Co2Value:
        # no additonal fields
        pass
    elif valueDict['type']=='FoodWasteData' and type(value)==FoodWasteData and 'field' in valueDict:
        value.FoodWasteField=FoodWasteField.get(valueDict['field'])
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
    db.session.commit()
    return value.id

def editReference(id, jsonData):
    reference = Reference.query.get(id)
    if 'name' in jsonData:
        reference.name = jsonData['name']
    if 'comment' in jsonData:
        reference.comment = jsonData['comment']
    db.session.add(reference)
    db.session.commit
    return reference.id

if __name__ == '__main__':
    app.run()