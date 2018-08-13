# -*- coding: utf-8 -*-
from SaveStrategies.Value import CValue
from SaveStrategies.Reference import CReference

class CSaveHandler(object):

	def __init__(self, params, sdo_owner):
		self._sdo_owner = sdo_owner
		self._raw_params = params
		self._params = {}
		self._getInitParams()


	def getSaver(self):
		if self._params.get('share_type') == CReference.type:
			return CReference(**self._params)
		return CValue(**self._params)

	def _getInitParams(self):
		def getShare(share):
			if share.strip() == '1':
				return True
			return False

		def getShareType(share_type):
			if share_type == 'reference':
				return CReference.type
			return CValue.type

		def getSDOParams(sdo_line):
			return [line.strip() for line in sdo_line.split(',') if line.strip()]

		def getBaseTsId(base_ts_id_str):
			return int(base_ts_id_str) if base_ts_id_str and base_ts_id_str.isdigit() and int(base_ts_id_str) != 0 else None

		self._params['name'] = self._raw_params.get('name', '')
		self._params['model'] = self._raw_params.get('model')
		self._params['sdo'] = getSDOParams(self._raw_params.get('SDO', ''))
		self._params['is_share'] = getShare(self._raw_params.get('share', ''))
		self._params['share_type'] = getShareType(self._raw_params.get('share_type'))
		self._params['sdo_owner'] = self._sdo_owner
		self._params['base_ts_id'] = getBaseTsId(self._raw_params.get('base_ts_id'))





