import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #os.system('export DATABASE = postgresql://${POSTGRESQL_USER}:${POSTGRESQL_PASSWORD}@${POSTGRESQL_SERVICE_HOST}/${POSTGRESQL_DATABASE}')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE') or 'sqlite:///' + os.path.join(basedir, 'app.db')  postgresql+psycopg2://${DROPMIRE_DB_USER}:${DROPMIRE_DB_PASS}@${POSTGRESQL_SERVICE_HOST}:5432/${DROPMIRE_DB_NAME}
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + str(os.environ.get('DROPMIRE_DB_USER')) + ":" + str(os.environ.get('DROPMIRE_DB_PASS')) + "@" + str(os.environ.get('POSTGRESQL_SERVICE_HOST')) + ":5432/" + str(os.environ.get('DROPMIRE_DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN') or None

    ADMINS = os.environ.get('ADMINS', 'root@localhost').split(',')
    MAIL_FROM = os.environ.get('MAIL_FROM', 'dropmire@example.org')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = os.environ.get('MAIL_PORT', 25)
    WHOIS_ORG_RE = os.environ.get('WHOIS_ORG_RE', '')
