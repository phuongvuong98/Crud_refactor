from app import db
from app.entity.mysql.brand import Brand as BrandEntity
from constants import Pages


class BrandModel(BrandEntity):

    def get_name_by_id(self, _id):
        return self.query.filter_by(id=_id).first().name

    def find(self, name):
        return self.query.filter_by(name=name).first()

    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def query_all(self):
        return self.query.order_by(self.id).all()

    def query_paginate(self, page):
        brands = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return brands.items, brands.pages

    def edit(self, _id, name):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update({"name": name})
            db.session.commit()
            return True, None
        except:
            return False, "Your brand is existed"

    @classmethod
    def create(cls, name):
        try:
            brand = BrandEntity(name=name)
            db.session.add(brand)
            db.session.commit()
            return True
        except:
            return False