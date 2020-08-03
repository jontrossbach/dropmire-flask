import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    oc.system('$DATABASE = postgresql://${DATABASE_USER}:${DATABASE_PASSWORD}@${POSTGRESQL_SERVICE_HOST}/${DATABASE_NAME}')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN') or None

    ADMINS = os.environ.get('ADMINS', 'root@localhost').split(',')
    MAIL_FROM = os.environ.get('MAIL_FROM', 'dropmire@example.org')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = os.environ.get('MAIL_PORT', 25)
    WHOIS_ORG_RE = os.environ.get('WHOIS_ORG_RE', '')
