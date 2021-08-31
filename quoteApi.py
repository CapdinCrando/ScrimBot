from pyairtable import Table
from random import choice

class QuoteApi:
	def __init__(self, key, base_id):
		self.table = Table(key, base_id, 'Quotes')
	def get_all_quotes(self):
		return self.table.all()
	def get_quote(self):
		return choice(self.get_all_quotes())
	def get_formatted_quote(self):
		fields = self.get_quote()['fields']
		quote = fields['Quote']
		if 'Author' in fields:
			quote += '\n\t- ' + fields['Author']
		return quote