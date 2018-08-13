# -*- coding: utf-8 -*-

from Base import CBase
from tedTM.managers.TedtmDataManager import CTedtmDataManager
from tedTM.handlers.SaveHandler.AccessoryHandlers.ReferenceLinkerHandler import CReferenceLinkerHandler
from tedTM.handlers.SaveHandler.AccessoryHandlers.NodeAttachmentHandler import CNodeAttachmentHandler


class CReference(CBase):

	type = 'REFERENCE'

	def save(self, ts_id):
		self.validation(ts_id)
		referenceLinkerHandler = CReferenceLinkerHandler(self._model, self._sdo_owner)
		current_ts_id, update_model = self._saveAsValue(ts_id, self._sdo_owner)
		saved_list = []
		if self._is_share:
			for sdo in self._sdo_list:
				saved_list.append(self._saveToDataBase(current_ts_id, sdo, self._sdo_owner))
			referenceLinkerHandler.saveInnerTendersForUsers(self._sdo_list)	 # save inner ts_reference for new users
		return current_ts_id, update_model, saved_list

	def _saveToDataBase(self, ts_id, sdo_referral, sdo_owner):
		raw_data = {}
		tedDataManager = CTedtmDataManager(raw_data, ts_id)
		reference_id = tedDataManager.saveTenderReference(sdo_referral, sdo_owner)
		return {'sdo': sdo_referral, 'id': reference_id}

	def _saveAsValue(self, ts_id, sdo_owner):
		rawData = {'model': self._model,
				   'tenderName': self._name}
		tedDataManager = CTedtmDataManager(rawData, ts_id)
		tedDataManager.saveUpdateTenderSpecification(sdo_owner, sdo_owner)
		if (self._base_ts_id != tedDataManager.tenderId) :
			nodeAttachmentHandler = CNodeAttachmentHandler(self._base_ts_id)
			nodeAttachmentHandler.saveNodeAttachmentForNewUser(tedDataManager.tenderId, sdo_owner)
		return tedDataManager.tenderId, tedDataManager.updatedModelData