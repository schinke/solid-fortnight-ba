import datetime, json, jsonpickle
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

#TODO: add appropriate comment columns
#TODO: add confidence intervals
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

#general purpose value
class Value(db.Model):
    __tablename__='scivalue'

    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'scivalue',
        'polymorphic_on':type
    }
    confidenceInterval=db.Column(db.Integer)
    id=db.Column(db.Integer, primary_key=True)
    validCountries = relationship("Location", secondary="location_scivalue_association")
    reference_id=db.Column(db.Integer, db.ForeignKey('reference.id'))
    reference=relationship("Reference")
    base_value_id=db.Column(db.Integer, db.ForeignKey('scivalue.id'))
    baseValue=relationship("Value")
    amount=db.Column(db.Integer)
    unit=db.Column(db.String)
    def actualValue(self):
        if self.baseValue:
            return self.baseValue.actualValue()
        else:
            return self

#Countries
class Location(db.Model):
    __tablename__='location'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    possibleProducts=relationship("Product", secondary="location_prod_association", back_populates="possibleOrigins")

#A single product's single foodwaste number
class FoodWasteData(Value):
    __tablename__='foodwaste'
    __mapper_args__ = {
        'polymorphic_identity':'foodwaste',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="foodWasteData")

#A process, not tied to a product
class Process(db.Model):
    __tablename__='process'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String())
    description=db.Column(db.String())

#An allergene not tied to a product
class Allergene(db.Model):#single allergene, not multiple allergenes
    __tablename__='allergene'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    shortname=db.Column(db.String)

#A nutrient, not tied to a product
class Nutrient(db.Model):
    __tablename__='nutrient'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    shortname=db.Column(db.String)

#A Tag, to be connected with products
class Tag(db.Model):
    __tablename__='tag'
    name=db.Column(db.String, primary_key=True)

#A Synonym, to be connected with products
class Synonym(db.Model):
    __tablename__ = 'synonym'
    name=db.Column(db.String, primary_key=True)

#A single product's CO2Value
class Co2Value(Value):
    __tablename__='co2'
    __mapper_args__ = {
        'polymorphic_identity':'co2',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    scivalue=db.Column(db.String)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="co2Value")

#A reference, maybe for multiple values
class Reference(db.Model):
    __tablename__ = 'reference'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    comment=db.Column(db.String)
    scivalues=relationship("Value", back_populates="reference")

#Associate products with relevant tags for searching
class TagProductAssociation(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    tag_name= db.Column(db.String, db.ForeignKey('tag.name'), primary_key=True)

#Associate products with relevant tags for searching
class SynonymProductAssociation(db.Model):
    __tablename__ = 'synonym_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    synonym_name= db.Column(db.String, db.ForeignKey('synonym.name'), primary_key=True)

#Associate one allergene to a product
class ProductAllergeneAssociation(Value):
    __tablename__ = 'prod_allergene_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_allergene_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=False)
    allergene_id= db.Column(db.Integer, db.ForeignKey('allergene.id'), primary_key=False)
    product=relationship("Product", back_populates="allergenes")
    allergene=relationship("Allergene")

#Store how much one process changes one nutrient for one product
class ProductProcessNutrientAssociation(Value):
    __tablename__ = 'prod_process_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_process_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    process_id= db.Column(db.Integer, db.ForeignKey('process.id'))
    nutrient_id=db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    nutrient=relationship("Nutrient")
    process=relationship("Process")
    product=relationship("Product", back_populates="processes")

#Store how much one process changes one product's CO2 Value
class ProductProcessCO2Association(Value):
    __tablename__ = 'prod_process_co2_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_process_co2_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    process_id= db.Column(db.Integer, db.ForeignKey('process.id'))
    product=relationship("Product", back_populates="processesCo2")

#Store how much of a nutrient one product has
class ProductNutrientAssociation(Value):
    __tablename__ = 'prod_nutrient_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_nutrient_association',
    }
    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product=relationship("Product", back_populates="nutrients")
    nutrient_id= db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    nutrient=relationship("Nutrient")

class ProductDensity(Value):
    __tablename__ = 'density'
    __mapper_args__ = {
        'polymorphic_identity':'density',
    }

    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product=relationship("Product", back_populates="density")

class ProductUnitWeight(Value):
    __tablename__ = 'unit_weight'
    __mapper_args__ = {
        'polymorphic_identity':'unit_weight',
    }

    id = Column(db.Integer, ForeignKey('scivalue.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product=relationship("Product", back_populates="unitWeight")

#Associate one product to one alternative product
class ProductAlternative(db.Model):
    __tablename__ = 'prod_alternatives'
    product_id_1 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product_id_2 = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

#Associate one product with possible origin locations
class LocationProductAssociation(db.Model):
    __tablename__ = 'location_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    location_id= db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)

#Associate one value to the locations in which it is valid
class LocationValueAssociation(db.Model): #valid for
    __tablename__ = 'location_scivalue_association'
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    scivalue_id= db.Column(db.Integer, db.ForeignKey('scivalue.id'), primary_key=True)

#A food product
class Product(db.Model):
    __tablename__='product'
    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'product',
        'polymorphic_on':type
    }

    # def __init__(self, allergenes, alternatives, englishName, frenchName,
    #     name, nutrients, processes, possibleOrigins, specification,
    #     synonyms, tags, co2Value, standardOrigin, startOfLocalSeason,
    #     endOfLocalSeason, density, unitWeight, commentsOnDensityAndUnitWeight,
    #     texture, foodWasteData, infoTextForCook):
    #     self.name=name
    #     self.allergenes=allergenes
    #     self.alternatives=alternatives
    #     self.englishName=englishName
    #     self.frenchName=frenchName
    #     self.name=name
    #     self.nutrients=nutrients
    #     self.processes=processes
    #     self.possibleOrigins=possibleOrigins
    #     self.specification=specification
    #     self.synonyms=synonyms
    #     self.tags=tags
    #     self.co2Value=co2Value
    #     self.standardOrigin=standardOrigin
    #     self.startOfLocalSeason=startOfLocalSeason
    #     self.endOfLocalSeason=endOfLocalSeason
    #     self.density=density
    #     self.unitWeight=unitWeight
    #     self.commentsOnDensityAndUnitWeight=commentsOnDensityAndUnitWeight
    #     self.texture=texture
    #     self.foodWasteData=foodWasteData
    #     self.infoTextForCook=infoTextForCook
        
    def fromJson(jsonObject):
        product.name = request.json['name']
        product.specification = request.json['specification']
        product.englishName = request.json['englishName']
        product.frenchName = request.json['frenchName']
        product.frenchName = request.json['frenchName']

    def toDict(self):
        response={'id': self.id, 'name': self.name,
        'specification': self.specification,
        'englishName': self.englishName,
        'frenchName':self.frenchName,
        'alternatives':[{'name':product.name, 'id':product.id} for product in self.alternatives],
        'synonyms':[synonym.name for synonym in self.synonyms],
        'tags':[tag.name for tag in self.tags],
        'nutrients':[{'derived': not nutrient.id==nutrient.actualValue().id,'amount':nutrient.amount,'name':nutrient.nutrient.name, } for nutrient in self.nutrients],
        'processes':[{'derived': not process.id==process.actualValue().id,'valueId':process.id, 'name':process.process.name, 'nutrient':process.nutrient.name,'amount':process.amount} for process in self.processes],
        'possibleOrigins':[origin.name for origin in self.possibleOrigins],
        'allergenes':[allergene.allergene.name for allergene in self.allergenes]
        }
        if self.co2Value:
            response['hasCo2Value']=(self.co2Value.actualValue().id==self.co2Value.id())
            response['co2Value']={'derived': not self.co2Value.id==self.co2Value.actualValue().id,
            'id':self.co2Value.id,'amount':self.co2Value.actualValue().amount}
        if self.standardOrigin:
            response['standardOrigin']=self.standardOrigin.name
        if self.density:
            response['density']={'derived': not self.density.id==self.density.actualValue().id,
            'id':self.density.id, 'amount':self.density.amount}
        if self.unitWeight:
            response['unitWeight']={'id':self.unitWeight.id, 'amount':self.unitWeight.amount}
        return response

    id = db.Column(db.Integer, primary_key=True)

    allergenes=relationship("ProductAllergeneAssociation", back_populates="product")
    alternatives=relationship("Product", secondary="prod_alternatives", primaryjoin=id==ProductAlternative.product_id_1,
                       secondaryjoin=id==ProductAlternative.product_id_2)
    englishName=db.Column(db.String())
    frenchName=db.Column(db.String())
    name = db.Column(db.String())
    nutrients=relationship("ProductNutrientAssociation", back_populates="product")
    processes=relationship("ProductProcessNutrientAssociation", back_populates="product")
    processesCo2=relationship("ProductProcessCO2Association", back_populates="product")
    possibleOrigins=relationship("Location", secondary="location_prod_association", back_populates="possibleProducts")
    specification = db.Column(db.String())
    synonyms=relationship("Synonym", secondary="synonym_prod_association")
    tags = relationship("Tag", secondary="tag_prod_association")

    co2Value=relationship("Co2Value", uselist=False, back_populates="product")
    standardOrigin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    standardOrigin=relationship(Location, foreign_keys=standardOrigin_id)
    ##replace multiple fields with processes list
    # productionMethods
    # productionMethodParameters
    # degreesOfProcessing
    # degreesOfProcessingParameters
    # preservationMethods
    # packaging
    # packagingParameters
    # packagingMethods
    
    startOfLocalSeason=db.Column(db.Date())
    endOfLocalSeason=db.Column(db.Date())
    density=relationship("ProductDensity", back_populates="product")
    unitWeight=relationship("ProductUnitWeight", back_populates="product")
    commentsOnDensityAndUnitWeight=db.Column(db.String())
    texture=db.Column(db.String)
    foodWasteData=relationship("FoodWasteData", back_populates="product")
    infoTextForCook=db.Column(db.String())
    # #Documentation
    # co2CalculationPath
    # calculationProcessDocumentation

    # referencesForBasicCO2Value
    # otherReferences
    # commentsOnFoodwasteCO2CalculationPathForDifferentProductParameters
    # dataQualityEstimation

#A food product that's used in the eaternity calculator
class EdbProduct(Product):
    __tablename__ = 'edb_product'

    __mapper_args__ = {
        'polymorphic_identity':'edb_product',
    }
    def toDict(self):
        output=super(EdbProduct, self).toDict()
        output['edb']=True
        return output
    id = Column(db.Integer, ForeignKey('product.id'), primary_key=True)

#A food product prototype, can be seen as category
class TemplateProduct(Product):
    __tablename__ = 'template'
    __mapper_args__ = {
        'polymorphic_identity':'template',
    }
    def toDict(self):
        output=super(TemplateProduct, self).toDict()
        output['edb']=False
        return output
    id = Column(db.Integer, ForeignKey('product.id'), primary_key=True)
