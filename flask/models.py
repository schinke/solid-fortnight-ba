import datetime, json, jsonpickle
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


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

class Value(db.Model):
    __tablename__='scivalue'

    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'scivalue',
        'polymorphic_on':type
    }

    id=db.Column(db.Integer, primary_key=True)
    validCountries = relationship("Location", secondary="location_scivalue_association")
    reference_id=db.Column(db.Integer, db.ForeignKey('reference.id'))
    reference=relationship("Reference", back_populates="scivalues")

class Location(db.Model):
    __tablename__='location'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    possibleProducts=relationship("Product", secondary="location_prod_association", back_populates="possibleLocations")

class FoodWasteData(Value):
    __tablename__='foodwaste'
    __mapper_args__ = {
        'polymorphic_identity':'prod_allergene_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="foodWasteData")

class Process(db.Model):
    __tablename__='process'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    #type
    #productAssociation
    #co2
    #nutrient
    #foodwaste?

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

class Co2Value(Value):
    __tablename__='co2'

    __mapper_args__ = {
        'polymorphic_identity':'co2',
    }

    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    scivalue=db.Column(db.String)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="Co2Value")

class Reference(db.Model):
    __tablename__ = 'reference'
    id=db.Column(db.Integer, primary_key=True)
    scivalues=relationship("Value", back_populates="reference")

class TagProductAssociation(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    tag_name= db.Column(db.String, db.ForeignKey('tag.name'), primary_key=True)

class ProductAllergeneAssociation(Value):
    __tablename__ = 'prod_allergene_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_allergene_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=False)
    allergene_id= db.Column(db.Integer, db.ForeignKey('allergene.id'), primary_key=False)
    product=relationship("Product", back_populates="allergenes")

class ProductProcessAssociation(Value):
    __tablename__ = 'prod_process_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_process_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    process_id= db.Column(db.Integer, db.ForeignKey('process.id'))
    product=relationship("Product", back_populates="processes")

class ProductNutrientAssociation(Value):
    __tablename__ = 'prod_nutrient_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_nutrient_association',
    }

    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    nutrient_id= db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    product=relationship("Product", back_populates="nutrients")

class ProductAlternative(db.Model):
    __tablename__ = 'prod_alternatives'
    product_id_1 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product_id_2 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

class LocationProductAssociation(db.Model):
    __tablename__ = 'location_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    location_id= db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)

class LocationValueAssociation(db.Model): #valid for
    __tablename__ = 'location_scivalue_association'
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    scivalue_id= db.Column(db.Integer, db.ForeignKey('scivalue.id'), primary_key=True)

class Product(db.Model):
    __tablename__='product'
    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'product',
        'polymorphic_on':type
    }
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
    #Advanced
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
    processes=relationship("ProductProcessAssociation", back_populates="product")
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

class EdbProduct(Product):
    __tablename__ = 'edb_product'

    __mapper_args__ = {
        'polymorphic_identity':'edb_product',
    }
    id = Column(db.Integer, ForeignKey('product.id'), primary_key=True)

class TemplateProduct(Product):
    __tablename__ = 'template'
    __mapper_args__ = {
        'polymorphic_identity':'template',
    }
    id = Column(db.Integer, ForeignKey('product.id'), primary_key=True)
