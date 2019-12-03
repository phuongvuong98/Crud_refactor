from app import db
from app.entity.mysql.category import Category as CategoryEntity
from constants import Pages, Errors


class CategoryModel(CategoryEntity):

    def get_name_by_id(self, _id):
        return self.query.filter_by(id=_id).first().name

    def find(self, name):
        return self.query.filter_by(name=name).first()

    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def query_all(self):
        return self.query.order_by(self.id).all()

    def query_paginate(self, page):
        categories = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return categories.items, categories.pages

    def query_by_brand_id(self, brand_id):
        return self.query.filter_by(brand_id=brand_id).all()

    def edit(self, _id, name, brand_id):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update(
                {"name": name, "brand_id": brand_id})
            db.session.commit()
            CategoryEntity.reindex()
            return True, None
        except:
            return False, Errors.ERROR_EXIST.value

    @classmethod
    def create(cls, name, brand_id):
        try:
            category = CategoryEntity(name=name, brand_id=brand_id)
            db.session.add(category)
            db.session.commit()
            CategoryEntity.reindex()
            return True
        except:
            return False

    def get_value(self):
        return self.name
