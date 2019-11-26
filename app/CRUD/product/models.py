from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.entity.mysql.product import Product as ProductEntity
from constants import Pages
from constants import Errors


class ProductModel(ProductEntity):

    def query_paginate(self, page):
        product = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return product.items, product.pages, product.page

    def query_all(self):
        return self.query.order_by(self.id).all()

    def get_name_by_id(self, _id):
        return self.query.filter_by(id=_id).first().name

    def edit(self, _id, category_id, name):
        try:
            if not category_id:
                return False, Errors.ERROR_EXIST.value
            db.session.query(self.__class__).filter(
                self.__class__.id == _id).update(
                {
                    "category_id": category_id,
                    "name": name,
                }
            )
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    @classmethod
    def create(cls, category_id, name):
        try:
            if not category_id or not name:
                return False, Errors.ERROR_EXIST.value
            product = ProductEntity(category_id=category_id, name=name)
            db.session.add(product)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    def get_value(self):
        return self.name
