
from flask import jsonify, Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import json
import controller
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
    id=controller.editProduct(product.id,request)
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
        controller.editProduct(id,request)
    return str(id)


@app.route('/<name>')
@auth.login_required
def hello_name(name):
    print(name)



@auth.verify_password
def verify_password(username, password):

    return (username and not password)

if __name__ == '__main__':
    app.run()