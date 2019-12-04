from app import db
from app.CRUD.search.models import SearchableMixin
from app.CRUD.rabbitmq.models import RabbitMqMixin


class Color(SearchableMixin, RabbitMqMixin,  db.Model):
    __tablename__ = "color"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['value']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), unique=True)
    product_variant = db.relationship(
        "ProductVariant", backref='color', lazy="dynamic")

    def convert_dict(self):
        return {
            "table": self.__tablename__,
            "mysql_id": str(self.id),
            "value": self.value,
            "create_mongo": {
                '_cls': 'Color',
                'value': self.value,
                'mysql_id': str(self.id)
            },
            "edit_mongo": {
                "$set":
                    {"value": self.value}
            }
        }
