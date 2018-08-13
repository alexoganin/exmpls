# -*- coding: utf-8 -*-
from datetime import datetime
from BaseChart import CBaseChart
from core.utils import getListOfDicts

class CRadarViewChart(CBaseChart):
	type = 'RadarViewChart'

	def _getDataFromDB(self):
		self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForRadarChart())

	def _formatDataForResponse(self):
		formattedPoint = []
		for row in self._raw_data:
			current_dict = {
				'name': '%s - %s' % (self._getTimeInFormat(row.get('belegdatum'), '%Y.%m.%d'), row.get('belegid')),
			}
			current_dict.update(self.__getDeltaTimesForCurrentRow(self._prepareRawData(row),
																  datetime.strptime(row.get('belegdatum'), '%y%m%d')))
			formattedPoint.append(current_dict)
			if len(formattedPoint) > self._max_point_counter:
				break

		self._formatted_data = formattedPoint

	def __getDeltaTimesForCurrentRow(self, row, belegdatum):
		result = dict()
		result['a1'] = self._getDifferenceBetweenDates(row.get('charged_by_time'), belegdatum)
		result['a2'] = self._getDifferenceBetweenDates(row.get('announced_by_doc_time'), belegdatum)
		result['a3'] = self._getDifferenceBetweenDates(row.get('payed_by_doc_time'), belegdatum)
		result['a4'] = self._getDifferenceBetweenDates(row.get('valid_until'), belegdatum)
		result['booked_charged_by_time_diff'] = self._getDifferenceBetweenDates(row.get('booked_charged_by_time'), belegdatum)
		result['booked_payed_by_time_diff'] = self._getDifferenceBetweenDates(row.get('booked_payed_by_time'), belegdatum)
		#####################################################################################
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
		return result
