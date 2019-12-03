import mongoengine

from app.CRUD.search.models import SearchableMixin


class Store(mongoengine.Document, SearchableMixin):
    __tablename__ = 'store_mongo'
    __searchable__ = ['store_name']
    store_name = mongoengine.StringField(max_length=60, required=True)
    address_id = mongoengine.ObjectIdField(required=True)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Store %r>' % (self.store_name)
