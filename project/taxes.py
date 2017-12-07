def calculate_taxes(employee):
	income_tax_witholding = calculate_income_tax_witholding(employee.salary, employee.number_of_witholdings)
	state_tax_witholding = calculate_state_tax_witholding(employee.salary, employee.number_of_witholdings)
	social_security_witholding = calculate_social_security_witheld(employee.salary)
	medicare_tax_witholding = calculate_medicare_witheld(employee.salary)
	total_tax = income_tax_witholding + state_tax_witholding + medicare_tax_witholding + social_security_witholding
	return {
		'federal_tax_witholding': round(income_tax_witholding, 2),
		'state_tax_witholding': round(state_tax_witholding, 2),
		'social_security_witholding': round(social_security_witholding, 2),
		'medicare_tax_witholding': round(medicare_tax_witholding, 2),
		'total_tax': round(total_tax, 2),
		'net_pay': round(employee.salary - total_tax, 2)
	}

def calculate_income_tax_witholding(salary, number_of_allowances):
	# Assume all individuals are single
	# at this company
	# Paid on a Monthly schedule
	# Data from : https://www.irs.gov/pub/irs-pdf/p15a.pdf
	income_tax_witholding = 0.0
	gross_pay = float(salary / 12.0)
	if number_of_allowances == 0:
		if gross_pay > 0.0 and gross_pay <= 969.0:
			income_tax_witholding = (gross_pay - 192.0)*0.1
		elif gross_pay > 969.0 and gross_pay <= 3354.0:
			income_tax_witholding = (gross_pay - 451.0)*0.15
		elif gross_pay > 3354.0 and gross_pay <= 7850.0:
			income_tax_witholding = (gross_pay - 1612.20)*0.25
		elif gross_pay > 7850.0 and gross_pay <= 16163.0:
			income_tax_witholding = (gross_pay - 2280.54)*0.28
		elif gross_pay > 16163.0 and gross_pay <= 34917.0:
			income_tax_witholding = (gross_pay - 4383.94)*0.33
		elif gross_pay > 34917.0 and gross_pay <= 35058.0:
			income_tax_witholding = (gross_pay - 6128.19)*0.35
		elif gross_pay > 35058.0:
			income_tax_witholding = (gross_pay - 9489.16)*0.396
	elif number_of_allowances == 1:
		if gross_pay > 0.0 and gross_pay <= 1306.50:
			income_tax_witholding = (gross_pay - 529.50)*0.1
		elif gross_pay > 1306.50 and gross_pay <= 3691.50:
			income_tax_witholding = (gross_pay - 788.50)*0.15
		elif gross_pay > 3691.50 and gross_pay <= 8187.50:
			income_tax_witholding = (gross_pay - 1949.70)*0.25
		elif gross_pay > 8187.50 and gross_pay <= 16500.50:
			income_tax_witholding = (gross_pay - 2618.04)*0.28
		elif gross_pay > 16500.50 and gross_pay <= 35254.50:
			income_tax_witholding = (gross_pay - 4721.44)*0.33
		elif gross_pay > 35254.50 and gross_pay <= 35395.50:
			income_tax_witholding = (gross_pay - 6466.19)*0.35
		elif gross_pay > 35395.50:
			income_tax_witholding = (gross_pay - 9826.66)*0.396
	elif number_of_allowances == 2:
		if gross_pay > 0.0 and gross_pay <= 1644.0:
			income_tax_witholding = (gross_pay - 867.0)*0.1
		elif gross_pay > 1644.0 and gross_pay <= 4029.0:
			income_tax_witholding = (gross_pay - 1126.0)*0.15
		elif gross_pay > 4029.0 and gross_pay <= 8525.0:
			income_tax_witholding = (gross_pay - 2287.20)*0.25
		elif gross_pay > 8525.0 and gross_pay <= 16838.0:
			income_tax_witholding = (gross_pay - 2955.54)*0.28
		elif gross_pay > 16838.0 and gross_pay <= 35592.0:
			income_tax_witholding = (gross_pay - 5058.94)*0.33
		elif gross_pay > 35592.0 and gross_pay <= 35733.0:
			income_tax_witholding = (gross_pay - 6803.69)*0.35
		elif gross_pay > 35733.0:
			income_tax_witholding = (gross_pay - 10164.16)*0.396
	elif number_of_allowances == 3:
		if gross_pay > 0.0 and gross_pay <= 1981.50:
			income_tax_witholding = (gross_pay - 1204.50)*0.1
		elif gross_pay > 1981.50 and gross_pay <= 4366.50:
			income_tax_witholding = (gross_pay - 1463.50)*0.15
		elif gross_pay > 4366.50 and gross_pay <= 8862.50:
			income_tax_witholding = (gross_pay - 2624.70)*0.25
		elif gross_pay > 8862.50 and gross_pay <= 17175.50:
			income_tax_witholding = (gross_pay - 3293.04)*0.28
		elif gross_pay > 17175.50 and gross_pay <= 35929.50:
			income_tax_witholding = (gross_pay - 5396.44)*0.33
		elif gross_pay > 35929.50 and gross_pay <= 36070.50:
			income_tax_witholding = (gross_pay - 7141.19)*0.35
		elif gross_pay > 36070.50:
			income_tax_witholding = (gross_pay - 10501.66)*0.396
	elif number_of_allowances == 4:
		if gross_pay > 0.0 and gross_pay <= 2319.0:
			income_tax_witholding = (gross_pay - 1542.0)*0.1
		elif gross_pay > 2319.0 and gross_pay <= 4704.0:
			income_tax_witholding = (gross_pay - 1801.0)*0.15
		elif gross_pay > 4704.0 and gross_pay <= 9200.0:
			income_tax_witholding = (gross_pay - 2962.20)*0.25
		elif gross_pay > 9200.0 and gross_pay <= 17513.0:
			income_tax_witholding = (gross_pay - 3630.54)*0.28
		elif gross_pay > 17513.0 and gross_pay <= 36267.0:
			income_tax_witholding = (gross_pay - 5733.94)*0.33
		elif gross_pay > 36267.0 and gross_pay <= 36408.0:
			income_tax_witholding = (gross_pay - 7478.69)*0.35
		elif gross_pay > 36408.0:
			income_tax_witholding = (gross_pay - 10839.16)*0.396
	elif number_of_allowances == 5:
		if gross_pay > 0.0 and gross_pay <= 2656.50 :
			income_tax_witholding = (gross_pay - 1879.50)*0.1
		elif gross_pay > 2656.50  and gross_pay <= 5041.50:
			income_tax_witholding = (gross_pay - 2138.50)*0.15
		elif gross_pay > 5041.50 and gross_pay <= 9537.50 :
			income_tax_witholding = (gross_pay - 3299.70)*0.25
		elif gross_pay > 9537.50  and gross_pay <= 17850.50:
			income_tax_witholding = (gross_pay - 3968.04)*0.28
		elif gross_pay > 17850.50 and gross_pay <= 36604.50 :
			income_tax_witholding = (gross_pay - 6071.44)*0.33
		elif gross_pay > 36604.50  and gross_pay <= 36745.50:
			income_tax_witholding = (gross_pay - 7816.19)*0.35
		elif gross_pay > 36745.50:
			income_tax_witholding = (gross_pay - 11176.66)*0.396
	elif number_of_allowances == 6:
		if gross_pay > 0.0 and gross_pay <= 2994.00:
			income_tax_witholding = (gross_pay - 2217.0 )*0.1
		elif gross_pay > 2994.00  and gross_pay <= 5379.0:
			income_tax_witholding = (gross_pay - 2476.0)*0.15
		elif gross_pay > 5379.00 and gross_pay <= 9875.00 :
			income_tax_witholding = (gross_pay - 3637.20)*0.25
		elif gross_pay > 9875.00  and gross_pay <= 18188.0:
			income_tax_witholding = (gross_pay - 4305.54)*0.28
		elif gross_pay > 18188.00 and gross_pay <= 36942.0:
			income_tax_witholding = (gross_pay - 6408.94)*0.33
		elif gross_pay > 36942.00  and gross_pay <= 37083.0:
			income_tax_witholding = (gross_pay - 8153.69)*0.35
		elif gross_pay > 37083.00:
			income_tax_witholding = (gross_pay - 11514.16)*0.396

	return income_tax_witholding

def calculate_state_tax_witholding(salary, number_of_allowances):
	# based on state of Illinois
	# state resource: http://www.revenue.state.il.us/TaxForms/Withholding/IL-700-T.pdf
	gross_pay = float(salary / 12.0)
	line_1_witholding_value = number_of_allowances * (2175/(2175+1000))
	line_2_witholding_value = number_of_allowances * (1000/(2175+1000))

	return 0.0495 * (gross_pay - ((line_1_witholding_value * 2175 + line_2_witholding_value * 1000) / 12))

def calculate_social_security_witheld(salary):
	social_security_tax_rate = 0.062
	return social_security_tax_rate * salary

def calculate_medicare_witheld(salary):
	medicare_tax_rate = 0.0145
	return medicare_tax_rate * salary

