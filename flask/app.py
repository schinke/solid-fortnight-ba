
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
    return jsonify([a.toDict() for a in EdbProduct.query.all()])

@app.route('/product/<id>', methods=['GET'])
def get_product(id):

    visit = Visits("/product")
    db.session.add(visit)
    db.session.commit()
    intermediate = Product.query.get(id)
    return jsonify(intermediate.toDict())

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
        abort
    else:
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
        for synonym in request.json['synonyms']:
            pass
    if 'tags' in request.json:
        for tag in request.json['tags']:
            pass
    if 'nutrients' in request.json:
        for nutrient in request.json['nutrients']:
            pass
    if 'processes' in request.json:
        for process in request.json['processes']:
            pass
    if 'possibleOrigins' in request.json:
        for origin in request.json['possibleOrigins']:
            pass
    if 'allergenes' in request.json:
        for allergene in request.json['allergenes']:
            pass
    if 'co2Value' in request.json:
        pass
    if 'standardOrigin' in request.json:
        pass
    if 'density' in request.json:
        pass
    if 'unitWeight' in request.json:
        pass
    db.session.add(product)
    db.session.commit()
    return "ok"


@app.route('/<name>')
@auth.login_required
def hello_name(name):
    print(name)



@auth.verify_password
def verify_password(username, password):

    return (username and not password)

if __name__ == '__main__':
    app.run()