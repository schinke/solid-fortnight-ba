from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import json
auth = HTTPBasicAuth()
import os


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

    return json.dumps(([str(a.__repr__()) for a in Product.query.all()]), indent = 4)

@app.route('/products', methods=['POST'])
def post_product():
    product = Product()
    product.name = request.json['name']
    product.specification = request.json['specification']
    product.englishName = request.json['englishName']
    product.frenchName = request.json['frenchName']
    db.session.add(product)
    db.session.commit()


@app.route('/<name>')
@auth.login_required
def hello_name(name):
	print(name)



@auth.verify_password
def verify_password(username, password):

    return (username and not password)

if __name__ == '__main__':
    app.run()
