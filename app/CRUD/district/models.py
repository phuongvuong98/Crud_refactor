from app import db
from app.entity.mysql.district import District as DistrictEntity
from constants import Pages


class DistrictModel(DistrictEntity):

    def find(self, name):
        return self.query.filter_by(name=name).first()

    def query_paginate(self, page):
        districts = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return districts.items, districts.pages

    def edit(self, _id, name, city_id):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update({"name": name, "city_id": city_id})
            db.session.commit()
            return True, None
        except:
            return False, "Your city is existed"

    @classmethod
    def create(cls, name, city_id):
        try:
            district = DistrictEntity(name=name, city_id=city_id)
            db.session.add(district)
            db.session.commit()
            return True
        except:
            return False
