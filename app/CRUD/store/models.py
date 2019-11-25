from app import db
from app.entity.mysql.store import Store as StoreEntity
from constants import Pages, Errors


class StoreModel(StoreEntity):

    def find(self, name):
        return self.query.filter_by(store_name=name).first()

    def query_all(self):
        return self.query.order_by(self.id).all()

    def query_paginate(self, page):
        stores = self.query.order_by(self.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return stores.items, stores.pages

    def query_by_address_id(self, address_id):
        return self.query.filter_by(address_id=address_id).all()

    def edit(self, _id, name, address_id):
        try:
            db.session.query(self.__class__).filter(self.__class__.id == _id).update(
                {"store_name": name, "address_id": address_id})
            db.session.commit()
            return True, None
        except:
            return False, Errors.ERROR_EXIST.value

    @classmethod
    def create(cls, name, address_id):
        try:
            store = StoreEntity(store_name=name, address_id=address_id)
            db.session.add(store)
            db.session.commit()
            return True
        except:
            return False
