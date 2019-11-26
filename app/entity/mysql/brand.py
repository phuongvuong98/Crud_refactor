from app import db
from app.CRUD.search.models import SearchableMixin


class Brand(SearchableMixin, db.Model):
    __tablename__ = "brand"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    category = db.relationship(
        "Category", backref='brand', lazy="dynamic")
