from app import db
from app.entity.mysql.city import City as CityEntity
from constants import Pages


class City(CityEntity):
    __tablename__ = 'city'

    def __init__(self, name):
        self.name = name

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def edit(cls, _id, name):
        try:
            db.session.query(CityEntity).filter(CityEntity.id == _id).update({"name": name})
            db.session.commit()
            return True, None
        except:
            return False, "Your city is existed"

    @classmethod
    def find(cls, name):
        return CityEntity.query.filter_by(name=name).first()

    @classmethod
    def query_order_by_id(cls, page):
        cities = CityEntity.query.order_by(CityEntity.id).paginate(page, Pages['NUMBER_PER_PAGE'], error_out=False)
        return cities, cities.pages
