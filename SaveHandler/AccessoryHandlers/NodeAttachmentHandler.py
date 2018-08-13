# -*- coding: utf-8 -*-

import os
import uuid
from shutil import copy
from werkzeug.utils import secure_filename
from datetime import datetime
from core.local_config import Config
from tedTM.sqltools.TedtmSqlTool import CTedtmSqlTool
from tedTM.sqltools.NodeAttachedFileSqlTool import CNodeAttachedFileSqlTool

class CNodeAttachmentHandler(object):
	def __init__(self, ts_id_source):
		self.__ts_id_source = ts_id_source
		self.__tedtmSqlTool = CTedtmSqlTool()
		self.__nodeAttachedFileSqlTool = CNodeAttachedFileSqlTool()

	def saveNodeAttachmentForNewUser(self, ts_id, sdo):
		# TODO: get all attachments
		source_attachments = self.__getNodesAttachemnts(self.__ts_id_source)
		# save it
		return self.__copyFilesForNewTenderSpecification(ts_id, source_attachments, sdo)

	def __copyFilesForNewTenderSpecification(self, ts_id, source_attachments, sdo):

		def get_source_files_by_position(position):
			return_value = []
			for node in source_attachments:
				if node.get('position') == position:
					return_value = node.get('files')
			return return_value

		return_node_file_list = []
		# get all new nodes with position
		nodes = self.__tedtmSqlTool.getTenderSpecificationNodesData(ts_id)
		for node in nodes:
			old_file_list = get_source_files_by_position(node.position)
			if len(old_file_list):
				new_file_list = self.__createFilesForNode(node.id, old_file_list, sdo)
				return_node_file_list.append({'node_id': node.id,
											  'file_list': new_file_list,
											  'position': node.position})
		return return_node_file_list

	# return dict [{node_id: [file_id_1, file_id_2, ..., file_id_n]}]
	def __getNodesAttachemnts(self, ts_id):
		result = []
		nodes = self.__tedtmSqlTool.getTenderSpecificationNodesData(ts_id)
		for node in nodes:
			if self.__nodeAttachedFileSqlTool.haveAttachedFiles(node.id):
				current_node_attachments = {
					"node_id": node.id,
					"position": node.position,
					"files": self.__nodeAttachedFileSqlTool.getByNodeId(node.id)}
				result.append(current_node_attachments)
		return result


	def __createFilesForNode(self, node_id, file_list, sdo):
		return_file_list = []
		for current_file in file_list:
			# TODO : copy file - get path
			server_file_name = self._getUniqFileName(current_file.file_name)
			new_path = self.__copyFile(current_file.path, server_file_name, sdo)
			# TODO : create new record in DB
			file_id = self.__nodeAttachedFileSqlTool.create({
				'node_id': node_id,
				'sdo': sdo,
				'created_at': datetime.now(),
				'server_file_name': server_file_name,
				'path': new_path,
				# ------------------------------------------
				'file_name': current_file.file_name,
				'attached_input_name': current_file.attached_input_name,
				'type': current_file.type,
				'size': current_file.size
			})
			return_file_list.append(file_id)
		return return_file_list

	# return str(new_file_path)
	def __copyFile(self, old_path, server_file_name, sdo):
		user_folder = os.path.join(Config.ATTACHED_FILES_PATH, sdo)
		if not os.path.exists(user_folder):
			os.makedirs(user_folder)
		new_file_path = os.path.join(user_folder, server_file_name)
		copy(old_path, new_file_path)
		return new_file_path

	# return new_file_id
	def __addToDBNewFile(self, file_id, file_path):
		pass

	# return string file_path
	def __getFilePathById(self, file_id):
		# sqlFilePathHandler
		file_path = ''
		return file_path

	# return list of ids
	def __getSorceTenderSpecificationNodesIds(self):
		return []

	def _getUniqFileName(self, origin_name):
		file_name, extension = os.path.splitext(secure_filename(origin_name))
		return file_name + '-' + str(uuid.uuid4()) + extension

