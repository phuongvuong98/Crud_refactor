import mongoengine

from app.CRUD.search.models import SearchableMixin


class ProductVariant(mongoengine.Document, SearchableMixin):
    __tablename__ = 'variant_mongo'
    __searchable__ = ['price']
    price = mongoengine.StringField(max_length=60, required=True)
    product_id = mongoengine.ObjectIdField(required=True)
    store_id = mongoengine.ObjectIdField(required=True)
    color_id = mongoengine.ObjectIdField(required=True)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<ProductVariant %r>' % (self.price)
