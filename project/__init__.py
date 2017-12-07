from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FinanceFinal.1.sqlite3'
db = SQLAlchemy(app)

from project.models.models import *

#db.metadata.drop_all(db.engine, tables=[PurchaseOrder.__table__, PartInventory.__table__])
#db.drop_all()
db.create_all()
db.session.commit()

import project.taxes
import project.views