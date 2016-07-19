import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON


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
#     #Product prototype

# class Product(db.Model):
#     __tablename__='product'

#     id = db.Column(db.integer, primary_key=True)
#     name = db.Column(db.String())
#     specification = db.Column(db.String())
#     synonyms=db.Column(db.sqlalchemy.types.ARRAY(db.String()))
#     englishName=db.Column(db.String())
#     frenchName=db.Column(db.String())

#     # #Advanced
#     # tags
#     # alternatives
#     # standardOrigin
#     # possibleOrigins
#     # productionMethods
#     # productionMethodParameters
#     # degreesOfProcessing
#     # degreesOfProcessingParameters
#     # preservationMethods
#     # packaging
#     # packagingParameters
#     # packagingMethods
#     # startOfLocalSeason
#     # endOfLocalSeason
#     # density
#     # unitWeight
#     # commentsOnDensityAndUnitWeight
#     # referencesOndensityAndUnitWeight
#     # Texture
#     # Foodwaste
#     # CommentsOnFoodwaste
#     # Allergenes

#     # #Documentation
#     # CO2CalculationPath
#     # CalculationProcessDocumentation
#     # InfoTextForCook
#     # ReferencesForBasicCO2Value
#     # OtherReferences
#     # CommentsOnFoodwasteCO2CalculationPathForDifferentProductParameters
#     # DataQualityEstimation

# class FoodWasteCollection(db.Model)
#     __tablename__ = 'foodwaste'
#     product=db.Column(db.ForeignKey)
#     productionAvoidable = db.Column(db.integer())

# class Value(db.Model)
#     __tablename__ = 'value'

# class ValueBase(Co2Value)
#     __tablename__ = 'base'

# class ValueDerived(Co2Value)
#     __tablename__ = 'derived'

# class Co2Value(Value)

# class 

# class Reference(db.Model)
#     __tablename__ = 'reference'

#TODO: many to many Reference <-> Value

