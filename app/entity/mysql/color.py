from app import db


class Color(db.Model):
    __tablename__ = "color"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), unique=True)
    product_variant = db.relationship(
        "ProductVariant", backref='color', lazy="dynamic")
