from app import db
from app.CRUD.search.models import SearchableMixin
from app.CRUD.rabbitmq.models import RabbitMqMixin

class Brand(SearchableMixin, RabbitMqMixin, db.Model):
    __tablename__ = "brand"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    category = db.relationship(
        "Category", backref='brand', lazy="dynamic")


    def convert_dict(self):
        return {
            "table": self.__tablename__,
            "mysql_id": str(self.id),
            "name": self.name,
            "create_mongo": {
                '_cls': 'Brand',
                'name': self.name,
                'mysql_id': str(self.id)
            },
            "edit_mongo": {
                "$set":
                    {"name": self.name}
            }
        }