from CoreData import *
from flask.ext.sqlalchemy import SQLAlchemy
import os
from myadmin.views import MyModelView

class ModelGenerator():
	def __init__(self, app=None, db=None, modelURI=None, momURI=None):
		if db is None:
			raise Exception('You mast pass SQLAlchemy instance as db')
		
		self.db = db
		self.types_map = {}
		self.types_map['100']=self.db.SmallInteger
		self.types_map['200']=self.db.Integer
		self.types_map['300']=self.db.BigInteger
		self.types_map['400']=self.db.Float
		self.types_map['500']=self.db.Float
		self.types_map['600']=self.db.Float
		self.types_map['700']=self.db.Text
		self.types_map['800']=self.db.Boolean
		self.types_map['900']=self.db.DateTime
		self.types_map['1000']=self.db.BINARY


		if app is not None:
			self.app = app
			self.init_app(self.app)
		else:
			self.app = None
			if modelURI is None or momURI is None:
				raise Exception('You must pass app or Xcode model file uri and path for compiled model')

			print 'momc %s %s' % (modelURI, momURI)
			os.system('momc %s %s' % (modelURI, momURI))
			self.mom = NSManagedObjectModel.alloc().initWithContentsOfURL_(NSURL.fileURLWithPath_(momURI))

	def init_app(self, app):
		app.config.setdefault('MODEL_URI',None)
		app.config.setdefault('MOM_URI',None)

		modelURI = app.config['MODEL_URI']
		momURI = app.config['MOM_URI']
		if modelURI is None or momURI is None:
			raise Exception('Must set MODEL_URI')

		print 'momc %s %s' % (modelURI, momURI)
		os.system('momc %s %s' % (modelURI, momURI))
		print NSURL.fileURLWithPath_(momURI)
		self.mom = NSManagedObjectModel.alloc().initWithContentsOfURL_(NSURL.fileURLWithPath_('Model.mom'))
		print self.mom

	def compile(self):
		entity_classes={}

		#iterate enitites
		for entity in self.mom.entities():
			entityName = entity.valueForKey_('name').__str__()
			structure = dict(id=self.db.Column(self.db.Integer, primary_key=True))
			defaults = dict()
			for attr in entity.attributesByName():
				attrDesc = entity.attributesByName().objectForKey_(attr)
				attrName = attrDesc.valueForKey_('name').__str__()
				attrDefaultValue = attrDesc.valueForKey_('defaultValue').__str__()
				attrClassStr = attrDesc.valueForKey_('attributeValueClassName').__str__()
				attrType = attrDesc.valueForKey_('attributeType').__str__()
				attrClass = None
				attrClass = self.types_map[attrType]
				
				isOptional = attrDesc.valueForKey_('isOptional')
				
				if attrDefaultValue != 'None': #and 'Number' not in attrClassStr:
					structure[attrName] = self.db.Column(attrClass, nullable=isOptional, server_default=attrDefaultValue)
					if attrType == '500' or attrType == '600' or attrType == '400':
						attrDefaultValue = float(attrDefaultValue)

					defaults[attrName] = dict(default=attrDefaultValue)
				else:
					structure[attrName] = self.db.Column(attrClass, nullable=isOptional)



			entityClass = type(entityName, (self.db.Model,), structure)
			entityAdminClass = type(entityName+'AdminView', (MyModelView,), dict(form_args=defaults))
			entity_classes[entityName]=(entityClass, entityAdminClass)

			#how to add method to class __repr__
			#def __repr__(self):
			#	return entityName + entity.id



		#iterate previouly created entites and their relationships
		for entity in self.mom.entities():
			entityName = entity.valueForKey_('name').__str__()
			for rel in entity.relationshipsByName():
				relationDesc = entity.relationshipsByName().objectForKey_(rel)
				relationName = relationDesc.valueForKey_('name').__str__()
				relationDestEntity = relationDesc.valueForKey_('destinationEntity').valueForKey_('name').__str__()
				minCount = relationDesc.valueForKey_('minCount')
				maxCount = relationDesc.valueForKey_('maxCount')
				isOptional = relationDesc.valueForKey_('isOptional')
				inverseRelationship = relationDesc.valueForKey_('inverseRelationship')

				relationDestEntityClass = entity_classes[relationDestEntity][0]
				entityClass = entity_classes[entityName][0]

				if inverseRelationship:
					pass
				else:
					structure[relationName+'_id'] = self.db.Column(self.db.Integer, self.db.ForeignKey(relationDestEntityClass.id), nullable=isOptional)
					setattr(entityClass, relationName+'_id', structure[relationName+'_id'])

					structure[relationName] = self.db.relationship(relationDestEntityClass)
					setattr(entityClass, relationName, structure[relationName])


		#note: If you would want to have a one-to-one relationship you can pass uselist=False to relationship()
		#code below tested only on one-to-many relationships

		#again iterate entites and their relationships
		#to organize inverse relationships
		for entity in self.mom.entities():
			entityName = entity.valueForKey_('name').__str__()
			for rel in entity.relationshipsByName():
				relationDesc = entity.relationshipsByName().objectForKey_(rel)
				relationName = relationDesc.valueForKey_('name').__str__()
				relationDestEntity = relationDesc.valueForKey_('destinationEntity').valueForKey_('name').__str__()
				minCount = relationDesc.valueForKey_('minCount')
				maxCount = relationDesc.valueForKey_('maxCount')
				isOptional = relationDesc.valueForKey_('isOptional')
				inverseRelationship = relationDesc.valueForKey_('inverseRelationship')
				inverseRelationshipName = inverseRelationship.valueForKey_('name').__str__()

				relationDestEntityClass = entity_classes[relationDestEntity][0]
				entityClass = entity_classes[entityName][0]

				if inverseRelationship:
					#if relationDestEntityClass already has attribte with name inverseRelationship
					#than pass
					#else create relationship

					print relationDesc

					if not getattr(relationDestEntityClass, inverseRelationshipName, None):
						print 'no %s in %s' % (inverseRelationshipName, relationDestEntityClass)
						structure[relationName] = self.db.relationship(relationDestEntityClass, backref=inverseRelationship.valueForKey_('name'))
						setattr(entityClass, relationName, structure[relationName])
						print 'add %s = %s to %s' % (relationName, structure[relationName],entityClass)
						#add entityClass_id to relationDestEntityClass
						structure[inverseRelationshipName+'_id'] = self.db.Column(self.db.Integer, self.db.ForeignKey(entityClass.id), nullable=isOptional)

						print 'add %s =  %s to %s' % (inverseRelationshipName+'_id', structure[inverseRelationshipName+'_id'], relationDestEntityClass)
						setattr(relationDestEntityClass, inverseRelationshipName+'_id', structure[inverseRelationshipName+'_id'])


		return entity_classes	
		

	#momURL = NSURL.fileURLWithPath_("Model.mom")


