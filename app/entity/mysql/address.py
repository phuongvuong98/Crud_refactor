from app import db


class Address(db.Model):
    __tablename__ = "address"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    detail = db.Column(db.String(50))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    store = db.relationship(
        "Store", backref='address', lazy="dynamic")
