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

class TagProductAssociation(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    tag_name= db.Column(db.String, db.ForeignKey('tag.name'), primary_key=True)


class ProductAllergeneAssociation(db.Model):
    __tablename__ = 'prod_allergene_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    allergene_id= db.Column(db.Integer, db.ForeignKey('allergene.id'), primary_key=True)
    product=relationship("Product", back_populates="allergenes")
    valueBase_id = db.Column(db.Integer, db.ForeignKey('value_base.id'))
    valueBase=relationship('ValueBase')

class ProductNutrientAssociation(db.Model):
    __tablename__ = 'prod_nutrient_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    allergene_id= db.Column(db.Integer, db.ForeignKey('allergene.id'), primary_key=True)
    product=relationship("Product", back_populates="nutrients")
    valueBase_id = db.Column(db.Integer, db.ForeignKey('value_base.id'))
    valueBase=relationship('ValueBase')

class ProductAlternative(db.Model):
    __tablename__ = 'prod_alternatives'
    product_id_1 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product_id_2 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

class LocationProductAssociation(db.Model):
    __tablename__ = 'location_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    location_id= db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)

class LocationValueAssociation(db.Model): #possible origins
    __tablename__ = 'location_value_association'
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    value_base_id= db.Column(db.Integer, db.ForeignKey('value_base.id'), primary_key=True)

class Location(db.Model):
    __tablename__='location'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    possibleProducts=relationship("Product", secondary="location_prod_association", back_populates="possibleLocations")

class FoodWasteData(db.Model):
    __tablename__='foodwaste'
    id=db.Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="foodWasteData")

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
    Co2Value=relationship("Co2Value", uselist=False, back_populates="product")
    tags = relationship("Tag", secondary="tag_prod_association")
    nutrients=relationship("ProductNutrientAssociation", back_populates="product")
    allergenes=relationship("ProductAllergeneAssociation", back_populates="product")
    # #Advanced
    alternatives=relationship("Product", secondary="prod_alternatives", primaryjoin=id==ProductAlternative.product_id_1,
                           secondaryjoin=id==ProductAlternative.product_id_2)
    standardOrigin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    standardOrigin=relationship(Location, foreign_keys=standardOrigin_id)
    possibleLocations=relationship("Location", secondary="location_prod_association", back_populates="possibleProducts")
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
    # texture
    foodWasteData=relationship("FoodWasteData", back_populates="product")
    # commentsOnFoodwaste

    # #Documentation
    # co2CalculationPath
    # calculationProcessDocumentation
    # infoTextForCook
    # referencesForBasicCO2Value
    # otherReferences
    # commentsOnFoodwasteCO2CalculationPathForDifferentProductParameters
    # dataQualityEstimation

class Process(db.Model):
    __tablename__='process'
    id=db.Column(db.Integer, primary_key=True)

class Allergene(db.Model):#single allergene, not multiple allergenes
    __tablename__='allergene'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    shortname=db.Column(db.String)

class Nutrient(db.Model):
    __tablename__='nutrient'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    shortname=db.Column(db.String)

class Tag(db.Model):
    __tablename__='tag'
    name=db.Column(db.String, primary_key=True)

class ValueBase(db.Model):
    __tablename__='value_base'
    id=db.Column(db.Integer, primary_key=True)
    validCountries = relationship("Location", secondary="location_value_association")

class Co2Value(db.Model):
    __tablename__='co2'
    id=db.Column(db.Integer, primary_key=True)
    value=db.Column(db.String)
    valueBase_id = db.Column(db.Integer, db.ForeignKey('value_base.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="Co2Value")

class Reference(db.Model):
    __tablename__ = 'reference'
    id=db.Column(db.Integer, primary_key=True)

