import csv
import sqlalchemy as sqAl
import os
basedir = os.path.abspath(os.path.dirname(__file__))


metadata = sqAl.MetaData()
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../app.db')
engine = sqAl.create_engine(SQLALCHEMY_DATABASE_URI)
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
