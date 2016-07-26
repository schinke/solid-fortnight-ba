import datetime, json, jsonpickle
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()


class Visits(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    timestamp = db.Column(db.DateTime())

    def __init__(self, url):
        self.url = url
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return 'id {}'.format(self.id)

# class Category(db.Model):
    #Product prototype

class Tag_Product_association(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    tag_name= db.Column(db.String, db.ForeignKey('tag.name'), primary_key=True)

class Co2_Product_association(db.Model):
    __tablename__ = 'co2_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    co2_id= db.Column(db.Integer, db.ForeignKey('co2.id'), primary_key=True)

class Product(db.Model):
    __tablename__='product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    specification = db.Column(db.String())
    # synonyms=db.Column(db.sqlalchemy.types.ARRAY(db.String()))
    englishName=db.Column(db.String())
    frenchName=db.Column(db.String())
    tags = relationship("Tag", secondary="tag_prod_association")

    def __repr__(self):
        return jsonpickle.encode(self.__dict__)
    # #Advanced
    # alternatives
    # standardOrigin
    # possibleOrigins
    # productionMethods
    # productionMethodParameters
    # degreesOfProcessing
    # degreesOfProcessingParameters
    # preservationMethods
    # packaging
    # packagingParameters
    # packagingMethods
    # startOfLocalSeason
    # endOfLocalSeason
    # density
    # unitWeight
    # commentsOnDensityAndUnitWeight
    # referencesOndensityAndUnitWeight
    # Texture
    # Foodwaste
    # CommentsOnFoodwaste
    # Allergenes

    # #Documentation
    # CO2CalculationPath
    # CalculationProcessDocumentation
    # InfoTextForCook
    # ReferencesForBasicCO2Value
    # OtherReferences
    # CommentsOnFoodwasteCO2CalculationPathForDifferentProductParameters
    # DataQualityEstimation

# class FoodWasteCollection(db.Model):
#     __tablename__ = 'foodwaste'
#     product=db.Column(db.ForeignKey)
#     productionAvoidable = db.Column(db.integer())

class Tag(db.Model):
    __tablename__='tag'

    name=db.Column(db.String, primary_key=True)

class Co2Value(db.Model):
    __tablename__='co2'
    id=db.Column(db.Integer, primary_key=True)
    value=db.Column(db.String)

# class CO2ValueDerived(Co2Value):

# class CO2ValueBase(Co2Value):

# class Reference(db.Model)
#     __tablename__ = 'reference'

