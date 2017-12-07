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

#db.metadata.drop_all(db.engine, tables=[BalanceSheet.__table__,IncomeStatement.__table__,PartInventory.__table__,PurchaseOrder.__table__,InvoiceRecord.__table__,PayrollRecord.__table__])
#db.metadata.drop_all(db.engine, tables=[PayrollRecord.__table__])
#db.drop_all()
#balance_sheet = BalanceSheet(business_name='Business Name', cash=0, accounts_receivable=0, inventory=0, total_current_assets=0, land_buildings=0,equipment=0,furniture_and_fixtures=0,total_fixed_assets=0,accounts_payable=0,notes_payable=0,accruals=0,mortgage=0,total_liabilities=0)
#db.session.add(balance_sheet)
# #balance_sheet = BalanceSheet.query.all()[0]
# #balance_sheet.total_current_assets = (balance_sheet.cash  + balance_sheet.inventory)
#income_statement = IncomeStatement(sales=0,cogs=0,gross_profit=0,payroll=0, payroll_witholding=0,bills=0,annual_expenses=0,total_expenses=0,other_income=0,operating_income=0,income_taxes=0,net_income=0)
#db.session.add(income_statement)

#payroll_records = PayrollRecord.query.all()
#payroll_records = [payroll_records[-1]]

# employees = Employee.query.all()
# for employee in employees:
# 	employee.last_date_paid = '12-07-2017'

db.create_all()
db.session.commit()

import project.taxes
import project.views