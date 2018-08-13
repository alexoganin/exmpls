# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest
from tedTM.managers.TedtmDataManager import CTedtmDataManager
from core.sqltools.CommonSqlTools import CCommonSqlTools
from tedTM.sqltools.TedtmSqlTool import CTedtmSqlTool
from tedTM.handlers.SaveHandler.AccessoryHandlers.ReferenceLinkerHandler import CReferenceLinkerHandler


class CGrantToHandler(object):
	def __init__(self, ts_id, sdo):
		self._common_sql_tool = CCommonSqlTools()
		self.__ts_id = int(ts_id)
		self.__owner_sdo = sdo
		self.__granted_list = []
		self.__model = dict()

	def save(self, inputData):
		return_message = []
		self.__initInputData(inputData)
		self.validation()
		for sdo in self.__granted_list:
			if not self.__checkIsSchemaAlreadyGranted(sdo):
				self.grantTo(sdo)
				return_message.append('schema has new reference for sdo: ' + sdo)
			else:
				return_message.append('schema already had reference for sdo: ' + sdo)

		reference_list = self.createLinkForReference()
		reference_linker_message = []
		for ref_dict in reference_list:
			reference_linker_message.append("inner reference created for sdo: {sdo}, reference id: {id}".format(**ref_dict))
		return_message.append('<br/>'.join(reference_linker_message))
		return return_message


	def grantTo(self, sdo):
		tedDataManager = CTedtmDataManager(None, self.__ts_id)
		reference_id = tedDataManager.saveTenderReference(sdo, self.__owner_sdo)

	def validation(self):
		self.__checkIsSdosExist()
		self.__checkIsSchemaRelated()


	def __initInputData(self, inputData):
		sdo_line = inputData.get('SDO', '')
		self.__granted_list = [line.strip() for line in sdo_line.split(',') if line.strip()]
		tedDataManager = CTedtmDataManager(None, self.__ts_id)
		tender_data = tedDataManager.getTenderSpecification(self.__owner_sdo, 'ted')
		self.__model = tender_data.get('raw_data')


	def __checkIsSchemaAlreadyGranted(self, sdo):
		tedSqlTool = CTedtmSqlTool()
		return tedSqlTool.countTender(self.__ts_id, sdo)


	def __checkIsSchemaRelated(self):
		tedTmManager = CTedtmDataManager(None, self.__ts_id)
		schema_list = tedTmManager.getUserTenders(self.__owner_sdo)
		if not (self.__ts_id in [schema.get('objectid') for schema in schema_list]):
			raise BadRequest('You don\'t have permission to grant this schema, id: ' + self.__ts_id)

	def __checkIsSdosExist(self):
		not_found_sdo_list = []
		for sdo in self.__granted_list:
			if not len(self._common_sql_tool.selectShopDataBySDO(sdo)):
				not_found_sdo_list.append(sdo)
		if len(not_found_sdo_list):
			raise BadRequest('This sdo doesn\'t exist: ' + ','.join(not_found_sdo_list))

	def createLinkForReference(self):
		referenceLinkerHandler = CReferenceLinkerHandler(self.__model, self.__owner_sdo)
		return referenceLinkerHandler.saveInnerTendersForUsers(self.__granted_list)  # save inner ts_reference for new users
