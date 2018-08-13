# -*- coding: utf-8 -*-
import json
from tedTM.managers.TedtmDataManager import CTedtmDataManager


class CReferenceLinkerHandler(object):
	def __init__(self, model, sdo_owner):
		self._model = model
		self._sdo_owner = sdo_owner

	def __getModelDict(self):
		model_dict = self._model
		if type(model_dict) is not dict:
			model_dict = json.loads(model_dict)
		return model_dict

	def getLinkedTenderSpecification(self):
		return_reference_list = []
		model = self.__getModelDict()
		node_data_array = model.get('nodeDataArray')
		for node in node_data_array:
			if node.get('category') == 'gateway' and node.get('gatewayType') == 2:
				return_reference_list.append(node.get('reference_ts_id'))
		return return_reference_list

	def saveInnerTendersForUsers(self, sdo_list):
		saved_list = []
		reference_list = self.getLinkedTenderSpecification()
		for sdo in sdo_list:
			for reference_ts_id in reference_list:
				if not self.isTenderSpecificationGranted(reference_ts_id, sdo) \
					and not self.isTenderReferenceSpecificationGranted(reference_ts_id, sdo):
					saved_list.append(self.saveReferenceToDB(reference_ts_id, sdo, self._sdo_owner))
		return saved_list

	def saveReferenceToDB(self, ts_id, sdo_referral, sdo_owner):
		tedDataManager = CTedtmDataManager({}, ts_id)
		reference_id = tedDataManager.saveTenderReference(sdo_referral, sdo_owner)
		return {'sdo': sdo_referral, 'id': reference_id}

	def isTenderSpecificationGranted(self, ts_id, sdo_referral):
		tedDataManager = CTedtmDataManager({}, ts_id)
		return int(ts_id) in [tender_spec.get('objectid') for tender_spec in tedDataManager.getUserTenders(sdo_referral, ['all'])]

	def isTenderReferenceSpecificationGranted(self, ts_id, sdo_referral):
		tedDataManager = CTedtmDataManager({}, ts_id)
		return int(ts_id) in [tender_spec.get('objectid') for tender_spec in tedDataManager.getUserTenderReferences(sdo_referral)]

	def deleteLinkedTenderSpecification(self):
		pass
