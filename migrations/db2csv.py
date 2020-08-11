import csv
import sqlalchemy as sqAl
import sys
sys.path.append("../")
import app
from config import Config
from flask import Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))


metadata = sqAl.MetaData()

app = Flask(__name__)
app.config.from_object(Config)
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../app.db')
engine = sqAl.create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata.bind = engine

mytable = sqAl.Table('domain', metadata, autoload=True)
db_connection = engine.connect()

select = sqAl.sql.select([mytable])
result = db_connection.execute(select)

fh = open('data.csv', 'w')
outcsv = csv.writer(fh)

outcsv.writerow(result.keys())
outcsv.writerows(result)

fh.close
