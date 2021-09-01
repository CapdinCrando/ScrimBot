from pyairtable import Table
from random import choice

class QuoteApi:
	def __init__(self, key, base_id):
		self.table = Table(key, base_id, 'Quotes')
	def get_all_quotes(self):
		out_data = ""
		for q in self.table.all():
			fields = q['fields']
			out_data += fields['Quote']
			if 'Author' in fields:
				out_data += ' - ' + fields['Author']
			out_data += '\n'
		return out_data
	def get_quote(self):
		fields = choice(self.table.all())['fields']
		quote = fields['Quote']
		if 'Author' in fields:
			quote += '\n\t- ' + fields['Author']
		return quote