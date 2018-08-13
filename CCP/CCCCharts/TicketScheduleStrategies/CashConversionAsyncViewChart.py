# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from core.utils import getListOfDicts
from BaseChart import CBaseChart

class CCashConversionAsyncViewChart(CBaseChart):
	type='CashConversionAsyncViewChart'

	def __init__(self, corporate_id, supplier_id, st_date, end_date, week_number):
		super(CCashConversionAsyncViewChart, self).__init__(corporate_id, supplier_id, st_date, end_date)
		self._week_counter = 1
		self._current_week_edge = None
		self._current_week_number = week_number

	def _getDataFromDB(self):
		self._current_week_edge = self.getEnumeratedWeeks(self._st_date, self._end_date)\
			.get(self._current_week_number)
		self._raw_data = getListOfDicts(
			self.ticket_schedule_sql_tool.getDataForCashConversionAsyncChart(self._current_week_edge[0], self._current_week_edge[1])
		)

	def _formatDataForResponse(self):
		formattedPoints = []
		for key, value in self.__groupByWeek().iteritems():
			formattedPoints.append(self.__get_week_average(key, value))

		self._formatted_data = {
			'records': formattedPoints,
			'week_counter': self._week_counter,
			'current_week': self._current_week_number
		}

	def __groupByWeek(self):
		week_list_values = []
		for row in self._raw_data:
			week_list_values.append(self.__getDeltaTimeForCurrentRow(self._prepareRawData(row)))
		return {self._current_week_edge: week_list_values}

	def __getDeltaTimeForCurrentRow(self, row):
		frozen_val = row.get('frozen_val')
		a1_days = self._getDifferenceBetweenDateStrings(row.get('charged_by_time'), row.get('suppliersettled_at'))
		a2_days = self._getDifferenceBetweenDateStrings(row.get('announced_by_doc_time'), row.get('charged_by'))
		a3_days = self._getDifferenceBetweenDateStrings(row.get('payed_by_doc_time'), row.get('charged_by'))
		a4_days = self._getDifferenceBetweenDateStrings(row.get('valid_until'), row.get('charged_by'))

		return {
			'frozen_val': row.get('frozen_val'),
			'a1': a1_days * frozen_val,
			'a2': a2_days * frozen_val,
			'a3': a3_days * frozen_val,
			'a4': a4_days * frozen_val,
			'a5': (a3_days * frozen_val) - (a4_days * frozen_val),
		}

	def __get_week_average(self, week_edge, week_row):
		def get_average_value(field_name):
			row_len = len(week_row) if len(week_row) else 1
			return float('%.4f' % (sum(map(lambda x: x.get(field_name), week_row)) / row_len))

		return {
			'a1': get_average_value('a1'),
			'a2': get_average_value('a2'),
			'a3': get_average_value('a3'),
			'a4': get_average_value('a4'),
			'a5': get_average_value('a5'),
			'frozen_val': get_average_value('frozen_val'),
			'name': '%s - %s' % (week_edge[0].strftime('%y.%m.%d'),
								week_edge[1].strftime('%y.%m.%d')),
			'start_date': time.mktime(week_edge[0].timetuple()),
			'end_date': time.mktime(week_edge[1].timetuple())
		}

	def getEnumeratedWeeks(self, st_date, end_date):
		result = {}
		week_counter = 1
		st_week = st_date
		end_week = st_week + timedelta(days=6-st_date.weekday())
		result[week_counter] = (st_week, end_week)
		while end_week < end_date:
			week_counter+=1
			st_week = end_week + timedelta(days=1)
			end_week = st_week + timedelta(days=6)
			end_week = end_week if end_week < end_date else end_date
			result[week_counter] = (st_week, end_week)
		self._week_counter = week_counter
		return result