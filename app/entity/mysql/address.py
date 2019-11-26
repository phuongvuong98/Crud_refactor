from app import db
from app.CRUD.search.models import SearchableMixin as SearchAddress


class Address(SearchAddress, db.Model):
    __tablename__ = "address"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['detail']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    detail = db.Column(db.String(50))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    store = db.relationship(
        "Store", backref='address', lazy="dynamic")
