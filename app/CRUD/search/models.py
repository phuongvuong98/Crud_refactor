from app import db
from app.search import add_to_index, remove_from_index, query_full_text, query_fuzzy, query_suggestion


class KindSearch:
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        pass


class FullTextSearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_full_text(table_name, expression, page, per_page)


class FuzzySearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_fuzzy(table_name, expression, page, per_page)


class SuggestionSearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_suggestion(table_name, expression)


class SearchableMixin(object):

    @classmethod
    def search(cls, expression, page, per_page, kind_search):
        ids, total = kind_search.query_index(cls.__tablename__, expression, page, per_page)

        ids = [int(_id) for _id in ids]
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))

        if ids == []:
            return cls.query.filter_by(id=0), 0

        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)).all(), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

#     @classmethod
#     def after_commit(cls, session):
#         for obj in session._changes['add']:
#             if isinstance(obj, SearchableMixin):
#                 add_to_index(obj.__tablename__, obj)
#         for obj in session._changes['update']:
#             if isinstance(obj, SearchableMixin):
#                 add_to_index(obj.__tablename__, obj)
#         for obj in session._changes['delete']:
#             if isinstance(obj, SearchableMixin):
#                 remove_from_index(obj.__tablename__, obj)
#         session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
# db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
