from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.entity.mysql.variant import ProductVariant as ProductVariantEntity
from constants import Pages


class ProductVariantModel(ProductVariantEntity):

    def query_paginate(self, page):
        variant = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return variant.items, variant.pages, variant.page

    def query_all(self):
        return self.query.order_by(self.id).all()

    def query_by_id(self):
        return self.query.filter(self.id == id).first()

    def edit(self, _id, price, product_id, store_id, color_id):
        try:
            db.session.query(self.__class__).filter(
                self.__class__.id == _id).update(
                {
                    "price": price,
                    "product_id": product_id,
                    "store_id": store_id,
                    "color_id": color_id
                }
            )
            db.session.commit()
            ProductVariantEntity.reindex()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    @classmethod
    def create(cls, price, product_id, store_id, color_id):
        try:
            new_product_variant = ProductVariantEntity(price=price, product_id=product_id, store_id=store_id,
                                                       color_id=color_id)
            db.session.add(new_product_variant)
            db.session.commit()
            ProductVariantEntity.reindex()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e.orig)

    def get_value(self):
        return self.price
