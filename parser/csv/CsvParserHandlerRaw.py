from CsvParserHandlerBase import CCsvParserHandlerBase
from inspect import currentframe, getframeinfo
# from core.db_connectors import loadSession

def lineno():
	frameinfo = getframeinfo(currentframe())
	return str(frameinfo)


class CCsvParserHandlerRaw(CCsvParserHandlerBase):
	def __init__(self, sql_execution, file_name, csv_file_iterator=None, start_line_to_read=0, delimiter=';'):
		super(CCsvParserHandlerRaw, self).__init__(file_name, csv_file_iterator, start_line_to_read, delimiter)
		self._sql_execution = sql_execution

	def _insert_tm_part(self, insert_dict):
		prepeared_string = "INSERT INTO tm_part (%(keys)s) VALUES (%(parameters)s) RETURNING id;" \
						   % self.__get_insert_value_parameters(insert_dict)
		insert_statement = prepeared_string % insert_dict
		result = self._sql_execution(lineno=str(lineno()), ssql=insert_statement)
		# session = loadSession()
		# result = session.execute(insert_statement.decode('utf-8'))
		id = None
		for row in result:
			id = row['id']
		# session.commit()
		return id

	def _insert_tm_part2part(self, insert_dict):
		prepeared_string = "INSERT INTO tm_part2part (%(keys)s) VALUES (%(parameters)s) RETURNING id;" \
						   % self.__get_insert_value_parameters(insert_dict)
		insert_statement = prepeared_string % insert_dict
		result = self._sql_execution(lineno=str(lineno()), ssql=insert_statement)
		# session = loadSession()
		# result = session.execute(insert_statement.decode('utf-8'))
		id = None
		for row in result:
			id = row['id']
		return id

	def _insert_tm_products_specification(self, file_name, tm_part_id, sdo='SDO'):

		insert_dict = {
			'name' : file_name,
			'sdo': sdo,
		}

		prepeared_string = "INSERT INTO tm_products_specification (%(keys)s) VALUES (%(parameters)s) RETURNING objectid;" \
						   % self.__get_insert_value_parameters(insert_dict)
		insert_statement = prepeared_string % insert_dict
		# session = loadSession()
		# result = session.execute(insert_statement.decode('utf-8'))
		result = self._sql_execution(lineno=str(lineno()), ssql=insert_statement)
		id = None
		for row in result:
			id = row['objectid']

		# if self._insert_tm_prodspecid_productid({
		# 	  'prodspec_id': id,
		# 	  'product_id': tm_part_id
		# }):
			# session.commit()
		self._insert_tm_prodspecid_productid({
			'prodspec_id': id,
			'product_id': tm_part_id
		})
		return id

	def _insert_tm_prodspecid_productid(self, insert_dict):
		prepeared_string = "INSERT INTO tm_prodspecid_productid (%(keys)s) VALUES (%(parameters)s);" \
						   % self.__get_insert_value_parameters(insert_dict)
		insert_statement = prepeared_string % insert_dict
		# session = loadSession()
		# result = session.execute(insert_statement.decode('utf-8'))
		# session.commit()
		result = self._sql_execution(lineno=str(lineno()), ssql=insert_statement)
		return result

	def __get_insert_value_parameters(self, insert_dict):
		parameters_string = ''
		keys_string = ''

		for key in insert_dict.keys():
			keys_string += key + ', '

		for key, value in insert_dict.iteritems():
			literal = '\'%(' + key + ')s\''
			if isinstance(value, int):
				literal = '%(' + key + ')d'
			if isinstance(value, bool):
				literal = '\'%(' + key + ')s\''
			parameters_string += literal + ', '

		return {'keys': keys_string[0: -2],
				'parameters': parameters_string[0: -2]}