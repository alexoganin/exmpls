# -*- coding: utf-8 -*-

from Base import CBase
from tedTM.managers.TedtmDataManager import CTedtmDataManager
from tedTM.handlers.SaveHandler.AccessoryHandlers.ReferenceLinkerHandler import CReferenceLinkerHandler
from tedTM.handlers.SaveHandler.AccessoryHandlers.NodeAttachmentHandler import CNodeAttachmentHandler


class CValue(CBase):
	type = "VALUE"

	def save(self, ts_id):
		saved_list = []
		self.validation(ts_id)
		referenceLinkerHandler = CReferenceLinkerHandler(self._model, self._sdo_owner)
		ts_id, update_model = self._saveToDataBase(ts_id, self._sdo_owner,
												   self._sdo_owner)  # double self._sdo_owner - user save schema for his own

		# save inner ts_reference for old user related to this ts_id
		referenceLinkerHandler.saveInnerTendersForUsers(self._getTenderRelatedSdo(ts_id))
		nodeAttacmentHandler = None
		if self._base_ts_id and ts_id != self._base_ts_id:
			nodeAttacmentHandler = CNodeAttachmentHandler(self._base_ts_id)
			nodeAttacmentHandler.saveNodeAttachmentForNewUser(ts_id, self._sdo_owner)

		if self._is_share:
			for sdo in self._sdo_list:
				ts_id_sdo, model = self._saveToDataBase(None, sdo, self._sdo_owner)
				saved_list.append({'sdo': sdo, 'id': ts_id_sdo})
				if nodeAttacmentHandler:
					nodeAttacmentHandler.saveNodeAttachmentForNewUser(ts_id_sdo, sdo)
			referenceLinkerHandler.saveInnerTendersForUsers(self._sdo_list)  # save inner ts_reference for new users
		return ts_id, update_model, saved_list

	def _saveToDataBase(self, ts_id, sdo, sdo_owner):
		tenderName = self._name
		if sdo != sdo_owner:
			tenderName = self._name + "_saved_by_" + str(sdo_owner)

		rawData = {'model': self._model,
				   'tenderName': tenderName}
		tedDataManager = CTedtmDataManager(rawData, ts_id)
		tedDataManager.saveUpdateTenderSpecification(sdo, sdo_owner)
		return tedDataManager.tenderId, tedDataManager.updatedModelData

	def _getTenderRelatedSdo(self, ts_id):
		tedDataManager = CTedtmDataManager({}, ts_id)
		tender_related_sdo_dict = tedDataManager.getAllTenderRelatedSdo(ts_id)
		result = tender_related_sdo_dict.get('related_sdo') + [tender_related_sdo_dict.get('owner_sdo')]
		return [sdo for sdo in result if sdo != self._sdo_owner]


	# TODO: need to refactor
	def saveAsNew(self):
		pass

	def updateCurrent(self, ts_id):
		pass

	def createShareItems(self):
		pass