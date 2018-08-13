# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from core.utils import getListOfDicts
from CCP.CCCCharts.TicketScheduleStrategies.BaseChart import CBaseChart

class CCashConversionViewChart(CBaseChart):
	type='CashConversionViewChart'

	def __init__(self, corporate_id, supplier_id, st_date, end_date, page, limit):
		super(CCashConversionViewChart, self).__init__(corporate_id, supplier_id, st_date, end_date)
		self._record_counter = 0
		self.__page = page
		self.__limit = limit
		self.__offset = (page*limit) - limit

	def _getDataFromDB(self):
		self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForCashConversionChart())

	def _formatDataForResponse(self):
		formattedPoint = []
		for key, value in self.__groupByWeek().iteritems():
			formattedPoint.append(self.__get_week_average(key, value))

		self._formatted_data = formattedPoint

	def __groupByWeek(self):
		def getWeekRange(date):
			start_date = date - timedelta(days=date.weekday())
			end_date = start_date + timedelta(days=6)
			if start_date < self._st_date:
				start_date = self._st_date
			if end_date > self._end_date:
				end_date = self._end_date
			return (start_date, end_date)

		result = dict()
		for row in self._raw_data:
			week_range = getWeekRange(datetime.strptime(row.get('belegdatum'), '%y%m%d'))
			if result.get(week_range):
				current_week_list = result.get(week_range)
				current_week_list.append(self.__getDeltaTimeForCurrentRow(self._prepareRawData(row)))
				result[week_range] = current_week_list
			else:
				result[week_range] = [self.__getDeltaTimeForCurrentRow(self._prepareRawData(row))]
		return result

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
			return float('%.4f' % (sum(map(lambda x: x.get(field_name), week_row)) / len(week_row)))

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

