from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.entity.mysql.color import Color as ColorEntity
from constants import Pages
from constants import Errors


class ColorModel(ColorEntity):

    def get_value_by_id(self, _id):
        return self.query.filter_by(id=_id).first().value

    def find(self, value):
        return self.query.filter_by(value=value).first()

    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def query_all(self):
        return self.query.order_by(self.id).all()

    def query_paginate(self, page):
        colors = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return colors.items, colors.pages

    def edit(self, _id, value):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update({"value": value})
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    @classmethod
    def create(cls, value):
        try:
            color = ColorEntity(value=value)
            db.session.add(color)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    def get_value(self):
        return self.value
