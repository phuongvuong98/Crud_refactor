from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.entity.mysql.address import Address as AddressEntity
from app.search import query_index
from constants import Pages
from constants import Errors


class AddressModel(AddressEntity):

    def query_paginate(self, page):
        address = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return address.items, address.pages, address.page

    def query_all(self):
        return self.query.order_by(self.id).all()

    def get_name_by_id(self, _id):
        return self.query.filter_by(id=_id).first().detail

    def edit(self, _id, district_id, detail):
        try:
            if not district_id:
                return False, Errors.ERROR_EXIST.value
            db.session.query(self.__class__).filter(
                self.__class__.id == _id).update(
                {
                    "district_id": district_id,
                    "detail": detail,
                }
            )
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    @classmethod
    def create(cls, district_id, detail):
        try:
            if not district_id or not detail:
                return False, Errors.ERROR_EXIST.value
            address = AddressEntity(district_id=district_id, detail=detail)
            db.session.add(address)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    @classmethod
    def search(cls, expression, page, per_page):
        AddressEntity.reindex()
        print("exp:", expression)
        print("table:", cls.__tablename__)
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        print(ids)
        print(total)
        ids = [int(_id) for _id in ids]
        print("ids", ids)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)).all(), total

    def get_value(self):
        return self.detail
