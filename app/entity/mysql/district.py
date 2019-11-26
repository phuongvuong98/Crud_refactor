from app import db
from app.CRUD.search.models import SearchableMixin


class District(SearchableMixin, db.Model):
    __tablename__ = "district"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    address = db.relationship(
        "Address", backref='district', lazy="dynamic")

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
