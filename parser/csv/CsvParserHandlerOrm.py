from CsvParserHandlerBase import CCsvParserHandlerBase
from inet.models import TmPart, TmPart2part
from core.db_connectors import loadSession

class CCsvParserHandlerOrm(CCsvParserHandlerBase):
	def __init__(self, file_name, csv_file_iterator=None, start_line_to_read=0, delimiter=';'):
		super(CCsvParserHandlerOrm, self).__init__(file_name, csv_file_iterator, start_line_to_read, delimiter)
		self._sql_session = loadSession()

	def _insert_tm_part(self, insert_dict):
		tm_part = TmPart(**insert_dict)
		self._sql_session.add(tm_part)
		self._sql_session.commit()
		return tm_part.id

	def _insert_tm_part2part(self, insert_dict):
		tm_part2part = TmPart2part(**insert_dict)
		self._sql_session.add(tm_part2part)
		self._sql_session.commit()
		return tm_part2part.id