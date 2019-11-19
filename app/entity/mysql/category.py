from app import db


class Category(db.Model):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    product = db.relationship(
        "Product", backref='category', lazy="dynamic")
