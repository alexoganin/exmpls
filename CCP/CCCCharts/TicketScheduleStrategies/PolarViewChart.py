# -*- coding: utf-8 -*-
from BaseChart import CBaseChart
from core.utils import getListOfDicts
from datetime import datetime

class CPolarViewChart(CBaseChart):
	type = 'PolarViewChart'

	def _getDataFromDB(self):
		self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForPolarChart())

	def _formatDataForResponse(self):
		formattedPoint = []
		for row in self._raw_data:
			suppliersettled_at_raw = row.get('suppliersettled_at') if row.get('suppliersettled_at') else ''
			suppliersettled_at = datetime.strptime(suppliersettled_at_raw,
												   self._getSourceFormat(suppliersettled_at_raw))
			row = self._prepareRawData(row)
			current_dict = self.__getDeltaTimesForCurrentRow(row, suppliersettled_at)
			formattedPoint.append(current_dict)

		self._formatted_data = formattedPoint

	def __getDeltaTimesForCurrentRow(self, row, suppliersettled_at):
		return {
			'name': '(%s) %s-%s' % (row.get('objectname'),
										self._getTimeInFormat(row.get('belegdatum'), '%Y.%m.%d'),
										row.get('belegid')),
			'a3': float(row.get('frozen_val')) *
					  self._getDifferenceBetweenDates(row.get('payed_by_doc_time'), suppliersettled_at),
			'a4': float(row.get('frozen_val')) *
					  self._getDifferenceBetweenDates(row.get('valid_until'), suppliersettled_at),
			'vunr': '%s (%s)' % (row.get('objectname'),row.get('vunr')),
			'primanotaid' : row.get('primanotaid'),
			'belegid' : row.get('belegid'),
			'suppliersettled_at' : self._getTimeInFormat(row.get('suppliersettled_at')),
			'valid_until' : self._getTimeInFormat(row.get('valid_until')),
			'charged_by_time' : self._getTimeInFormat(row.get('charged_by_time')),
			'announced_by_time' : self._getTimeInFormat(row.get('announced_by_time')),
			'charged_by_netto_sums' : row.get('charged_by_netto_sums'),
			'announced_by_doc_time' : self._getTimeInFormat(row.get('announced_by_doc_time')),
			'payed_by_time' : self._getTimeInFormat(row.get('payed_by_time')),
			'payed_by_doc_time' : self._getTimeInFormat(row.get('payed_by_doc_time')),
			'booked_charged_by_time' : self._getTimeInFormat(row.get('booked_charged_by_time')),
			'booked_payed_by_time' : self._getTimeInFormat(row.get('booked_payed_by_time')),
			'belegdatum' : self._getTimeInFormat(row.get('belegdatum'))
		}

