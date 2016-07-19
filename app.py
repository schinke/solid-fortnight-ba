from flask import Flask
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


@app.route('/')
def hello():
    import time
    visit=Visits("/")
    db.session.add(visit)
    db.session.commit()
    time.sleep(5)
    return json.dumps(([str(a.__repr__()) for a in Visits.query.all()]), indent=4)

@app.route('/<name>')
@auth.login_required
def hello_name(name):
	print(name)



@auth.verify_password
def verify_password(username, password):

    return (username and not password)

if __name__ == '__main__':
    app.run()
