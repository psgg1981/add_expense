import datetime
import functools
import operator
import calendar

import gspread

# Constants
COL_OPTIONS = 'A'

EXPENSES_ROW_START 	 	 =  6
EXPENSES_ROW_TOTALS 	 = 18


COL_JAN		= 'B'
COL_FEB		= 'C'
COL_MAR		= 'D'
COL_APR		= 'E'
COL_MAY		= 'F'
COL_JUN		= 'G'
COL_JUL		= 'H'
COL_AUG		= 'I'
COL_SEP		= 'J'
COL_OCT		= 'K'
COL_NOV		= 'L'
COL_DEC		= 'M'

# exceptions
class AuthenticationFailedException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class UnexpectedFlow(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class UnexpectedFormat(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class AddExpenses:
	def __init__(self):
		self.menu_options = []
		self.spreadsheet = None
		self.client = None

	def listOptions(self):
		self.auth_and_init()
		print("Menu option items:")
		self.list_menu_options()

	def	readOption(self, option, month):
		self.auth_and_init()
		if self.validate_menu_option(option) and self.validate_month(month):
			self.read_expense_value(option, 
									self.get_month_col(month))	# get month column to retrieve values from

	# returns current month constant
	def get_curr_month(self):
		switcher = {
			1:	COL_JAN,
			2:	COL_FEB,
			3:	COL_MAR,
			4:	COL_APR,
			5:	COL_MAY,
			6:	COL_JUN,
			7:	COL_JUL,
			8:	COL_AUG,
			9:	COL_SEP,
			10:	COL_OCT,
			11:	COL_NOV,
			12:	COL_DEC
		}
		month = int(datetime.datetime.now().month)
		return switcher.get(month)

	# returns configured column for given month
	def get_month_col(self, month):
		switcher = {
			'Jan':	COL_JAN,
			'Feb':	COL_FEB,
			'Mar':	COL_MAR,
			'Apr':	COL_APR,
			'May':	COL_MAY,
			'Jun':	COL_JUN,
			'Jul':	COL_JUL,
			'Aug':	COL_AUG,
			'Sep':	COL_SEP,
			'Oct':	COL_OCT,
			'Nov':	COL_NOV,
			'Dec':	COL_DEC
		}
		return switcher.get(month)

	# returns month name from configured spreadsheet cell column
	def get_month_name_by_col(self, month_col):
		switcher = {
			COL_JAN: 'Jan',
			COL_FEB: 'Feb',
			COL_MAR: 'Mar',
			COL_APR: 'Apr',
			COL_MAY: 'May',
			COL_JUN: 'Jun',
			COL_JUL: 'Jul',
			COL_AUG: 'Aug',
			COL_SEP: 'Sep',
			COL_OCT: 'Oct',
			COL_NOV: 'Nov',
			COL_DEC: 'Dec'
		}
		return switcher.get(month_col)

	# adds new currency value under given month (e.g. Jan, Feb, etc.) to specified option
	def submit(self, option, value, month):
		self.auth_and_init()
		if(self.validate_menu_option(option) and self.validate_value(value) and self.validate_month(month)):			
			self.append_value_to_expenses(	option, 
											round(float(value), 2),
											self.get_month_col(month))	# get month column to retrieve values from


	# authenticates service account on google spreadsheets
	def authenticate_gs(self):
		try:
			return gspread.service_account()
		except:
			raise AuthenticationFailedException("Google API Service Account key not found. "
	                                            "Please follow instructions at https://gspread.readthedocs.io/en/latest/oauth2.html")

	# opens google spreadsheet
	def initialize_gs(self):
		return self.client.open("Contas Casa")

	# initializes available menu options
	def setup_menu_options(self):

		sheet = self.spreadsheet.sheet1;
		# e.g. get A6:A17
		range_of_cells_contents = sheet.get(COL_OPTIONS+str(EXPENSES_ROW_START)+':'+ COL_OPTIONS+str(EXPENSES_ROW_TOTALS - 1))
		# retrieve a single list of strings; ref. https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists/40857703
		self.menu_options = self.flattenlist(range_of_cells_contents)

	def flattenlist(self, list):
		return functools.reduce(operator.iconcat, list, [])

	# lists available menu options
	def list_menu_options(self):
		for idx, val in enumerate(self.menu_options):
			print(idx, val)

	# authenticates service account and initializes spreadsheet
	def auth_and_init(self):
		print("Authenticating...")
		self.client = self.authenticate_gs()
		print("Setting up menu options...")	
		self.spreadsheet = self.initialize_gs()
		self.setup_menu_options()

	# validates menu option
	def validate_menu_option(self, option):
		if not option.isnumeric():
			print("Option must be numeric")
			return False
		if(int(option) > 0 and int(option) < len(self.menu_options)):
			print("Selected option " + option + " found: " + str(self.menu_options[int(option)]))
			return True
		else:
			print("Selected option " + option + " not found")
			return False

	# validates if a proper currency number
	def validate_value(self, value):
		if not value.replace('.','',1).isdigit():
			print("Provided value " + str(value) + " must be a number" + ("", ". Please use '.' for input of decimal values.")[value.replace(',','',1).isdigit()])
			return False
		elif float(value) <= 0:
			print("Provided value " + str(value) + " must be positive")
			return False
		elif round(float(value), 2) == 0:
			print("Provided value " + str(value) + " is too low.")
			return False
		
		return True

	# validates if a proper currency number
	def validate_month(self, month):
		if month not in list(calendar.month_abbr):
			print('Invalid month ' + month +'. Expecting value from ' + ','.join(list(calendar.month_abbr))[1:])
			return False

		return True

	# formats a string to a google spreadsheet number format e.g. '2.5' -> '2,50'
	def format2gsnumber(self, string):
		if string.replace('.','',1).isdigit():

			# adding trailing zeros to string, https://www.kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
			string = "{:.2f}".format(float(string))

			string = string.replace(".", ",")

			return string
		else:
			raise UnexpectedFormat(string + " is not a number")

	def append_value_to_expenses(self, option, value, month_col):

		sheet = self.spreadsheet.sheet1

		# find the row corresponding to the menu_option
		option_row = sheet.find(self.menu_options[int(option)], in_column=1).row

		if option_row is not None:
			cell_position = month_col+str(option_row)

			# determine expense item and value to be affected
			str_expense_item = sheet.get(COL_OPTIONS+str(option_row))[0][0]

			# there may be no values yet saved...
			try:
				expense_value = sheet.get(cell_position)
				# get the existing cell
				expense_value_cell = sheet.acell(cell_position, value_render_option='FORMATTED_VALUE')
				# get the existing value's formula
				expense_value_formula = str(expense_value_cell.value)  # uses FORMATTED_VALUE for the ',' commas
				##delete expense_value_formula = flattenlist(expense_value_formula)

				print("Appending $" + self.format2gsnumber(str(value)) + 
					  " to " + str_expense_item + 
					  " under " + self.get_month_name_by_col(month_col) +
					  ", current value: " + str(expense_value) + " " + str(expense_value_formula))

				# check for formula types
				# e.g. '=1+2' 	-> '=1+2+3'
				if expense_value_formula.find("=", 0, 1) > -1:		
					expense_value_formula += "+" + self.format2gsnumber(str(value))
				# e.g. '33' 	-> '=33+34'
				elif(expense_value_formula.replace(',','',1).isdigit()):
					expense_value_formula = "=" + expense_value_formula + "+" + self.format2gsnumber(str(value))
				else:
					raise UnexpectedFlow("Unable to determine proper formula update for cell " + cell_position + " in '" + str_expense_item + "' item")

				# update the cell with the new formula
				##deprecated sheet.update_acell(cell_position, expense_value_formula)
				expense_value_cell.value = expense_value_formula
				sheet.update_cells([expense_value_cell], value_input_option='USER_ENTERED')		## WARNING: this is not maintaining the full formula

				# report the final value
				final_expense_value = sheet.get(cell_position)[0][0]
				print("Final value set to: " + str(final_expense_value))

            # when there is no value found on the cell
			except KeyError:
				print("Expenses item '" + str_expense_item + "' is currently empty (" + 
					  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
					  str(datetime.datetime.now().year) + ")")
				print("Setting " + str_expense_item + 
					  " with " + self.format2gsnumber(str(value)) + "...")
				sheet.update_acell(cell_position, self.format2gsnumber(str(value)))
		else:
			raise UnexpectedFlow("Unexpected error: row for menu option " + option + " not found!")
			
	def read_expense_value(self, option, month_col):		

		sheet = self.spreadsheet.sheet1

		# find the row corresponding to the menu_option
		option_row = sheet.find(self.menu_options[int(option)], in_column=1).row

		if option_row is not None:
			cell_position = month_col+str(option_row)

			str_expense_item = sheet.get(COL_OPTIONS+str(option_row))[0][0]
			
			# there may be no values yet saved...
			try:
				str_expense_value = sheet.get(cell_position)[0][0]	
				str_expense_value_formula = str(sheet.acell(cell_position, value_render_option='FORMULA').value)
				print(str_expense_item + ": " + str_expense_value + " (" + str_expense_value_formula + ")")
				return 0
			except KeyError:
				print("Expenses item '" + str_expense_item + "' is currently empty (" + 
					  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
					  str(datetime.datetime.now().year) + ")")
		else:
			raise UnexpectedFlow("Unexpected error: row for menu option " + option + " not found!")