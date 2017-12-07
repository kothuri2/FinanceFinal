from project import db
from sqlalchemy import Column, Integer, String, Float, PickleType
from sqlalchemy.ext.declarative import declarative_base

'''
ORM for Product Model in database
'''
class Product(db.Model):
	__tablename__ = 'Product'
	id = db.Column('product_id', db.Integer, primary_key = True)
	product_name = db.Column(db.String(50))
	parts = db.Column(db.PickleType)

	def __repr__(self):
		return '<Product {} {}>'.format(self.product_name, self.parts)

'''
ORM for Part Inventory in database
'''
class PartInventory(db.Model):
	__tablename__ = 'PartInventory'
	id = db.Column('partinventory_id', db.Integer, primary_key = True)
	part = db.Column(db.String(400))
	vendor_id = db.Column(db.Integer)
	quantity = db.Column(db.Integer)

	def __repr__(self):
		return '<PartInventory {} {}>'.format(self.part, self.quantity)

'''
ORM for PurchaseOrder Model in database
'''
class PurchaseOrder(db.Model):
	__tablename__ = 'PurchaseOrder'
	id = db.Column('purchaseorder_id', db.Integer, primary_key = True)
	vendor_id = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	date = db.Column(db.String(50))

	def __repr__(self):
		return '<PurchaseOrder {} {}>'.format(self.vendor_id, self.quantity)

'''
ORM for InvoiceRecord Model in database
'''
class InvoiceRecord(db.Model):
	__tablename__ = 'InvoiceRecord'
	id = db.Column('invoicerecord_id', db.Integer, primary_key = True)
	customer_id = db.Column(db.Integer)
	product_name = db.Column(db.String(50))
	quantity = db.Column(db.Integer)
	date = db.Column(db.String(50))

	def __repr__(self):
		return '<InvoiceRecord {} {}>'.format(self.customer_id, self.quantity)

'''
ORM for Employee Model in database
'''
class Employee(db.Model):
	__tablename__ = 'Employee'
	id = db.Column('employee_id', db.Integer, primary_key = True)
	last_name = db.Column(db.String(50))
	first_name = db.Column(db.String(50))
	address_line_1 = db.Column(db.String(400))
	address_line_2 = db.Column(db.String(400))
	city = db.Column(db.String(50))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	social_security_number = db.Column(db.String(9))
	number_of_witholdings = db.Column(db.Integer)
	last_date_paid = db.Column(db.String(50))
	salary = db.Column(db.Float)

	def __repr__(self):
		return '<Employee {} {}>'.format(self.first_name, self.last_name)

'''
ORM for Payroll Record Model in database
'''
class PayrollRecord(db.Model):
	__tablename__ = 'PayrollRecord'
	id = db.Column('payroll_id', db.Integer, primary_key = True)
	employee_id = db.Column(db.Integer)
	date = db.Column(db.String(50))
	medicare_tax = db.Column(db.Float)
	social_security_tax = db.Column(db.Float)
	federal_tax = db.Column(db.Float)
	state_tax = db.Column(db.Float)
	total_tax = db.Column(db.Float)
	net_pay = db.Column(db.Float)

	def __repr__(self):
		return '<PayRoll Record {}>'.format(self.employee_id)

'''
ORM for Customer Model in database
'''
class Customer(db.Model):
	__tablename__ = 'Customer'

	id = db.Column('customer_id', db.Integer, primary_key=True)
	company_name = db.Column(db.String(400))
	last_name = db.Column(db.String(50))
	first_name = db.Column(db.String(50))
	address_line_1 = db.Column(db.String(400))
	address_line_2 = db.Column(db.String(400))
	city = db.Column(db.String(50))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	price = db.Column(db.Float)

	def __repr__(self):
		return '<Customer {} {} {}>'.format(self.company_name, self.first_name, self.last_name)

'''
ORM for Vendor Model in database
'''
class Vendor(db.Model):
	__tablename__ = 'Vendor'

	id = db.Column('vendor_id', db.Integer, primary_key=True)
	company_name = db.Column(db.String(400))
	part = db.Column(db.String(400))
	price_per_unit = db.Column(db.Float)
	address_line_1 = db.Column(db.String(400))
	address_line_2 = db.Column(db.String(400))
	city = db.Column(db.String(50))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))

	def __repr__(self):
		return '<Vendor {}>'.format(self.company_name)

'''
ORM for BalanceSheet Model in database
'''
class BalanceSheet(db.Model):
	__tablename__ = 'BalanceSheet'

	id = db.Column('balancesheet_id', db.Integer, primary_key=True)
	business_name = db.Column(db.String(400))
	#total_current_assets
	cash = db.Column(db.Float)
	accounts_receivable = db.Column(db.Float)
	inventory = db.Column(db.Float)
	total_current_assets = db.Column(db.Float)

	#total fixed assets
	land_buildings = db.Column(db.Float)
	equipment = db.Column(db.Float)
	furniture_and_fixtures = db.Column(db.Float)
	total_fixed_assets = db.Column(db.Float)

	#liabilities
	accounts_payable = db.Column(db.Float)
	notes_payable = db.Column(db.Float)
	accruals = db.Column(db.Float)
	mortgage = db.Column(db.Float)
	total_liabilities = db.Column(db.Float)

	def __repr__(self):
		return '<BalanceSheet {}>'.format(self.business_name)

'''
ORM for IncomeStatement Model in database
'''
class IncomeStatement(db.Model):
	__tablename__ = 'IncomeStatement'

	id = db.Column('incomestatement_id', db.Integer, primary_key=True)
	sales = db.Column(db.Float)
	cogs = db.Column(db.Float)
	gross_profit = db.Column(db.Float)

	#expenses
	payroll = db.Column(db.Float)
	payroll_witholding = db.Column(db.Float)
	bills = db.Column(db.Float) #business_info page
	annual_expenses = db.Column(db.Float) #business_info page
	total_expenses= db.Column(db.Float)

	#total_expenses
	other_income = db.Column(db.Float) #business_info page
	operating_income = db.Column(db.Float)
	income_taxes = db.Column(db.Float)
	net_income = db.Column(db.Float)

	def __repr__(self):
		return '<IncomeStatement {}>'.format(self.sales)
