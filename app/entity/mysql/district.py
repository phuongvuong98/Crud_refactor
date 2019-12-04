from app import db
from app.CRUD.search.models import SearchableMixin
from app.CRUD.rabbitmq.models import RabbitMqMixin


class District(SearchableMixin, RabbitMqMixin, db.Model):
    __tablename__ = "district"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    address = db.relationship(
        "Address", backref='district', lazy="dynamic")

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def convert_dict(self):
        return {
            "table": self.__tablename__,
            "mysql_id": str(self.id),
            "name": self.name,
            "mysql_city_id": str(self.city_id),
            "create_mongo": {
                '_cls': 'District',
                'name': self.name,
                'mysql_city_id': str(self.city_id),
                'mysql_id': str(self.id)
            },
            "edit_mongo": {
                "$set":
                    {
                        "name": self.name,
                        "mysql_city_id": str(self.city_id)
                    }
            }
        }
