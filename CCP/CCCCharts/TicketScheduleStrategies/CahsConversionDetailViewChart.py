# -*- coding: utf-8 -*-
from datetime import datetime
from core.utils import getListOfDicts
from CCP.CCCCharts.TicketScheduleStrategies.BaseChart import CBaseChart

class CCashConversionDetailViewChart(CBaseChart):
	type='CashConversionDetailViewChart'

	def __init__(self, corporate_id, supplier_id, st_date, end_date, bar_type=''):
		super(CCashConversionDetailViewChart, self).__init__(corporate_id, supplier_id, st_date, end_date)
		self.__bar_type = bar_type

	def _getDataFromDB(self):
		self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForCashConversionDetailChart())

	def _formatDataForResponse(self):
		formattedPoint = []
		for row in self._raw_data:
			formattedPoint.append(self.__getFinalRow(self._prepareRawData(row)))

		self._formatted_data = formattedPoint

	def __getFinalRow(self, row):
		result = dict()
		result['bar_type'] = self.__getDataByBarType(row),
		result['primanotaid'] = row.get('primanotaid')
		result['vunr'] = '%s (%s)' % (row.get('objectname'),row.get('vunr'))
		result['belegid'] = row.get('belegid')
		result['suppliersettled_at'] = self._getTimeInFormat(row.get('suppliersettled_at'))
		result['valid_until'] = self._getTimeInFormat(row.get('valid_until'))
		result['charged_by_time'] = self._getTimeInFormat(row.get('charged_by_time'))
		result['announced_by_time'] = self._getTimeInFormat(row.get('announced_by_time'))
		result['charged_by_netto_sums'] = row.get('charged_by_netto_sums')
		result['announced_by_doc_time'] = self._getTimeInFormat(row.get('announced_by_doc_time'))
		result['payed_by_time'] = self._getTimeInFormat(row.get('payed_by_time'))
		result['payed_by_doc_time'] = self._getTimeInFormat(row.get('payed_by_doc_time'))
		result['booked_charged_by_time'] = self._getTimeInFormat(row.get('booked_charged_by_time'))
		result['booked_payed_by_time'] = self._getTimeInFormat(row.get('booked_payed_by_time'))
		result['belegdatum'] = self._getTimeInFormat(row.get('belegdatum'))
		result['frozen_val'] = row.get('frozen_val')
		return result

	def __getDataByBarType(self, row):
		result = 0
		if self.__bar_type == 'a1':
			result = self._getDifferenceBetweenDateStrings(row.get('charged_by_time'), row.get('suppliersettled_at')) \
					 * row.get('frozen_val')
		elif self.__bar_type == 'a2':
			result = self._getDifferenceBetweenDateStrings(row.get('announced_by_doc_time'), row.get('charged_by')) \
					 * row.get('frozen_val')
		elif self.__bar_type == 'a3':
			result = self._getDifferenceBetweenDateStrings(row.get('payed_by_doc_time'), row.get('charged_by')) \
					 * row.get('frozen_val')
		elif self.__bar_type == 'a4':
			result = self._getDifferenceBetweenDateStrings(row.get('valid_until'), row.get('charged_by')) \
					 * row.get('frozen_val')
		elif self.__bar_type == 'a5':
			result = (self._getDifferenceBetweenDateStrings(row.get('payed_by_doc_time'),row.get('charged_by'))
					  * row.get('frozen_val')) \
					 - (self._getDifferenceBetweenDateStrings(row.get('valid_until'), row.get('charged_by'))
						* row.get('frozen_val'))

		return float('%.4f' % result)