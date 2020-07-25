"""ADD EXPENSE appends currency amounts to your Google Spreadsheet.

Usage:
	add_expense [-h|--help]
	add_expense [-l|--list]
	add_expense [-a|--add] <option> <value>
	add_expense [-r|--read] <option>

Options:
	-h --help Show this screen
	-l --list List options
	-a --add Add new expense
	-r --read Reads current monthly expenses amount and formula
"""

import gspread
import datetime
import functools
import operator
import calendar
from docopt import docopt

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

# authenticates service account on google spreadsheets
def authenticate_gs():
	try:
		return gspread.service_account()
	except:
		raise AuthenticationFailedException("Google API Service Account key not found. Please follow instructions at https://gspread.readthedocs.io/en/latest/oauth2.html")

# opens google spreadsheet
def initialize_gs(gc):
	return gc.open("Contas Casa")

menu_options = []

# initializes available menu options
def setup_menu_options(sh):
	# e.g. get A6:A17
	range_of_cells_contents = sh.sheet1.get(COL_OPTIONS+str(EXPENSES_ROW_START)+':'+ COL_OPTIONS+str(EXPENSES_ROW_TOTALS - 1))
	# retrieve a single list of strings; ref. https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists/40857703
	global menu_options 
	menu_options = flattenlist(range_of_cells_contents)

def flattenlist(list):
	return functools.reduce(operator.iconcat, list, [])

# lists available menu options
def list_menu_options():
	for idx, val in enumerate(menu_options):
		print(idx, val)

# returns current month constant
def get_curr_month():
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


sh = None

# authenticates service account and initializes spreadsheet
def auth_and_init():
	global sh # required to be accessed elsewhere during read/write operations
	print("Authenticating...")
	gc = authenticate_gs()
	print("Setting up menu options...")	
	sh = initialize_gs(gc)
	setup_menu_options(sh)

# validates menu option
def validate_menu_option(option):
	if(not option.isnumeric()):
		print("Option must be numeric")
		return False
	if(int(option) > 0 and int(option) < len(menu_options)):
		print("Selected option " + option + " found: " + str(menu_options[int(option)]))
		return True
	else:
		print("Selected option " + option + " not found")
		return False

# validates if a proper currency number
def validate_value(value):
	if(not value.replace('.','',1).isdigit()):
		print("Provided value " + str(value) + " must be a number" + ("", ". Please use '.' for input of decimal values.")[value.replace(',','',1).isdigit()])
		return False
	elif(float(value) <= 0):
		print("Provided value " + str(value) + " must be positive")
		return False
	elif(round(float(value), 2) == 0):
		print("Provided value " + str(value) + " is too low.")
		return False
	
	return True

# formats a string to a google spreadsheet number e.g. '2.5' -> '2,5'
def format2gsnumber(string):
	if(string.replace('.','',1).isdigit()):
		string = string.replace(".", ",")
		return string
	else:
		raise Exception(string + " is not a number")

def append_value_to_expenses(option, value):
	# get month column to retrieve values from
	month_col = get_curr_month()

	# find the row corresponding to the menu_option
	option_row = sh.sheet1.find(menu_options[int(option)], in_column=1).row

	if (option_row == None):
		raise Exception("Unexpected error: row for menu option " + option + " not found!")
	else:
		cell_position = month_col+str(option_row)

		# determine expense item and value to be affected
		str_expense_item = sh.sheet1.get(COL_OPTIONS+str(option_row))[0][0]

		# there may be no values yet saved...
		try:
			expense_value = sh.sheet1.get(cell_position)
			# get the existing value's formula
			expense_value_formula = sh.sheet1.acell(cell_position, value_render_option='FORMULA').value
			##delete expense_value_formula = flattenlist(expense_value_formula)

			print("Appending " + format2gsnumber(str(value)) + 
				  " to " + str_expense_item + 
				  ", current value: " + str(expense_value) + " " + str(expense_value_formula))

			# check for formula types
			# e.g. '=1+2' 	-> '=1+2+3'
			if(expense_value_formula.find("=", 0, 1) > -1):		
				expense_value_formula += "+" + format2gsnumber(str(value))
			# e.g. '33' 	-> '=33+34'
			elif(expense_value_formula.isdecimal() or expense_value_formula.isnumeric()):
				expense_value_formula = "=" + expense_value_formula + "+" + format2gsnumber(str(value))
			else:
				raise Exception("Unable to determine proper formula update for cell " + cell_position + " in '" + str_expense_item + "' item")

			# update the cell with the new formula
			sh.sheet1.update_acell(cell_position, expense_value_formula)

			# report the final value
			final_expense_value = sh.sheet1.get(cell_position)[0][0]
			print("Final value set to: " + str(final_expense_value))


		except KeyError:
			print("Expenses item '" + str_expense_item + "' is currently empty (" + 
				  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
				  str(datetime.datetime.now().year) + ")")
			print("Setting " + str_expense_item + 
				  " with " + format2gsnumber(str(value)) + "...")
			sh.sheet1.update(cell_position, format2gsnumber(str(value)))
		
def read_expense_value(option):
	# get month column to retrieve values from
	month_col = get_curr_month()

	# find the row corresponding to the menu_option
	option_row = sh.sheet1.find(menu_options[int(option)], in_column=1).row

	if (option_row == None):
		raise Exception("Unexpected error: row for menu option " + option + " not found!")
	else:
		cell_position = month_col+str(option_row)

		str_expense_item = sh.sheet1.get(COL_OPTIONS+str(option_row))[0][0]
		
		# there may be no values yet saved...
		try:
			str_expense_value = sh.sheet1.get(cell_position)[0][0]	
			str_expense_value_formula = sh.sheet1.acell(cell_position, value_render_option='FORMULA').value
			print(str_expense_item + ": " + str_expense_value + " (" + str_expense_value_formula + ")")
			return 0
		except KeyError:
			print("Expenses item '" + str_expense_item + "' is currently empty (" + 
				  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
				  str(datetime.datetime.now().year) + ")")


# main function: evaluates arguments
if __name__ == "__main__":

	try:
		arguments = docopt(__doc__, version='DEMO 1.0')
		
		if arguments['-l'] or arguments['--list']:

			auth_and_init()
			print("Menu option items:")
			list_menu_options()

		elif arguments['-a'] or arguments['--add']:
			option = arguments['<option>']
			value = arguments['<value>']

			auth_and_init()
			if(validate_menu_option(option) and validate_value(value)):
				print('Adding ' + '${:,.2f}'.format(float(value)) + ' to item' + option + '...')
				append_value_to_expenses(option, round(float(value), 2))

		elif arguments['-r'] or arguments['--read']:
			option = arguments['<option>']

			auth_and_init()
			if(validate_menu_option(option)):
				read_expense_value(option)

		else:
			print(__doc__)

	except AuthenticationFailedException as e: 
		print("Error: " + str(e).strip('\''))
	except Exception as e:
		print("Unkown error occurred.")