# -*- coding: utf-8 -*-
from datetime import datetime
from CCP.sqltools.TicketScheduleSqlTool import CTicketScheduleSqlTool

class CBaseChart(object):
	type = 'BaseChart'

	def __init__(self, corporate_id, supplier_id, st_date, end_date):
		self._corporate_id = corporate_id
		self._supplier_id = supplier_id
		self._st_date = st_date
		self._end_date = end_date
		self.ticket_schedule_sql_tool = CTicketScheduleSqlTool(corporate_id, supplier_id, st_date, end_date)
		self._raw_data = None
		self._formatted_data = None
		self._max_point_counter = 500

	@property
	def raw_data(self):
		return self._raw_data

	@property
	def formatted_data(self):
		return self._formatted_data

	def buildChart(self):
		self._getDataFromDB()
		self._formatDataForResponse()

	def _getDataFromDB(self):
		raise NotImplementedError()

	def _formatDataForResponse(self):
		raise NotImplementedError()

	def _prepareRawData(self, row):
		if row.get('valid_until') == '*':
			row['valid_until'] = ''

		if not row.get('charge_by_time') and row.get('charged_by'):
			row['charged_by_time'] = row.get('charged_by')

		if row.get('announced_by_doc_time'):
			row['announced_by_doc_time'] = datetime.strptime(row.get('announced_by_doc_time'), '%d.%m.%Y')\
				.strftime('%y%m%d')

		if not row.get('payed_by_doc_time'):
			row['payed_by_doc_time'] = row.get('announced_by_doc_time')

		if row.get('charged_by_doc') and len(row.get('charged_by_doc')) == 10 :
			row['charged_by_doc'] = row.get('charged_by_doc')[4:] + row.get('charged_by_doc')[:4]

		return row

	def _getTimeInFormat(self, time_string, format="%d.%m.%Y"):
		try:
			current_time = datetime.strptime(time_string, self._getSourceFormat(time_string))
			if current_time == datetime(1900, 1, 1, 0, 0):
				return ''
		except Exception, e:
			# TODO data is incorrect log data here
			return time_string

		return current_time.strftime(format)

	def _getSourceFormat(self, time_string):
		return {
				0: '',
				6: '%y%m%d',
				7: '%y%m%dZ',
				10: '%y%m%d%H%M',
				12: '%y%m%d%H%M%S'
			}.get(len(time_string), '')


	def _getDifferenceBetweenDates(self, current_param, main_parameter, absolute=True):
		if not current_param:
			return 0
		try:
			result = (main_parameter - datetime.strptime(current_param, self._getSourceFormat(current_param))).days
			return abs(result) if absolute else result
		except Exception, e:
			# TODO: make sure that it is not mistake
			return 0

	def _getDifferenceBetweenDateStrings(self, first_parameter, second_parameter, absolute=True):
		if not first_parameter or not second_parameter:
			return 0
		try:
			first_parameter_datetime = datetime.strptime(first_parameter, self._getSourceFormat(first_parameter))
			second_parameter_datetime = datetime.strptime(second_parameter, self._getSourceFormat(second_parameter))
			result = (first_parameter_datetime - second_parameter_datetime).days
			return abs(result) if absolute else result
		except Exception, e:
			# TODO: make sure that it is not mistake
			return 0