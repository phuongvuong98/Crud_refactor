import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = "True"
    ELASTICSEARCH_URL = 'http://localhost:9200'
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:@localhost:3306/newtest?charset=utf8mb4"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:@localhost:3306/search?charset=utf8mb4"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
