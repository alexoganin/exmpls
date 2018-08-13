# -*- coding: utf-8 -*-
from datetime import datetime
from BaseChart import CBaseChart
from core.utils import getListOfDicts

class CLineVolumeViewChart(CBaseChart):
	type = 'LineVolumeViewChart'

	def _getDataFromDB(self):
		self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForLineVolumeChart())

	def _formatDataForResponse(self):
		formattedPoint = []
		for row in self._raw_data:
			if not row.get('suppliersettled_at'):
				continue

			suppliersettled_at = datetime.strptime(row.get('suppliersettled_at'),
												   self._getSourceFormat(row.get('suppliersettled_at')))
			current_dict = {
				'name': '%s - %s' % (self._getTimeInFormat(row.get('suppliersettled_at'), '%Y.%m.%d'), row.get('belegid')),
			}
			current_dict.update(self.__getDeltaTimesForCurrentRow(self._prepareRawData(row), suppliersettled_at))
			formattedPoint.append(current_dict)
			if len(formattedPoint) > self._max_point_counter:
				break

		self._formatted_data = formattedPoint

	def __getDeltaTimesForCurrentRow(self, row, suppliersettled_at):
		result = dict()
		result['charged_by_time_diff'] = self._getDifferenceBetweenDates(row.get('charged_by_time'), suppliersettled_at)
		result['announced_by_time_diff'] = self._getDifferenceBetweenDates(row.get('announced_by_doc_time'), suppliersettled_at)
		result['payed_by_time_diff'] = self._getDifferenceBetweenDates(row.get('payed_by_time'), suppliersettled_at)
		result['valid_until_diff'] = self._getDifferenceBetweenDates(row.get('valid_until'), suppliersettled_at)
		result['booked_charged_by_time_diff'] = self._getDifferenceBetweenDates(row.get('booked_charged_by_time'), suppliersettled_at)
		result['booked_payed_by_time_diff'] = self._getDifferenceBetweenDates(row.get('booked_payed_by_time'), suppliersettled_at)
		result['belegdatum_diff'] = self._getDifferenceBetweenDateStrings(row.get('belegdatum'), row.get('suppliersettled_at'), False)
		###################################################################
		result['suppliersettled_at'] = self._getTimeInFormat(row.get('suppliersettled_at'))
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
