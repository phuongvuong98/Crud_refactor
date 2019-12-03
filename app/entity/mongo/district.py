import mongoengine

from app.CRUD.search.models import SearchableMixin


class District(mongoengine.Document, SearchableMixin):
    __tablename__ = 'district_mongo'
    __searchable__ = ['name']
    name = mongoengine.StringField(max_length=60, required=True)
    city_id = mongoengine.ObjectIdField(required=True)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<District %r>' % (self.name)
