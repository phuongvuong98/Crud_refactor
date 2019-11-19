from app import db


class Brand(db.Model):
    __tablename__ = "brand"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    category = db.relationship(
        "Category", backref='brand', lazy="dynamic")
