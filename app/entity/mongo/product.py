import mongoengine

from app.CRUD.search.models import SearchableMixin


class Product(mongoengine.Document, SearchableMixin):
    __tablename__ = 'product_mongo'
    __searchable__ = ['name']
    name = mongoengine.StringField(max_length=60, required=True)
    category_id = mongoengine.ObjectIdField(required=True)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Address %r>' % (self.name)
