
from flask import jsonify, Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import json

auth = HTTPBasicAuth()
import os
"""Provides an API for models, intended for use with javascript and electron"""
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/products', methods=['GET'])
def get_products():

    #TODO: log visits automatically
    visit = Visits("/products")
    db.session.add(visit)
    db.session.commit()
    return jsonify([a.toDict() for a in Product.query.all()])

@app.route('/product/<id>', methods=['GET'])
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

@app.route('/product', methods=['PUT'])
def put_product():
    if 'edb' in request.json:
        if request.json['edb']:
            product = EdbProduct()
        else:
            product=TemplateProduct()
    else:
        product=TemplateProduct()

    if not 'name' in request.json:
        return "name missing"#TODO: add appropriate status code
    else:
        product.name = request.json['name']
    db.session.add(product)
    db.session.commit()
    id=editProduct(product.id,request)
    return str(id)

@app.route('/product/<id>', methods=['POST'])
def post_product(id):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource not found"#TODO: add appropriate status code
    else:
        editProduct(id,request)
    return str(id)


@app.route('/<name>')
@auth.login_required
def hello_name(name):
    print(name)



@auth.verify_password
def verify_password(username, password):

    return (username and not password)


def editProduct(id,request):
    try:
        product = Product.query.get(id)
    except:
        product = None
    if not product:
        return "resource not found"#TODO: add appropriate status code
    if 'name' in request.json:
        product.name = request.json['name']
    if 'specification' in request.json:
        product.specification = request.json['specification']
    if 'englishName' in request.json:
        product.englishName = request.json['englishName']
    if 'frenchName' in request.json:
        product.frenchName = request.json['frenchName']
    if 'alternatives' in request.json:
        for alternativeId in request.json['alternatives']:
            try:
                alternative=Product.query.get(alternativeId)
                product.alternatives.append(alternative)
            except:
                pass
    if 'synonyms' in request.json:
        for synonymName in request.json['synonyms']:
            try:
                synonym=Synonym.query.get(synonymName)
            except:
                synonym=None
            if not synonym:
                synonym=Synonym(synonymName)
                #side effect
                db.session.add(synonym)
            product.synonyms.append(synonym)
    if 'tags' in request.json:
        for tagName in request.json['tags']:
            try:
                tag=Tag.query.get(tagName)
            except:
                tag=None
            if not tag:
                tag=Tag()
                tag.name=tagName
                #side effect
                db.session.add(tag)
            product.tags.append(tag)
    #add ProductNutrientAssociation (if not existing) and if necessary create respective Nutrient (side effect)
    if 'nutrients' in request.json:
        for nutrientDict in request.json['nutrients']:
            if 'name' in nutrientDict and 'amount' in nutrientDict:
                try:
                    nutrient=Nutrient.query.filter(Nutrient.name==nutrientDict['name']).all()[0]
                except:
                    print("nutrient not found")
                    nutrient=None
                if not nutrient:
                    print("created nutrient")
                    nutrient=Nutrient()
                    nutrient.name=nutrientDict['name']
                    db.session.add(nutrient)
                try:
                    association=ProductNutrientAssociation.query.filter(
                        ProductNutrientAssociation.nutrient==nutrient,
                            ProductNutrientAssociation.product==product).all()[0]
                    print(association)
                except:
                    print("association not found")
                    association=None
                if not association:
                    association=ProductNutrientAssociation()
                    db.session.add(association)
                    product.nutrients.append(association)
                    association.nutrient=nutrient
                    print("ProductNutrientAssociation created")
                association.baseValue=[]
                association.amount=nutrientDict['amount']
            elif 'name' in nutrientDict and 'id' in nutrientDict:
                try:
                    value=ProductNutrientAssociation.query.get(id)
                except:
                    value=None
                if value:
                    try:
                        nutrient=Nutrient.query.filter(Nutrient.name==nutrientDict['name']).all()[0]
                    except:
                        print("nutrient not found")
                        nutrient=None
                    if not nutrient:
                        print("created nutrient")
                        nutrient=Nutrient()
                        nutrient.name=nutrientDict['name']
                        db.session.add(nutrient)
                    try:
                        association=ProductNutrientAssociation.query.filter(
                            ProductNutrientAssociation.nutrient==nutrient,
                                ProductNutrientAssociation.product==product).all()[0]
                        print(association)
                    except:
                        association=None
                    if not association:
                        association=ProductNutrientAssociation()
                        association.product=product
                        association.nutrient=nutrient
                        db.session.add(association)
                    association.baseValue=value
    #add ProductProcessNutrientAssociation (if not existing) and if necessary create respective Nutrient and Process (side effect) 
    if 'processes' in request.json:
        for processDict in request.json['processes']:
            if 'name' in processDict and 'nutrient' in processDict\
            and 'amount' in processDict:
                try:
                    process=Process.query.filter(Process.name==processDict['name']).all()[0]
                except:
                    process=None
                if not process:
                    process=Process()
                    process.name=processDict['name']
                    db.session.add(process)
                try:
                    nutrient=Nutrient.query.filter(Nutrient.name==processDict['nutrient']).all()[0]
                except:
                    nutrient=None
                if not nutrient:
                    nutrient=Nutrient()
                    nutrient.name=processDict['nutrient']
                    db.session.add(nutrient)
                try:
                    association=ProductProcessNutrientAssociation.query.filter(
                            ProductProcessNutrientAssociation.process==process,
                            ProductProcessNutrientAssociation.product==product,
                            ProductProcessNutrientAssociation.nutrient==nutrient).all()[0]
                except:
                    association=None
                if not association:
                    association=ProductProcessNutrientAssociation()
                    association.process=process
                    association.product=product
                    association.nutrient=nutrient
                association.amount=processDict['amount']
                db.session.add(association)
            elif 'name' in processDict and 'nutrient' in processDict\
            and 'id' in processDict:
                try:
                    value=ProductProcessNutrientAssociation.query.get(id)
                except:
                    value=None
                if value:
                    try:
                        process=Process.query.filter(Process.name==processDict['name']).all()[0]
                    except:
                        process=None
                    if not process:
                        process=Process()
                        process.name=processDict['name']
                        db.session.add(process)
                    try:
                        nutrient=Nutrient.query.filter(Nutrient.name==processDict['nutrient']).all()[0]
                    except:
                        nutrient=None
                    if not nutrient:
                        nutrient=Nutrient()
                        nutrient.name=processDict['nutrient']
                        db.session.add(nutrient)
                    try:
                        association=ProductProcessNutrientAssociation.query.filter(
                            ProductProcessNutrientAssociation.process==process,
                            ProductProcessNutrientAssociation.product==product,
                            ProductProcessNutrientAssociation.nutrient==nutrient).all()[0]
                        print(association)
                    except:
                        association=None
                    if not association:
                        association=ProductProcessNutrientAssociation()
                        association.product=product
                        association.process=process
                        association.nutrient=nutrient
                        db.session.add(association)
                    association.baseValue=value
            elif 'name' in processDict and 'co2Amount' in processDict:
                try:
                    process=Process.query.filter(Process.name==processDict['name']).all()[0]
                except:
                    process=None
                if not process:
                    process=Process()
                    process.name=processDict['name']
                    db.session.add(process)
                try:
                    association=ProductProcessCo2Association.query.filter(
                        ProductProcessCo2Association.process==process,
                        ProductProcessCo2Association.product==product).all()[0]
                except:
                    association=None
                if not association:
                    association=ProductProcessCo2Association()
                    association.process=process
                    association.product=product
                association.amount=processDict['co2Amount']
                association.baseValue=[]
            elif 'name' in processDict and 'id' in processDict:
                try:
                    value=Value.query.get(id)
                except:
                    value=None
                if value:
                    try:
                        process=Process.query.filter(Process.name==processDict['name']).all()[0]
                    except:
                        process=None
                    if not process:
                        process=Process()
                        process.name=processDict['name']
                        db.session.add(process)
                    try:
                        association=ProductProcessCo2Association.query.filter(
                            ProductProcessCo2Association.process==process,
                            ProductProcessCo2Association.product==product).all()[0]
                    except:
                        association=None
                    if not association:
                        association=ProductProcessCo2Association()
                        association.product=product
                        association.process=process
                        association.baseValue=value
    if 'possibleOrigins' in request.json:
        for originName in request.json['possibleOrigins']:
            try:
                location=Location.query.filter(Location.name==originName).all()[0]
            except:
                location=None
            if not location:
                location=Location()
                location.name=originName
                db.session.add(location)
            if not location in product.possibleOrigins:
                product.possibleOrigins.append(location)
    if 'allergenes' in request.json:
        for allergeneName in request.json['allergenes']:
            try:
                allergene=Allergene.query.filter(Allergene.name==allergeneName).all()[0]
            except:
                allergene=None
            if not allergene:
                allergene=Allergene()
                allergene.name=allergeneName
                db.session.add(allergene)
            try:
                #Check if associated
                association=ProductAllergeneAssociation.query.filter(ProductAllergeneAssociation.product==product, ProductAllergeneAssociation.allergene==allergene).all()[0]
            except:
                association=None
            if not association:
                association=ProductAllergeneAssociation()
                association.product=product
                association.allergene=allergene
                session.add(association)
    if 'co2Value' in request.json:
        if 'id' in request.json['co2Value']:
            try:
                value=Co2Value.query.get(id)
            except:
                value=None
            if value:
                if not product.co2Value:
                    co2Value=Co2Value()
                    co2Value.product=product
                    co2Value.baseValue=value
                    db.session.add(co2Value)
                else:
                    product.co2Value.baseValue=value
        elif 'amount' in request.json['co2Value']:
            if not product.co2Value:
                co2Value=Co2Value()
                co2Value.product=product
                db.session.add(co2Value)
            product.co2Value.amount=request.json['co2Value']['value']
    if 'standardOrigin' in request.json:
        pass
    if 'density' in request.json:
        if 'id' in request.json['density']:
            try:
                value=ProductDensity.query.get(id)
            except:
                value=None
            if value:
                if not product.density:
                    density=ProductDensity
                    product.density=density
                    session.add(density)
                product.density.baseValue=value
        elif 'amount' in request.json['density']:
            if not product.density:
                density=ProductDensity
                product.density=density
                session.add(density)
            product.density.amount=request.json['density']['value']
            product.density.baseValue=[]
    if 'unitWeight' in request.json:
        if 'id' in request.json['unitWeight']:
            try:
                value=ProductUnitWeight.query.get(id)
            except:
                value=None
            if value:
                if not product.density:
                    unitWeight=ProductUnitWeight
                    product.unitWeight=unitWeight
                    session.add(density)
                product.unitWeight.baseValue=value
        elif 'amount' in request.json['unitWeight']:
            if not product.unitWeight:
                unitWeight=ProductDensity
                product.unitWeight=unitWeight
                session.add(unitWeight)
            product.untiWeight.amount=request.json['unitWeight']['value']
            product.unitWeight.baseValue=[]
    db.session.add(product)
    db.session.commit()
    return product.id
if __name__ == '__main__':
    app.run()