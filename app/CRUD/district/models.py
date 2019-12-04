from app import db
from app.entity.mysql.district import District as DistrictEntity
from constants import Pages, Errors


class DistrictModel(DistrictEntity):

    def find(self, name):
        return self.query.filter_by(name=name).first()

    def query_paginate(self, page):
        districts = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return districts.items, districts.pages

    def query_by_city_id(self, city_id):
        return self.query.filter_by(city_id=city_id).all()

    def edit(self, _id, name, city_id):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update({"name": name, "city_id": city_id})
            db.session.update.append(self.query.filter_by(name=name).first())
            db.session.commit()
            DistrictEntity.reindex()
            return True, None
        except:
            return False, Errors.ERROR_EXIST.value

    @classmethod
    def create(cls, name, city_id):
        try:
            district = DistrictEntity(name=name, city_id=city_id)
            db.session.add(district)
            db.session.commit()
            DistrictEntity.reindex()
            return True
        except:
            return False

    def get_value(self):
        return self.name
