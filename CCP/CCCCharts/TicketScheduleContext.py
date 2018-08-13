# -*- coding: utf-8 -*-

from TicketScheduleStrategies.RadarViewChart import CRadarViewChart
from TicketScheduleStrategies.PolarViewChart import CPolarViewChart
from TicketScheduleStrategies.DeadLineViewChart import CDeadLineViewChart
from TicketScheduleStrategies.LineVolumeViewChart import CLineVolumeViewChart
from TicketScheduleStrategies.CashConversionViewChart import CCashConversionViewChart
from TicketScheduleStrategies.CahsConversionDetailViewChart import CCashConversionDetailViewChart
from TicketScheduleStrategies.CashConversionAsyncViewChart import CCashConversionAsyncViewChart

class TicketScheduleChartGenerator(object):

	@staticmethod
	def generate(strategy_type, params_dict):
		if strategy_type == CRadarViewChart.type:
			return CRadarViewChart(**params_dict)
		elif strategy_type == CPolarViewChart.type:
			return CPolarViewChart(**params_dict)
		elif strategy_type == CDeadLineViewChart.type:
			return CDeadLineViewChart(**params_dict)
		elif strategy_type == CLineVolumeViewChart.type:
			return CLineVolumeViewChart(**params_dict)
		elif strategy_type == CCashConversionViewChart.type:
			return CCashConversionViewChart(**params_dict)
		elif strategy_type == CCashConversionDetailViewChart.type:
			return CCashConversionDetailViewChart(**params_dict)
		elif strategy_type == CCashConversionAsyncViewChart.type:
			return CCashConversionAsyncViewChart(**params_dict)
		else:
			raise NotImplementedError('Not implemented chart %s selected' % (strategy_type))

	# TODO: idea for future
	def configure(self): pass