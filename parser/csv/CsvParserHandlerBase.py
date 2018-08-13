# -*- coding: utf-8 -*-

import csv
from datetime import datetime

def update(d, u):
	for k, v in u.iteritems():
		if isinstance(v, dict):
			r = update(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = u[k]
	return d

def position_to_list(position_string):
	return map(int, position_string.strip('*').split('.'))


class CCsvParserHandlerBase(object):
	def __init__(self, file_name, csv_file_iterator=None, start_line_to_read=0, delimiter=';'):
		self.__file_name = file_name
		self.__csv_file_iterator = csv_file_iterator
		self.__structure = {}
		self.__start_line_to_read = start_line_to_read
		self.__delimiter = delimiter
		self.__csv_keys = [
			'position', 'amount', 'name', 'name1', 'articlenr',
			'gabarit', 'stuff', 'din', 'manufacturer', 'htn']

	@property
	def structure(self):
		return self.__structure

	def parse(self):
		for line_number, row in enumerate(self.__open_file_to_iterator()):
			if line_number < self.__start_line_to_read:
				continue
			print row
			self.__create_structure(position_to_list(row[0]), row)

	def put_to_database(self, inner_dict=None, parent=0, parent_position=''):

		if not inner_dict:  # first call of function
			tm_part_id = self.__create_TmPart([], False, 'root', self.__file_name)
			self._insert_tm_products_specification(self.__file_name, tm_part_id)
			self.put_to_database(self.__structure, tm_part_id)
			# self._sql_session.commit() # TODO here must be commit if necessary
			return tm_part_id

		for key, item in inner_dict.iteritems():
			if key in ['data']:
				continue
			data = item.get('data', [])
			position = str(key)
			if parent_position:
				position = parent_position + '.' + str(key)
			tm_part_id = self.__create_TmPart(data, self.__is_single_part(item), position)
			self.__create_TmPart2part(parent, tm_part_id)
			self.put_to_database(item, tm_part_id, position)

	def __create_structure(self, position_list, data):
		structure_dict = {}
		for step, item in enumerate(reversed(position_list)):
			if step == 0:
				structure_dict = {item: {'data': data}}
			else:
				structure_dict = {item: structure_dict}
		update(self.__structure, structure_dict)

	def __open_file_to_iterator(self):
		if not self.__csv_file_iterator:
			self.__csv_file_iterator = file(self.__file_name)

		if not self.__file_name:
			self.__file_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		return csv.reader(self.__csv_file_iterator, delimiter=self.__delimiter)

	def __convert_csv_list_to_dict(self, data):
		return_dict = {}
		for index, value in enumerate(data):
			return_dict[self.__csv_keys[index]] = value
		return return_dict

	def __is_single_part(self, item):
		return_value = False
		if item.get('data') and len(item) == 1:
			return_value = True
		return return_value

	def __create_TmPart(self, data, single_part=False, position='root', root_name=None):
		insert_dict = self.__convert_csv_list_to_dict(data)
		if root_name:
			insert_dict['name'] = root_name
		insert_dict['position'] = position
		insert_dict['is_single_part'] = single_part
		insert_dict['is_assembly_unit'] = not single_part
		return self._insert_tm_part(insert_dict)

	def __create_TmPart2part(self, parent, child):
		insert_dict = {}
		insert_dict['parent'] = parent
		insert_dict['child'] = child
		return self._insert_tm_part2part(insert_dict)

	def _insert_tm_part(self, insert_dict):
		pass

	def _insert_tm_part2part(self, insert_dict):
		pass

	def _insert_tm_products_specification(self, file_name, tm_part_id, sdo='SDO'):
		pass