from app import db
from app.CRUD.search.models import SearchableMixin
from app.CRUD.rabbitmq.models import RabbitMqMixin


class Category(SearchableMixin, RabbitMqMixin, db.Model):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    product = db.relationship(
        "Product", backref='category', lazy="dynamic")

    def convert_dict(self):
        return {
            "table": self.__tablename__,
            "mysql_id": str(self.id),
            "name": self.name,
            "mysql_brand_id": str(self.brand_id),
            "create_mongo": {
                '_cls': 'Category',
                'name': self.name,
                'mysql_brand_id': str(self.brand_id),
                'mysql_id': str(self.id)
            },
            "edit_mongo": {
                "$set":
                    {
                        "name": self.name,
                        "mysql_brand_id": str(self.brand_id),
                    }
            }
        }
