from flask.ext.admin.model import BaseModelView
from flask.ext import wtf


class MongoModel(BaseModelView):
    
	def get_pk_value(self, model):
		return str(self.model.mongo_id)


	def scaffold_list_columns(self):
        	exclude = self.excluded_list_columns or []
		colums = [colum for colum in self.model.__class__.get_fields() if colum not in exclude]
		return colums

	def scaffold_sortable_columns(self):
		return None

	def init_search(self):
		return False

	def is_valid_filter(self, filter):
		return True

	def scaffold_filters(self, name):
		return None


	def scaffold_form(self):
		class MyForm(wtf.Form):
		    pass

		# Do something
		return MyForm
