from app import db


class ProductVariant(db.Model):
    __tablename__ = "product_variant"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.BigInteger)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
