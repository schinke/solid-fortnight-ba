
from flask import jsonify, Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import json
auth = HTTPBasicAuth()
import os, sys
""""provides reoccuring functions for the app"""
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

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
                        db.session.add(association)
                    association.baseValue=value

    #add ProductProcessNutrientAssociation (if not existing) and if necessary create respective Nutrient and Prodcess (side effect) 
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
        if product.co2Value:
            co2Value
    if 'standardOrigin' in request.json:
        pass
    if 'density' in request.json:
        pass
    if 'unitWeight' in request.json:
        pass
    db.session.add(product)
    db.session.commit()
    return product.id