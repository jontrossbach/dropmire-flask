import sys
sys.path.append("../")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import app
from config import Config

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import pandas as pd

engine = db.get_engine()  # db is the one from the question
csv_file_path = 'data.csv'

# Read CSV with Pandas
with open(csv_file_path, 'r') as file:
    df = pd.read_csv(file)

# Insert to DB
df.to_sql('domain',
          con=engine,
          index=False,
          index_label='id',
          if_exists='replace')
