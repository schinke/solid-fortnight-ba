
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
def put_product():
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
def post_product(id):
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

@app.route('/values/<id>', methods = ['PUT'])
def post_value(id):
    try:
        value = Value.query.get(id)
    except:
        value = None
    if not value:
        return "resource not found"#TODO: add appropriate status code
    else:
        editValue(value.id,request.json)
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
def post_reference(id):
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
        for allergeneDict in (a for a in jsonData['allergenes'] if 'name' in a):
            try:
                allergene = Allergene.query.filter(Allergene.name == allergeneDict['name']).all()[0]
            except:
                allergene = None
            if not allergene:
                allergene = Allergene()
                allergene.name = allergeneDict['name']
                db.session.add(allergene)
            try:
                #Check if associated
                association = ProductAllergeneAssociation.query.filter(ProductAllergeneAssociation.product == product, ProductAllergeneAssociation.allergene == allergene).all()[0]
            except:
                association = None
            if not association:
                association = ProductAllergeneAssociation()
                association.product = product
                association.allergene = allergene
                db.session.add(association)
    if 'alternatives' in jsonData:
        for alternative in jsonData['alternatives']:
            try:
                alternative = Product.query.get(alternative['id'])
                if not alternative in product.alternatives:
                    product.alternatives.append(alternative)
            except:
                pass
    if 'co2Value' in jsonData:
        if 'baseValue' in jsonData['co2Value']:
            try:
                value = Co2Value.query.get(jsonData['co2Value']['baseValue'])
            except:
                value = None
            if value:
                if not product.co2Value:
                    co2Value = Co2Value()
                    co2Value.product = product
                    co2Value.baseValue = value
                    db.session.add(co2Value)
                else:
                    product.co2Value.baseValue = value
        elif 'amount' in jsonData['co2Value']:
            if not product.co2Value:
                co2Value = Co2Value()
                product.co2Value = co2Value
                db.session.add(co2Value)
            product.co2Value.baseValue = None
            product.co2Value.amount = jsonData['co2Value']['amount']
    if 'commentsOnDensityAndUnitWeight' in jsonData:
        product.commentsOnDensityAndUnitWeight=jsonData['commentsOnDensityAndUnitWeight']
    if 'density' in jsonData:
        if 'baseValue' in jsonData['density']:
            try:
                value = ProductDensity.query.get(jsonData['density']['baseValue'])
            except:
                value = None
            if value:
                if not product.density:
                    density = ProductDensity
                    product.density = density
                    session.add(density)
                product.density.baseValue = value
        elif 'amount' in jsonData['density']:
            if not product.density:
                density = ProductDensity
                product.density = density
                session.add(density)
            product.density.amount = jsonData['density']['value']
            product.density.baseValue = None
    if 'endOfLocalSeason' in jsonData:
        #TODO: parse date, check, add
        pass
    if 'englishName' in jsonData:
        product.englishName = jsonData['englishName']
    if 'foodWasteData' in jsonData:
        for element in jsonData['foodWasteData']:
            if 'field' in element and 'amount' in element:
                try:
                    field = FoodWasteField.query.get(element['field'])
                except:
                    field = None
                if not field:
                    field=FoodWasteField()
                    field.name=element['field']
                    db.session.add(field)
                try:
                    foodWaste = FoodWasteData.query.filter(FoodWasteData.field == field, FoodWasteData.product==product).all()[0]
                except:
                    foodWaste = None
                if not foodWaste:
                    foodWaste = FoodWasteData()
                    foodWaste.field = field
                    foodWaste.product=product
                    db.session.add(foodWaste)
                foodWaste.amount=element['amount']
    if 'frenchName' in jsonData:
        product.frenchName = jsonData['frenchName']
    if 'infoTextForCook' in jsonData:
        product.infoTextForCook = jsonData['infoTextForCook']
    if 'name' in jsonData:
        product.name = jsonData['name']
        #add ProductProcessNutrientAssociation (if not existing) and if necessary create respective Nutrient and Process (side effect) 
    if 'nutrientProcesses' in jsonData:
        for processDict in jsonData['nutrientProcesses']:
            if 'name' in processDict and 'nutrient' in processDict\
            and 'baseValue' in processDict:
                try:
                    value = ProductProcessNutrientAssociation.query.get(processDict['baseValue'])
                except:
                    value = None
                if value:
                    try:
                        process = Process.query.filter(Process.name == processDict['name']).all()[0]
                    except:
                        process = None
                    if not process:
                        process = Process()
                        process.name = processDict['name']
                        db.session.add(process)
                    try:
                        nutrient = Nutrient.query.filter(Nutrient.name == processDict['nutrient']).all()[0]
                    except:
                        nutrient = None
                    if not nutrient:
                        nutrient = Nutrient()
                        nutrient.name = processDict['nutrient']
                        db.session.add(nutrient)
                    try:
                        association = ProductProcessNutrientAssociation.query.filter(
                            ProductProcessNutrientAssociation.process == process,
                            ProductProcessNutrientAssociation.product == product,
                            ProductProcessNutrientAssociation.nutrient == nutrient).all()[0]
                        print(association)
                    except:
                        association = None
                    if not association:
                        association = ProductProcessNutrientAssociation()
                        association.product = product
                        association.process = process
                        association.nutrient = nutrient
                        db.session.add(association)
                    association.baseValue = value
            elif 'name' in processDict and 'nutrient' in processDict\
            and 'amount' in processDict:
                try:
                    process = Process.query.filter(Process.name == processDict['name']).all()[0]
                except:
                    process = None
                if not process:
                    process = Process()
                    process.name = processDict['name']
                    db.session.add(process)
                try:
                    nutrient = Nutrient.query.filter(Nutrient.name == processDict['nutrient']).all()[0]
                except:
                    nutrient = None
                if not nutrient:
                    nutrient = Nutrient()
                    nutrient.name = processDict['nutrient']
                    db.session.add(nutrient)
                try:
                    association = ProductProcessNutrientAssociation.query.filter(
                            ProductProcessNutrientAssociation.process == process,
                            ProductProcessNutrientAssociation.product == product,
                            ProductProcessNutrientAssociation.nutrient == nutrient).all()[0]
                except:
                    association = None
                if not association:
                    association = ProductProcessNutrientAssociation()
                    association.process = process
                    association.product = product
                    association.nutrient = nutrient
                association.amount = processDict['amount']
                db.session.add(association)
    #add ProductNutrientAssociation (if not existing) and if necessary create respective Nutrient (side effect)
    if 'nutrients' in jsonData:
        for nutrientDict in jsonData['nutrients']:
            if 'name' in nutrientDict and 'baseValue' in nutrientDict:
                try:
                    value = ProductNutrientAssociation.query.get(nutrientDict['baseValue'])
                except:
                    value = None
                if value:
                    # find nutrient
                    try:
                        nutrient = Nutrient.query.filter(Nutrient.name == nutrientDict['name']).all()[0]
                    except:
                        print("nutrient not found")
                        nutrient = None
                    if not nutrient:
                        print("created nutrient")
                        nutrient = Nutrient()
                        nutrient.name = nutrientDict['name']
                        db.session.add(nutrient)
                    # see if prod and nutrient are already associated
                    try:
                        association = ProductNutrientAssociation.query.filter(
                            ProductNutrientAssociation.nutrient == nutrient,
                                ProductNutrientAssociation.product == product).all()[0]
                    except:
                        association = None
                    # otherwise associate them
                    if not association:
                        association = ProductNutrientAssociation()
                        association.product = product
                        association.nutrient = nutrient
                        db.session.add(association)
                    association.baseValue = value
            elif 'name' in nutrientDict and 'amount' in nutrientDict:
                try:
                    nutrient = Nutrient.query.filter(Nutrient.name == nutrientDict['name']).all()[0]
                except:
                    print("nutrient not found")
                    nutrient = None
                if not nutrient:
                    print("created nutrient")
                    nutrient = Nutrient()
                    nutrient.name = nutrientDict['name']
                    db.session.add(nutrient)
                try:
                    association = ProductNutrientAssociation.query.filter(
                        ProductNutrientAssociation.nutrient == nutrient,
                            ProductNutrientAssociation.product == product).all()[0]
                except:
                    print("association not found")
                    association = None
                if not association:
                    association = ProductNutrientAssociation()
                    db.session.add(association)
                    product.nutrients.append(association)
                    association.nutrient = nutrient
                    print("ProductNutrientAssociation created")
                association.baseValue = None
                association.amount = nutrientDict['amount']
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
            if 'name' in processDict and 'baseValue' in processDict:
                try:
                    value = Value.query.get(processDict['baseValue'])
                except:
                    value = None
                if value:
                    try:
                        process = Process.query.filter(Process.name == processDict['name']).all()[0]
                    except:
                        process = None
                    if not process:
                        process = Process()
                        process.name = processDict['name']
                        db.session.add(process)
                    try:
                        association = ProductProcessCo2Association.query.filter(
                            ProductProcessCO2Association.process == process,
                            ProductProcessCO2Association.product == product).all()[0]
                    except:
                        association = None
                    if not association:
                        association = ProductProcessCO2Association()
                        association.product = product
                        association.process = process
                        association.baseValue = value
            elif 'name' in processDict and 'amount' in processDict:
                try:
                    process = Process.query.filter(Process.name == processDict['name']).all()[0]
                except:
                    process = None
                if not process:
                    process = Process()
                    process.name = processDict['name']
                    db.session.add(process)
                try:
                    association = ProductProcessCO2Association.query.filter(
                        ProductProcessCO2Association.process == process,
                        ProductProcessCO2Association.product == product).all()[0]
                except:
                    association = None
                if not association:
                    association = ProductProcessCO2Association()
                    association.process = process
                    association.product = product
                association.amount = processDict['amount']
                association.baseValue = None
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
    if 'unitWeight' in jsonData:
        if 'baseValue' in jsonData['unitWeight']:
            try:
                value = ProductUnitWeight.query.get(jsonData['unitWeight']['baseValue'])
            except:
                value = None
            if value:
                if not product.density:
                    unitWeight = ProductUnitWeight()
                    product.unitWeight = unitWeight
                    session.add(density)
                product.unitWeight.baseValue = value
        elif 'amount' in jsonData['unitWeight']:
            if not product.unitWeight:
                unitWeight = ProductDensity
                product.unitWeight = unitWeight
                session.add(unitWeight)
            product.untiWeight.amount = jsonData['unitWeight']['value']
            product.unitWeight.baseValue = None
    db.session.add(product)
    db.session.commit()
    return product.id

def editValue(id,jsonData):
    value = Value.query.get(id)
    if 'amount' in jsonData:
        value.amount = jsonData['amount']
        value.baseValue = None
    if 'unit' in jsonData:
        value.unit = jsonData['unit']
    if 'reference' in jsonData:
        if 'id' in jsonData['reference']:
            try:
                reference = Reference.query.get(jsonData['reference']['id'])
            except:
                reference = None
            if reference:
                value.reference = reference
        elif 'name' in jsonData['reference']:
            try:
                reference = Reference.query.filter(Reference.name == jsonData['reference']['name']).all()[0]
            except:
                reference = None
            if not reference:
                reference = Reference()
                reference.name = jsonData['reference']['name']
                value.reference = reference
                db.session.add(reference)
    if 'baseValue' in jsonData:
        value.baseValue = Value.query.get(jsonData['baseValue'])
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