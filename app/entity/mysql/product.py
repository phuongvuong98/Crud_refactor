from app import db
from app.CRUD.search.models import SearchableMixin


class Product(SearchableMixin, db.Model):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    product_variant = db.relationship(
        "ProductVariant", backref='product', lazy="dynamic")
