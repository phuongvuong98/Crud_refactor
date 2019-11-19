from app import db


class Store(db.Model):
    __tablename__ = "store"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    store_name = db.Column(db.String(50))

    product_variant = db.relationship(
        "ProductVariant", backref='store', lazy="dynamic")
