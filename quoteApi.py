from pyairtable import Table
from random import choice

class QuoteApi:
	def __init__(self, key, base_id):
		self.table = Table(key, base_id, 'Quotes')
	def get_formatted_quote(self):
		fields = choice(self.table.all())['fields']
		quote = fields['Quote']
		if 'Author' in fields:
			quote += '\n\t- ' + fields['Author']
		return quote