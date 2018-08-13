# -*- coding: utf-8 -*-
from core.utils import getListOfDicts
from datetime import datetime
from CCP.CCCCharts.TicketScheduleStrategies.BaseChart import CBaseChart

class CDeadLineViewChart(CBaseChart):
	type = 'DeadLineViewChart'

	def _getDataFromDB(self):
			self._raw_data = getListOfDicts(self.ticket_schedule_sql_tool.getDataForDeadLine())

	def _formatDataForResponse(self):
		formattedPoint = []
		for row in self._raw_data:
			suppliersettled_at_raw = row.get('suppliersettled_at') if row.get('suppliersettled_at') else ''
			suppliersettled_at = datetime.strptime(suppliersettled_at_raw,
												   self._getSourceFormat(suppliersettled_at_raw))

			current_dict = self.__getDeltaTimesForCurrentRow(self._prepareRawData(row), suppliersettled_at)
			formattedPoint.append(current_dict)
			if len(formattedPoint) > self._max_point_counter:
				break

		self._formatted_data = formattedPoint

	def __getDeltaTimesForCurrentRow(self, row, belegdatum):
		return {
			'name': '%s - %s' % (row.get('objectname')[0:10], row.get('belegid')),
			'frozen_val': row.get('frozen_val'),
			'charged_by_doc': self._getDifferenceBetweenDates(row.get('charged_by_doc'), belegdatum),
			'payed_by_time': self._getDifferenceBetweenDates(row.get('payed_by_time'), belegdatum),
			'payed_by_doc_time': self._getDifferenceBetweenDates(row.get('payed_by_doc_time'), belegdatum),
			'announced_by_doc_time': self._getDifferenceBetweenDates(row.get('announced_by_doc_time'), belegdatum),
			'booked_payed_by_time': self._getDifferenceBetweenDates(row.get('booked_payed_by_time'), belegdatum),
			'booked_charged_by_time': self._getDifferenceBetweenDates(row.get('booked_charged_by_time'), belegdatum),
			'valid_until': self._getDifferenceBetweenDates(row.get('valid_until'), belegdatum)
		}