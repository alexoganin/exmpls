# -*- coding: utf-8 -*-

from collections import OrderedDict
from sqlalchemy import distinct, func, desc, asc, and_
from core.db_connectors import loadSession
from core.models import PaymVouc, PaymVoucFroz, ShopData


class CTicketScheduleSqlTool():

	def __init__(self, corporateId, supplierId, st_date=None, end_date=None):
		self.__corporateId = corporateId
		self.__supplierId = supplierId
		self.__st_date = st_date
		self.__end_date = end_date

	@property
	def corporateId(self):
		return self.__corporateId

	@property
	def supplierId(self):
		return self.__supplierId

	def getDataForRadarChart(self):
		session = loadSession()
		select = session.query(PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVouc.c.corporateno,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.charged_by,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getDataForPolarChart(self):
		session = loadSession()
		select = session.query(PaymVouc.c.corporateno,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.suppliersettled_at,
							   PaymVouc.c.primanotaid,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.frozen_val,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getDataForDeadLine(self):
		session = loadSession()
		select = session.query(PaymVouc.c.corporateno,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.suppliersettled_at,
							   PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.frozen_val,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.charged_by_doc,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getDataForLineVolumeChart(self):
		session = loadSession()
		select = session.query(PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getDataForCashConversionChart(self):
		session = loadSession()
		select = session.query(PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.frozen_val,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   PaymVouc.c.charged_by,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getDataForCashConversionAsyncChart(self, start_date, end_date):
		session = loadSession()
		select = session.query(PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.frozen_val,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   PaymVouc.c.charged_by,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= start_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		session.close()
		return select.all()

	def getCountForCashConversionChart(self):
		session = loadSession()
		count = session.query(
							   PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.frozen_val,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   PaymVouc.c.charged_by,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()\
			.count()
		session.close()
		return count

	def getDataForCashConversionDetailChart(self):
		session = loadSession()
		select = session.query(PaymVoucFroz.c.revision,
							   PaymVoucFroz.c.charged_by_time,
							   PaymVoucFroz.c.announced_by_time,
							   PaymVoucFroz.c.payed_by_time,
							   PaymVoucFroz.c.charged_by_netto_sums,
							   PaymVoucFroz.c.announced_by_doc_time,
							   PaymVoucFroz.c.payed_by_doc_time,
							   PaymVoucFroz.c.booked_charged_by_time,
							   PaymVoucFroz.c.booked_payed_by_time,
							   PaymVoucFroz.c.frozen_val,
							   PaymVouc.c.corporateno,
							   PaymVouc.c.belegdatum,
							   PaymVouc.c.belegid,
							   PaymVouc.c.charged_by,
							   PaymVouc.c.valid_until,
							   PaymVouc.c.primanotaid,
							   PaymVouc.c.vunr,
							   PaymVouc.c.suppliersettled_at,
							   ShopData.c.vunr,
							   ShopData.c.objectname)\
			.filter(PaymVouc.c.belegid == PaymVoucFroz.c.belegid,
					PaymVoucFroz.c.revision == 0,
					ShopData.c.vunr == PaymVouc.c.vunr,
					and_(
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') >= self.__st_date,
						func.to_date(PaymVouc.c.belegdatum, 'YYMMDD') <= self.__end_date),
					PaymVouc.c.corporateno == self.__corporateId if self.__corporateId else '',
					PaymVouc.c.vunr == self.__supplierId if self.__supplierId else '')\
			.distinct()
		result = select.all()
		session.close()

		return result