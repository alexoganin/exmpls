# -*- coding: utf-8 -*-

from werkzeug.exceptions import BadRequest

from tedTM.sqltools.TedtmSqlTool import CTedtmSqlTool
from core.sqltools.CommonSqlTools import CCommonSqlTools

class CBase(object):

	type = 'BASE'

	def __init__(self, name, is_share, share_type, model, sdo, sdo_owner, base_ts_id):
		self._name = name
		self._is_share = is_share
		self._share_type = share_type
		self._model = model
		self._sdo_list = sdo
		self._sdo_owner = sdo_owner
		self._base_ts_id = base_ts_id

		self._tedtm_sql_tool = CTedtmSqlTool()
		self._common_sql_tool = CCommonSqlTools()

	def validation(self, ts_id):
		def checkName(name, owner_sdo):
			if not name.strip():
				raise BadRequest('we can\'t use empty name')
			if len(self._tedtm_sql_tool.selectUserTendersByName(owner_sdo, name)) and not ts_id:
				raise BadRequest('This name %s is also presents in your tender list' % (name))

		def checkSdoList(sdoList):
			not_found_sdo_list = []
			for sdo in sdoList:
				if not len(self._common_sql_tool.selectShopDataBySDO(sdo)):
					not_found_sdo_list.append(sdo)
			if len(not_found_sdo_list):
				raise BadRequest('This sdo doesn\'t exist: ' + ','.join(not_found_sdo_list))

		checkSdoList(self._sdo_list)
		checkName(self._name, self._sdo_owner)

	def save(self, *args, **kwargs):
		pass

	def _saveToDataBase(self, *args, **kwargs):
		pass
