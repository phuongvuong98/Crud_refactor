from app import db
from app.CRUD.search.models import SearchableMixin
from app.CRUD.rabbitmq.models import RabbitMqMixin


class City(SearchableMixin, RabbitMqMixin, db.Model):
    __tablename__ = 'city'
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    district = db.relationship(
        "District", backref='city', lazy="dynamic")

    def __repr__(self):
        return '<City %r>' % self.name

    def convert_dict(self):
        return {
            "table": self.__tablename__,
            "mysql_id": str(self.id),
            "name": self.name,
            "create_mongo": {
                '_cls': 'City',
                'name': self.name,
                'mysql_id': str(self.id)
            },
            "edit_mongo": {
                "$set":
                    {"name": self.name}
            }
        }

