# -*- coding: utf-8 -*-

from CCP.CCCCharts.TicketScheduleContext import TicketScheduleChartGenerator
from CCP.CCCCharts.TicketScheduleStrategies.RadarViewChart import CRadarViewChart
from CCP.CCCCharts.TicketScheduleStrategies.PolarViewChart import CPolarViewChart
from CCP.CCCCharts.TicketScheduleStrategies.DeadLineViewChart import CDeadLineViewChart
from CCP.CCCCharts.TicketScheduleStrategies.LineVolumeViewChart import CLineVolumeViewChart
from CCP.CCCCharts.TicketScheduleStrategies.CashConversionViewChart import CCashConversionViewChart
from CCP.CCCCharts.TicketScheduleStrategies.CahsConversionDetailViewChart import CCashConversionDetailViewChart
from CCP.CCCCharts.TicketScheduleStrategies.CashConversionAsyncViewChart import CCashConversionAsyncViewChart


class CTicketScheduleManager(object):

	def __init__(self, *args, **kwargs):
		self.__args = args
		self.__kwargs = kwargs
		self._status = True
		self._message = None
		self._rawData = []
		self._formattedData =[]
		self._maxPointCounter = 500
		self._argument_dict = {
			0: 'corporate_id',
			1: 'supplier_id',
			2: 'st_date',
			3: 'end_date',
			4: 'bar_type'
		}

	@property
	def status(self):
		return self._status
	@property
	def message(self):
		return self._message

	def getDataForRadarChartView(self):
		return self.__createChart(CRadarViewChart.type)

	def getDataForPolarChart(self):
		return self.__createChart(CPolarViewChart.type)

	def getDataForDeadLineChart(self):
		return self.__createChart(CDeadLineViewChart.type)

	def getDataForLineVolumeChart(self):
		return self.__createChart(CLineVolumeViewChart.type)

	def getDataForCashConversionChart(self):
		return self.__createChart(CCashConversionViewChart.type)

	def getDataForCashConversionDetailChart(self):
		return self.__createChart(CCashConversionDetailViewChart.type)

	def getDataForCashConversionAsyncChart(self):
		return self.__createChart(CCashConversionAsyncViewChart.type)

	def __createChart(self, type):
		print self.__getArguments()
		chart = TicketScheduleChartGenerator.generate(type, self.__getArguments())
		chart.buildChart()
		return chart.formatted_data

	def __getArguments(self):
		result = {}
		for i in range(0, len(self.__args)):
			result[self._argument_dict.get(i)] = self.__args[i]
		result.update(self.__kwargs)
		print result
		return result
