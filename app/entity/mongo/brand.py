import mongoengine

from app.CRUD.search.models import SearchableMixin


class Brand(mongoengine.Document, SearchableMixin):
    __tablename__ = 'brand_mongo'
    __searchable__ = ['name']
    name = mongoengine.StringField(max_length=60, required=True, unique=True)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Brand %r>' % (self.name)
