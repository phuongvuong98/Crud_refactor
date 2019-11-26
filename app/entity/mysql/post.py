from app import db
from app.CRUD.search.models import SearchableMixin


class Post(SearchableMixin, db.Model):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Post %r>' % self.name
