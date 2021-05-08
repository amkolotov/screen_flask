import os


class Configuration(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    MEDIA_DIR = os.path.join(BASEDIR, 'media')
    CSRF_ENABLED = True
    SECRET_KEY = 'aoajsbjmdkclahdkdkdl'

    PAGINATE_BY = 15

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'sqlite:///' + os.path.join(BASEDIR, 'screen.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
