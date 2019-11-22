from app import db


class District(db.Model):
    __tablename__ = "district"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    # address = db.relationship(
    #     "Address", backref='district', lazy="dynamic")

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
