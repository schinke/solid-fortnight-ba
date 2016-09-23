import datetime, json, jsonpickle
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

#TODO: add appropriate comment columns
#TODO: add confidence intervals
#TODO: circular dependencies of values
#TODO: product dependencies and categories
class Visits(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String())
    timestamp = db.Column(db.DateTime())

    def __init__(self, url):
        self.url = url
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return 'id {}'.format(self.id)

#general purpose value
class Value(db.Model):
    __tablename__ = 'scivalue'
    def fromDict(self, data):
        if 'amount' in data:
            self.amount = data['amount']
            self.baseValue = None
        if 'unit' in data:
            self.unit = data['unit']
        if 'reference' in data:
            if 'id' in data['reference']:
                try:
                    reference = Reference.query.get(data['reference']['id'])
                except:
                    reference = None
                if reference:
                    self.reference = reference
            elif 'name' in data['reference']:
                try:
                    reference = Reference.query.filter(Reference.name == data['reference']['name']).all()[0]
                except:
                    reference = None
                if not reference:
                    reference = Reference()
                    reference.name = data['reference']['name']
                self.reference = reference
        if 'baseValue' in data:
            value.baseValue = Value.query.get(data['baseValue'])

    def toDict(self,fields=None):
        output = {
        'id':self.id,
        'validCountries':[location.name for location in self.validCountries],
        'derived':self.id == self.base_value_id,
        'amount':self.actualValue().amount,
        'unit':self.actualValue().unit,
        'type':type(self).__name__,
        'product':self.product_id,
        'comment':self.comment
        }
        if not self.actualValue().id == self.id:
            output['derived'] = True
            output['baseValue'] = self.baseValue.id
        else:
            output['derived'] = False
        if self.reference:
            output['referenceId'] = self.reference.id
            output['reference'] = self.reference.name
        return output
    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'scivalue',
        'polymorphic_on':type,
        
    }
    confidenceInterval = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"))
    validCountries = relationship("Location", secondary = "location_scivalue_association")
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id', ondelete="SET NULL"))
    reference = relationship("Reference", uselist=False)
    base_value_id = db.Column(db.Integer, db.ForeignKey('scivalue.id'))
    baseValue = relationship("Value", uselist = False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String)
    comment = db.Column(db.String)
    def actualValue(self, id=None):
        if id == self.id:
            return self
        if not id:
            id=self.id
        if self.baseValue and not self.id == self.baseValue.id:
            return self.baseValue.actualValue(id)
        else:
            return self

#Countries
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    possibleProducts = relationship("Product", secondary = "location_prod_association", back_populates = "possibleOrigins")

class FoodWasteField(db.Model):
    __tablename__ = 'foodwaste_field'
    name = Column(db.String(), primary_key = True)

#A single product's single foodwaste number
class FoodWasteData(Value):
    __tablename__ = 'foodwaste'
    __mapper_args__ = {
        'polymorphic_identity':'foodwaste',
    }
    def fromDict(self, data):
        super(FoodWasteData, self).toDict(data)
        if 'field' in data:
            self.field=FoodWasteField.query.get(data['field'])

    def toDict(self):
        output = super(FoodWasteData, self).toDict()
        output['field'] = self.field.name
        return output
    field_id = db.Column(db.String(), db.ForeignKey('foodwaste_field.name'))
    field = relationship("FoodWasteField", uselist=False)
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = Column(db.Integer(), ForeignKey('product.id'))
    product = relationship("Product", back_populates = "foodWasteData")

#A process, not tied to a product
class Process(db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer, primary_key = True)
    products = relationship("Product", secondary = "prod_process_association", back_populates = "processes")
    name = db.Column(db.String())
    type=db.Column(db.String())
    description = db.Column(db.String())

    def toDict(self):
        return {'id':self.id, 'name':self.name, 'type':self.type, 'description':self.description}


#An allergene not tied to a product
class Allergene(db.Model):#single allergene, not multiple allergenes
    __tablename__ = 'allergene'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    abbreviation = db.Column(db.String)

    def toDict(self):
        return {'name':self.name, 'abbreviation':self.abbreviation}

#A nutrient, not tied to a product
class Nutrient(db.Model):
    __tablename__ = 'nutrient'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    abbreviation = db.Column(db.String)
    def toDict(self):
        return {'name':self.name, 'abbreviation':self.abbreviation}
#A Tag, to be connected with products
class Tag(db.Model):
    __tablename__ = 'tag'
    name = db.Column(db.String, primary_key = True)

#A Synonym, to be connected with products
class Synonym(db.Model):
    __tablename__ = 'synonym'
    name = db.Column(db.String, primary_key = True)

#A single product's CO2Value
class Co2Value(Value):
    __tablename__ = 'co2'
    __mapper_args__ = {
        'polymorphic_identity':'co2',
        
    }

    def toDict(self):
        output = super(Co2Value, self).toDict()
        return output
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    scivalue = db.Column(db.String)
    #product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates = "co2Values")

#A reference, maybe for multiple values
class Reference(db.Model):
    __tablename__ = 'reference'

    def toDict(self, fields=None):
        response = {'id':self.id,}
        if not fields or (fields and 'name' in fields):
            response['name'] = self.name
        if not fields or (fields and 'comment' in fields):
            response['comment'] = self.comment
        if not fields or (fields and 'values' in fields):
            response['values']=[value.id for value in self.scivalues]
        return response
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    comment = db.Column(db.String)
    scivalues = relationship("Value", back_populates = "reference")

#Associate products with relevant tags for searching
class TagProductAssociation(db.Model):
    __tablename__ = 'tag_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)
    tag_name =  db.Column(db.String, db.ForeignKey('tag.name',), primary_key = True)

#Associate products with relevant tags for searching
class SynonymProductAssociation(db.Model):
    __tablename__ = 'synonym_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)
    synonym_name =  db.Column(db.String, db.ForeignKey('synonym.name'), primary_key = True)

#Associate one allergene to a product
class ProductAllergeneAssociation(Value):
    __tablename__ = 'prod_allergene_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_allergene_association'
    }
    def fromDict(self, data):
        super(ProductAllergeneAssociation, self).fromDict(data)
        if 'allergeneId' in data:
            try:
                allergene=Allergene.query.get(data['allergeneId'])
            except:
                allergene=None
            if not allergene:
                allergene=Allergene()
                allergene.name=data['allergene']
                db.session.add(allergene)
            

    def toDict(self):
        output = super(ProductAllergeneAssociation, self).toDict()
        output['allergeneId'] = self.allergene.id
        output['allergeneName'] = self.allergene.name
        return output

    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key = False)
    allergene_id =  db.Column(db.Integer, db.ForeignKey('allergene.id', ondelete = "CASCADE"), primary_key = False)
    product = relationship("Product", back_populates = "allergenes")
    allergene = relationship("Allergene")

#Store if a process is applicable on a product
class LocationProductAssociation(db.Model):
    __tablename__ = 'prod_process_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete = "CASCADE"), primary_key = True)
    process_id =  db.Column(db.Integer, db.ForeignKey('process.id',ondelete = "CASCADE"), primary_key = True)


#Store how much one process changes one nutrient for one product
class ProductProcessNutrientAssociation(Value):
    __tablename__ = 'prod_process_nutrient_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_process_nutrient_association',
        
    }

    def toDict(self):
        output = super(ProductProcessNutrientAssociation, self).toDict()
        output['processId'] = self.process.id
        output['processName'] = self.process.name
        output['nutrientId'] = self.nutrient.id
        output['nutrientName'] = self.nutrient.name
        return output

    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id',))
    process_id =  db.Column(db.Integer, db.ForeignKey('process.id'))
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    nutrient = relationship("Nutrient")
    process = relationship("Process")
    product = relationship("Product", back_populates = "processesNutrients")

#Store how much one process changes one product's CO2 Value
class ProductProcessCO2Association(Value):
    __tablename__ = 'prod_process_co2_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_process_co2_association',
        
    }
    def toDict(self):
        output = super(ProductProcessCO2Association, self).toDict()
        output['processId'] = self.process.id
        output['processName'] = self.process.name
        return output
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    process_id =  db.Column(db.Integer, db.ForeignKey('process.id', ondelete = "SET NULL"))
    process = relationship("Process")
    product = relationship("Product", back_populates = "processesCo2")

#Store how much of a nutrient one product has
class ProductNutrientAssociation(Value):
    __tablename__ = 'prod_nutrient_association'
    __mapper_args__ = {
        'polymorphic_identity':'prod_nutrient_association',
        
    }

    def toDict(self):
        output = super(ProductNutrientAssociation, self).toDict()
        output['nutrientId'] = self.nutrient.id
        output['nutrientName'] = self.nutrient.name
        return output
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"))
    product = relationship("Product", back_populates = "nutrients")
    nutrient_id =  db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    nutrient = relationship("Nutrient")

class ProductDensity(Value):
    __tablename__ = 'density'
    __mapper_args__ = {
        'polymorphic_identity':'density',
        
    }
    def toDict(self):
        output = super(ProductDensity, self).toDict()
        return output
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = relationship("Product", back_populates = "densities")

class ProductUnitWeight(Value):
    __tablename__ = 'unit_weight'
    __mapper_args__ = {
        'polymorphic_identity':'unit_weight',
        
    }
    def toDict(self):
        output = super(ProductUnitWeight, self).toDict()
        return output
    id = Column(db.Integer, ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = relationship("Product", back_populates = "unitWeights")

#Associate one product to one alternative product
class ProductAlternative(db.Model):
    __tablename__ = 'prod_alternatives'
    product_id_1 = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)
    product_id_2 = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)

#Associate one product with possible origin locations
class LocationProductAssociation(db.Model):
    __tablename__ = 'location_prod_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete = "CASCADE"), primary_key = True)
    location_id =  db.Column(db.Integer, db.ForeignKey('location.id',ondelete = "CASCADE"), primary_key = True)

#Associate one value to the locations in which it is valid
class LocationValueAssociation(db.Model): #valid for
    __tablename__ = 'location_scivalue_association'
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key = True)
    scivalue_id =  db.Column(db.Integer, db.ForeignKey('scivalue.id', ondelete = "CASCADE"), primary_key = True)

#A food product
class Product(db.Model):
    __tablename__ = 'product'
    type = Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'product',
        'polymorphic_on':type,
        
    }

    def fromJson(jsonObject):
        product.name = request.json['name']
        product.specification = request.json['specification']
        product.englishName = request.json['englishName']
        product.frenchName = request.json['frenchName']
        product.frenchName = request.json['frenchName']

    def toDict(self, fields=None):
        response = {'id':self.id}
        if not fields or (fields and 'allergenes' in fields):
            response['allergenes'] = [allergene.toDict() for allergene in self.allergenes]
        if not fields or (fields and 'alternatives' in fields):
            response['alternatives'] = [{'name':product.name, 'id':product.id,} for product in self.alternatives]
        if not fields or (fields and 'commentsOnDensityAndUnitWeight' in fields):
            response['commentsOnDensityAndUnitWeight'] = self.commentsOnDensityAndUnitWeight
        if not fields or (fields and 'co2Values' in fields):
            response['co2Values'] = [value.toDict() for value in self.co2Values]
        if not fields or (fields and 'densities' in fields):
            response['densities'] = [density.toDict() for density in self.densities]
        if not fields or (fields and 'endOfLocalSeason' in fields):
            response['endOfLocalSeason'] = str(self.endOfLocalSeason)
        if not fields or (fields and 'englishName' in fields):
            response['englishName'] = self.englishName
        if not fields or (fields and 'foodWasteData' in fields):
            response['foodWasteData'] = [data.toDict() for data in self.foodWasteData]
        if not fields or (fields and 'frenchName' in fields):
            response['frenchName'] = self.frenchName
        if not fields or (fields and 'infoTextForCook' in fields):
            response['infoTextForCook'] = self.infoTextForCook
        if not fields or (fields and 'name' in fields):
            response['name'] = self.name
        if not fields or (fields and 'nutrients' in fields):
            response['nutrients'] = [nutrient.toDict() for nutrient in self.nutrients]
        if not fields or (fields and 'nutrientProcesses' in fields):
            response['nutrientProcesses'] = [process.toDict() for process in self.processesNutrients]
        if not fields or (fields and 'possibleOrigins' in fields):
            response['possibleOrigins'] = [origin.name for origin in self.possibleOrigins]
        if not fields or (fields and 'processes' in fields):
            response['processes'] = [process.toDict() for process in self.processes]
        if not fields or (fields and 'processesCo2' in fields):
            response['processesCo2'] = [process.toDict() for process in self.processesCo2]
        if not fields or (fields and 'specification' in fields):
            response['specification'] = self.specification
        if not fields or (fields and 'startOfLocalSeason' in fields):
            response['startOfLocalSeason'] = str(self.startOfLocalSeason)
        if not fields or (fields and 'synonyms' in fields):
            response['synonyms'] = [synonym.name for synonym in self.synonyms]
        if not fields or (fields and 'tags' in fields):
            response['tags'] = [tag.name for tag in self.tags]
        if not fields or (fields and 'texture' in fields):
            response['texture'] = self.texture
        if not fields or (fields and 'unitWeights' in fields):
            response['unitWeights'] = [unitWeight.toDict() for unitWeight in self.unitWeights]
        if (not fields or (fields and 'standardOrigin' in fields)) and self.standardOrigin:
            response['standardOrigin'] = self.standardOrigin.name
        fields=[]
        return response

    id = db.Column(db.Integer, primary_key = True)

    allergenes = relationship("ProductAllergeneAssociation", back_populates = "product", passive_deletes = True)
    alternatives = relationship("Product", secondary = "prod_alternatives", primaryjoin = id == ProductAlternative.product_id_1, secondaryjoin = id == ProductAlternative.product_id_2, passive_deletes = True)
    co2Values = relationship("Co2Value", back_populates = "product", passive_deletes = True)
    commentsOnDensityAndUnitWeight = db.Column(db.String())
    densities = relationship("ProductDensity", back_populates = "product", passive_deletes = True)
    endOfLocalSeason = db.Column(db.String())
    englishName = db.Column(db.String())
    foodWasteData = relationship("FoodWasteData", back_populates = "product", passive_deletes = True)
    frenchName = db.Column(db.String())
    infoTextForCook = db.Column(db.String())
    name = db.Column(db.String())
    nutrients = relationship("ProductNutrientAssociation", back_populates = "product", passive_deletes = True)
    possibleOrigins = relationship("Location", secondary = "location_prod_association", back_populates = "possibleProducts", passive_deletes = True)
    processes = relationship("Process", secondary="prod_process_association", back_populates="products")
    processesNutrients = relationship("ProductProcessNutrientAssociation", back_populates = "product", passive_deletes = True)
    processesCo2 = relationship("ProductProcessCO2Association", back_populates = "product", passive_deletes = True)
    specification = db.Column(db.String())
    standardOrigin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    standardOrigin = relationship(Location, foreign_keys = standardOrigin_id)
    startOfLocalSeason = db.Column(db.String())
    synonyms = relationship("Synonym", secondary = "synonym_prod_association", passive_deletes = True)
    tags = relationship("Tag", secondary = "tag_prod_association", passive_deletes = True)
    texture = db.Column(db.String)
    unitWeights = relationship("ProductUnitWeight", back_populates = "product")

#A food product that's used in the eaternity calculator
class EdbProduct(Product):
    __tablename__ = 'edb_product'

    __mapper_args__ = {
        'polymorphic_identity':'edb_product',
    }
    def toDict(self, fields=None):
        output = super(EdbProduct, self).toDict(fields=fields)
        output['edb'] = True
        return output
    id = Column(db.Integer, ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)

#A food product prototype, can be seen as category
class TemplateProduct(Product):
    __tablename__ = 'template'
    __mapper_args__ = {
        'polymorphic_identity':'template',
        
    }
    def toDict(self, fields=None):
        output = super(TemplateProduct, self).toDict(fields=fields)
        output['edb'] = False
        return output
    id = Column(db.Integer, ForeignKey('product.id', ondelete = "CASCADE"), primary_key = True)



