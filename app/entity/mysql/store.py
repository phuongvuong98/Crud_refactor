from app import db
from app.CRUD.search.models import SearchableMixin


class Store(SearchableMixin, db.Model):
    __tablename__ = "store"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['store_name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    store_name = db.Column(db.String(100))

    product_variant = db.relationship(
        "ProductVariant", backref='store', lazy="dynamic")
