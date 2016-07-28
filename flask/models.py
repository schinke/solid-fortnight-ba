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

class Tag_Product_association(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    tag_name= db.Column(db.String, db.ForeignKey('tag.name'), primary_key=True)

class Product_alternative(db.Model):
    __tablename__ = 'prod_alternatives'
    product_id_1 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product_id_2 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

class Co2_Product_association(db.Model):
    __tablename__ = 'co2_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    co2_id= db.Column(db.Integer, db.ForeignKey('co2.id'), primary_key=True)

class Location_Product_association(db.Model):
    __tablename__ = 'location_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    location_id= db.Column(db.Integer, db.ForeignKey('location.id'))

class Location(db.Model):
    __tablename__='location'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    possibleOrigins=relationship("Product", secondary="location_prod_association")

class FoodWasteData(db.Model):
    __tablename__='foodwaste'
    id=db.Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="foodWastes")

class Product(db.Model):
    __tablename__='product'

    def toDict(self):
        return {'id': self.id, 'name': self.name, 'specification': self.specification}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    specification = db.Column(db.String())
    # synonyms=relationship("Synonym", secondary="synonym_prod_association")
    englishName=db.Column(db.String())
    frenchName=db.Column(db.String())
    Co2Values=relationship("Co2Value")
    tags = relationship("Tag", secondary="tag_prod_association")


    # #Advanced
    alternatives=relationship("Product", secondary="prod_alternatives", primaryjoin=id==Product_alternative.product_id_1,
                           secondaryjoin=id==Product_alternative.product_id_2)
    standardOrigin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    standardOrigin=relationship(Location, foreign_keys=standardOrigin_id)
    possibleOrigins=relationship("Location", secondary="location_prod_association")
    # productionMethods
    # productionMethodParameters
    # degreesOfProcessing
    # degreesOfProcessingParameters
    # preservationMethods
    # packaging
    # packagingParameters
    # packagingMethods
    startOfLocalSeason=db.Column(db.Date)
    endOfLocalSeason=db.Column(db.Date)
    # density
    # unitWeight
    # commentsOnDensityAndUnitWeight
    # referencesOndensityAndUnitWeight
    # Texture
    foodWastes=relationship("FoodWasteData")
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
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="Co2Values")

# class CO2ValueDerived(Co2Value):

# class CO2ValueBase(Co2Value):

# class Reference(db.Model)
#     __tablename__ = 'reference'

