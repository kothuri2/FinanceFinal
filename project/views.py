from project import app, db
from flask import render_template, request, redirect
from project.models.models import *
from sqlalchemy.ext.declarative import declarative_base
import json, datetime, ast
from project.taxes import calculate_taxes

month_increment = 0

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/increment_date", methods=["POST"])
def increment_date():
	global month_increment
	balance_sheet = BalanceSheet.query.all()[0]
	income_statement = IncomeStatement.query.all()[0]
	# balance_sheet operations
	balance_sheet.cash += balance_sheet.accounts_receivable
	balance_sheet.cash -= balance_sheet.accounts_payable
	balance_sheet.accounts_receivable = 0
	balance_sheet.accounts_payable = 0
	month_increment += 1
	db.session.commit()
	db.session.flush()
	return redirect('/')	

@app.route("/add_employee", methods=["POST", "GET"])
def add_employee():
	if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		address_line_1 = request.form['address_line_1']
		address_line_2 = request.form['address_line_2']
		city = request.form['city']
		state = request.form['state']
		zip_code = request.form['zip_code']
		social_security = request.form['social_security']
		number_of_witholdings = int(request.form['number_of_witholdings'])
		salary = float(request.form['salary'])
		new_employee = Employee(last_name=last_name, first_name=first_name,
								address_line_1=address_line_1, address_line_2=address_line_2,
								city=city, state=state, zip_code=zip_code,
								social_security_number=social_security,
								number_of_witholdings=number_of_witholdings, salary=salary)
		db.session.add(new_employee)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	return render_template('add_employee.html')

@app.route("/get_employees")
def get_employees():
	employees = Employee.query.all()
	return render_template('employees.html', employees=employees)

@app.route("/pay_employee", methods=["POST", "GET"])
def pay_employee():
	global month_increment
	if request.method == 'POST':
		employee_id = request.form['employee_id']
		employee = Employee.query.filter_by(id=employee_id).all()[0]
		taxes = calculate_taxes(employee)
		today_date = datetime.datetime.now()
		date_str = today_date.strftime('%m-%d-%Y')
		print(employee)
		month, day, year = date_str.split('-')[0], date_str.split('-')[1], date_str.split('-')[2]
		new_month = (int(month) + month_increment)%12
		if new_month == 0:
			new_month = 12
		date_str = str(new_month) + '-'+ day + '-'+year
		employee.last_date_paid = date_str
		payroll_record = PayrollRecord(employee_id=employee_id,date=date_str,medicare_tax=taxes['medicare_tax_witholding'],
									   social_security_tax=taxes['social_security_witholding'], federal_tax=taxes['federal_tax_witholding'],
									   state_tax=taxes['state_tax_witholding'], total_tax=taxes['total_tax'], net_pay=taxes['net_pay'])
		balance_sheet = BalanceSheet.query.all()[0]
		balance_sheet.cash -= round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		balance_sheet.total_current_assets -= round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		income_statement = IncomeStatement.query.all()[0]
		income_statement.payroll += round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		income_statement.payroll_witholding += round(float(taxes['total_tax']), 2)
		income_statement.total_expenses += round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		income_statement.operating_income -= round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		income_statement.net_income -= round(float(employee.salary/12) - float(taxes['total_tax']), 2)
		db.session.add(payroll_record)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	employees = Employee.query.all()
	employees_array = []
	for employee in employees:
		new_employee = {'employee': employee, 'payroll': True}
		current_date = datetime.datetime.now()
		current_date_str = current_date.strftime('%m-%d-%Y')
		last_date_paid = employee.last_date_paid
		if last_date_paid is not None:
			print(employee, last_date_paid, month_increment)
			month, day, year = current_date_str.split('-')[0], current_date_str.split('-')[1], current_date_str.split('-')[2]
			new_month = (int(month) + month_increment)%12
			if new_month == 0:
				new_month = 12
			current_date_str = str(new_month) + '-'+ day + '-'+year
			print(current_date_str)
			difference = abs((datetime.datetime.strptime(current_date_str, "%m-%d-%Y") - datetime.datetime.strptime(last_date_paid, "%m-%d-%Y")).days)
			if difference <= 30:
				new_employee['payroll'] = False
		employees_array.append(new_employee)
		db.session.commit()
		db.session.flush()
	return render_template('pay_employee.html', employees=employees_array)

@app.route("/payroll_events")
def payroll_events():
	payroll_events = PayrollRecord.query.all()
	payroll_events_array = []
	print(payroll_events)
	for payroll_event in payroll_events:
		employee_id = payroll_event.employee_id
		employee = Employee.query.filter_by(id=employee_id).all()[0]
		year = employee.last_date_paid.split('-')[2]
		new_event = {
		 			 'first_name': employee.first_name,
		 			 'last_name': employee.last_name,
		 			 'salary': employee.salary,
		 			 'payroll': payroll_event
		 			}
		payroll_events_array.append(new_event)
	return render_template('payroll_events.html', payroll_events=payroll_events_array)

@app.route("/add_customer", methods=["POST", "GET"])
def add_customer():
	if request.method == 'POST':
		company_name = request.form['company_name']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		address_line_1 = request.form['address_line_1']
		address_line_2 = request.form['address_line_2']
		city = request.form['city']
		state = request.form['state']
		zip_code = request.form['zip_code']
		price = round(float(request.form['price']), 2)
		new_customer = Customer(company_name=company_name, last_name=last_name, first_name=first_name,
								address_line_1=address_line_1, address_line_2=address_line_2,
								city=city, state=state, zip_code=zip_code, price=price)
		db.session.add(new_customer)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	return render_template('add_customer.html')

@app.route("/get_customers")
def get_customers():
	customers = Customer.query.all()
	return render_template('customers.html', customers=customers)

@app.route("/add_vendor", methods=["POST", "GET"])
def add_vendor():
	if request.method == 'POST':
		company_name = request.form['company_name']
		address_line_1 = request.form['address_line_1']
		address_line_2 = request.form['address_line_2']
		city = request.form['city']
		state = request.form['state']
		zip_code = request.form['zip_code']
		part = request.form['part']
		price_per_unit = round(float(request.form['price_per_unit']), 2)
		new_vendor = Vendor(company_name=company_name, address_line_1=address_line_1, address_line_2=address_line_2,
								city=city, state=state, zip_code=zip_code, price_per_unit=price_per_unit, part=part)
		db.session.add(new_vendor)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	return render_template('add_vendor.html')

@app.route("/get_vendors")
def get_vendors():
	vendors = Vendor.query.all()
	return render_template('vendors.html', vendors=vendors)

@app.route("/get_invoices")
def get_invoices():
	invoices = InvoiceRecord.query.all()
	invoices_array = []
	for invoice in invoices:
		customer_id = invoice.customer_id
		customer = Customer.query.filter_by(id=customer_id).all()[0]
		new_invoice = {'customer': customer,
					 'total': invoice.quantity * customer.price,
					 'invoice': invoice
		 			}
		invoices_array.append(new_invoice)

	return render_template('invoices.html', invoices=invoices_array)

@app.route("/create_invoice", methods=["POST", "GET"])
def create_invoice():
	if request.method == 'POST':
		product = Product.query.filter_by(product_name=request.form['product'].split(',')[0]).all()[0]
		units_purchased = int(request.form['number_of_units'])
		customer_id = request.form['customer']
		customer = Customer.query.filter_by(id=customer_id).all()[0]
		product_parts = product.parts
		today_date = datetime.datetime.now()
		date_str = today_date.strftime('%m-%d-%Y')
		for part in product_parts:
			parts_necessary_for_product = product_parts[part]
			part_inventory = PartInventory.query.filter_by(part=part).all()[0]
			part_inventory.quantity -= units_purchased * parts_necessary_for_product
			db.session.commit()
			db.session.flush()
		new_invoice = InvoiceRecord(customer_id=customer_id, product_name=request.form['product'].split(',')[0], quantity=units_purchased, date=date_str)
		balance_sheet = BalanceSheet.query.all()[0]
		income_statement = IncomeStatement.query.all()[0]
		balance_sheet.accounts_receivable += round(float(customer.price * units_purchased), 2)
		balance_sheet.total_current_assets += round(float(customer.price * units_purchased), 2)
		income_statement.sales += round(float(customer.price * units_purchased), 2)
		income_statement.gross_profit +=  round(float(customer.price * units_purchased), 2)
		income_statement.operating_income += round(float(customer.price * units_purchased), 2)
		income_taxes = round(round(float(customer.price * units_purchased), 2) * 0.07, 2) #illinois tax rate
		income_statement.income_taxes += income_taxes
		income_statement.net_income += (round(float(customer.price * units_purchased), 2) - income_taxes)
		db.session.add(new_invoice)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	customers = Customer.query.all()
	# calculate how many units of each product can be made
	products = Product.query.all()
	print(products)
	products_array = []
	for product in products:
		product_parts = product.parts
		quantity_available = 0
		quantity_can_make_from_parts = []
		for part in product_parts:
			# get all parts available
			parts_necessary_for_product = product_parts[part]
			part_inventory = PartInventory.query.filter_by(part=part).all()[0]
			parts_available_for_product = part_inventory.quantity
			if parts_available_for_product < parts_necessary_for_product:
				quantity_available = 0
				break
			else:
				quantity_can_make_from_parts.append(int(parts_available_for_product / parts_necessary_for_product))
		new_entry = {
			'product': product,
			'quantity': min(quantity_can_make_from_parts)
		}
		products_array.append(new_entry)
	return render_template('create_invoice.html', customers=customers, products=products_array)

@app.route("/create_purchase_order", methods=["POST", "GET"])
def create_purchase_order():
	if request.method == 'POST':
		vendor_id = request.form['vendor'].split(',')[0]
		part_name = request.form['vendor'].split(',')[1]
		quantity = request.form['number_of_units']
		today_date = datetime.datetime.now()
		date_str = today_date.strftime('%m-%d-%Y')
		new_order = PurchaseOrder(vendor_id=vendor_id, quantity=quantity, date=date_str)
		db.session.add(new_order)
		if(len(PartInventory.query.filter_by(part=part_name).all()) == 0):
			# part doesn't exist in PartInventory
			new_part_inventory = PartInventory(vendor_id=vendor_id, part=part_name, quantity=quantity)
			db.session.add(new_part_inventory)
		else:
			part_inventory = PartInventory.query.filter_by(part=part_name).first()
			part_inventory.quantity += int(quantity)
		vendor = Vendor.query.filter_by(id=vendor_id).all()[0]
		balance_sheet = BalanceSheet.query.all()[0]
		income_statement = IncomeStatement.query.all()[0]
		balance_sheet.inventory += round(float(int(quantity) * vendor.price_per_unit), 2)
		balance_sheet.accounts_payable += round(float(int(quantity) * vendor.price_per_unit), 2)
		balance_sheet.total_current_assets += round(float(int(quantity) * vendor.price_per_unit), 2)
		balance_sheet.total_liabilities += round(float(int(quantity) * vendor.price_per_unit), 2)
		income_statement.cogs += round(float(int(quantity) * vendor.price_per_unit), 2)
		income_statement.gross_profit -= round(float(int(quantity) * vendor.price_per_unit), 2)
		income_statement.operating_income -= round(float(int(quantity) * vendor.price_per_unit), 2)
		income_taxes = round(round(float(int(quantity) * vendor.price_per_unit), 2) * 0.07, 2)
		income_statement.income_taxes += income_taxes
		income_statement.net_income -= (round(float(int(quantity) * vendor.price_per_unit), 2) + income_taxes)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	vendors = Vendor.query.all()
	return render_template('create_PO.html', vendors=vendors)

@app.route("/purchase_orders")
def purchase_orders():
	purchase_orders = PurchaseOrder.query.all()
	purchase_orders_array = []
	for purchase_order in purchase_orders:
		vendor_id = purchase_order.vendor_id
		vendor = Vendor.query.filter_by(id=vendor_id).all()[0]
		new_order = {'vendor': vendor,
					 'total': purchase_order.quantity * vendor.price_per_unit,
					 'purchase_order': purchase_order
		 			}
		purchase_orders_array.append(new_order)
	return render_template('purchase_orders.html', purchase_orders=purchase_orders_array)

@app.route("/parts_inventory")
def parts_inventory():
	parts_inventory = PartInventory.query.all()
	parts_inventory_array = []
	for part_inventory in parts_inventory:
		vendor_id = part_inventory.vendor_id
		vendor = Vendor.query.filter_by(id=vendor_id).all()[0]
		quantity_low = False
		if part_inventory.quantity < 12:
			quantity_low = True
		new_inventory = {'vendor': vendor,
					 'total': part_inventory.quantity * vendor.price_per_unit,
					 'quantity': part_inventory.quantity,
					 'quantity_low': quantity_low
		 			}
		parts_inventory_array.append(new_inventory)
	return render_template('parts_inventory.html', parts_inventory=parts_inventory_array)

@app.route("/build_units", methods=["POST", "GET"])
def build_units():
	if request.method == 'POST':
		product_keys = list(request.form)
		product_name = request.form['product_name']
		parts = {}
		for key in product_keys:
			if 'part_name' in key:
				vals = key.split('_')
				counter_val = vals[2]
				parts[request.form[key]] = int(request.form['number_of_units_' + str(counter_val)])
		new_product = Product(product_name=product_name, parts=parts)
		db.session.add(new_product)
		db.session.commit()
		db.session.flush()
		return redirect('/')
	vendors = Vendor.query.all()
	return render_template('build_units.html', vendors=vendors)

@app.route("/get_new_part", methods=["POST"])
def get_new_part():
	data = json.loads(request.data)
	vendors = Vendor.query.all()
	return render_template('part_unit.html', vendors=vendors, counter=data['counter'])

@app.route("/business_info", methods=["POST", "GET"])
def business_info():
	if request.method == 'POST':
		balance_sheet = BalanceSheet.query.all()[0]
		income_statement = IncomeStatement.query.all()[0]
		if request.form['business_name'] != '':
			balance_sheet.business_name = request.form['business_name']
		if request.form['cash'] != '':
			balance_sheet.cash = round(float(request.form['cash']), 2)
			income_statement.sales = round(float(request.form['cash']), 2)
			income_statement.gross_profit = round(float(request.form['cash']), 2)
			income_statement.operating_income = round(float(request.form['cash']), 2)
			income_statement.net_income = round(float(request.form['cash']), 2)
			balance_sheet.total_current_assets += round(float(request.form['cash']), 2)
		if request.form['accounts_receivable'] != '':
			balance_sheet.accounts_receivable = round(float(request.form['accounts_receivable']), 2)
			balance_sheet.total_current_assets += round(float(request.form['accounts_receivable']), 2)
		if request.form['inventory'] != '':
			balance_sheet.inventory = round(float(request.form['inventory']), 2)
			balance_sheet.total_current_assets += round(float(request.form['inventory']), 2)
		
		if request.form['land_buildings'] != '':
			balance_sheet.land_buildings = round(float(request.form['land_buildings']), 2)
			balance_sheet.total_fixed_assets += round(float(request.form['land_buildings']), 2)
		if request.form['equipment'] != '':
			balance_sheet.equipment = round(float(request.form['equipment']), 2)
			balance_sheet.total_fixed_assets += round(float(request.form['equipment']), 2)
		if request.form['furniture_and_fixtures'] != '':
			balance_sheet.furniture_and_fixtures = round(float(request.form['furniture_and_fixtures']), 2)
			balance_sheet.total_fixed_assets += round(float(request.form['furniture_and_fixtures']), 2)
		if request.form['accounts_payable'] != '':
			balance_sheet.accounts_payable = round(float(request.form['accounts_payable']), 2)
			balance_sheet.total_liabilities += round(float(request.form['accounts_payable']), 2)
		if request.form['notes_payable'] != '':
			balance_sheet.notes_payable = round(float(request.form['notes_payable']), 2)
			balance_sheet.total_liabilities += round(float(request.form['notes_payable']), 2)
		if request.form['accruals'] != '':
			balance_sheet.accruals = round(float(request.form['accruals']), 2)
			balance_sheet.total_liabilities += round(float(request.form['accruals']), 2)
		if request.form['mortgage'] != '':
			balance_sheet.mortgage = round(float(request.form['mortgage']), 2)
			balance_sheet.total_liabilities += round(float(request.form['mortgage']), 2)
		if request.form['bills'] != '':
			income_statement.bills = round(float(request.form['bills']), 2)
			income_statement.total_expenses += round(float(request.form['bills']), 2)
			income_statement.operating_income -= round(float(request.form['bills']), 2)
			income_statement.net_income -= round(float(request.form['bills']), 2)
		if request.form['annual_expenses'] != '':
			income_statement.annual_expenses = round(float(request.form['annual_expenses']), 2)
			income_statement.total_expenses += round(float(request.form['annual_expenses']), 2)
			income_statement.operating_income -= round(float(request.form['annual_expenses']), 2)
			income_statement.net_income -= round(float(request.form['annual_expenses']), 2)
		if request.form['other_income'] != '':
			income_statement.other_income = round(float(request.form['other_income']), 2)
			income_statement.operating_income += round(float(request.form['other_income']), 2)
			income_statement.net_income += round(float(request.form['other_income']), 2)

		db.session.commit()
		db.session.flush()
		return redirect('/')
	balance_sheet = BalanceSheet.query.all()[0]
	income_statement = IncomeStatement.query.all()[0]
	return render_template('business_info.html', balance_sheet=balance_sheet, income_statement=income_statement)

@app.route("/balance_sheet", methods=["GET"])
def balance_sheet():
	balance_sheet = BalanceSheet.query.all()[0]
	return render_template('balance_sheet.html', balance_sheet=balance_sheet)

@app.route("/income_statement", methods=["GET"])
def income_statement():
	income_statement = IncomeStatement.query.all()[0]
	return render_template('income_statement.html', income_statement=income_statement)


