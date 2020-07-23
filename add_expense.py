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

ROW_START_HOME 	 	 =  6
ROW_TOTALS_HOME 	 = 18
ROW_TOTALS_TRANSPORT = 31
ROW_TOTALS_KIDS 	 = 45
ROW_TOTALS_EDUCATION = 54


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

# authenticates service account on google spreadsheets
def authenticate_gs():
	return gspread.service_account()

# opens google spreadsheet
def initialize_gs(gc):
	return gc.open("Contas Casa")

menu_options = []

# initializes available menu options
def setup_menu_options(sh):
	# e.g. get A6:A17
	range_of_cells_contents = sh.sheet1.get(COL_OPTIONS+str(ROW_START_HOME)+':'+ COL_OPTIONS+str(ROW_TOTALS_HOME - 1))
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
	if(not value.isnumeric()):
		print("Value must be numeric")
		return False
	if(float(value) <= 0):
		print("Value must be positive")
		return False
	
	return True

def append_value_to_expenses(option, value):
	# get month column to retrieve values from
	month_col = get_curr_month()

	# find the row corresponding to the menu_option
	option_row = sh.sheet1.find(menu_options[int(option)], in_column=1).row

	if (option_row == None):
		raise Exception("Unexpected error: row for menu option " + option + " not found!")
	else:
		# determine expense item and value to be affected
		str_expense_item = sh.sheet1.get(COL_OPTIONS+str(option_row))[0][0]

		# there may be no values yet saved...
		try:
			str_expense_value = str(sh.sheet1.get(month_col+str(option_row)))
			print("Appending " + str(value) + 
				  " to " + str_expense_item + 
				  ", current value: " + str_expense_value)

		except KeyError:
			print("Expenses item '" + str_expense_item + "' is currently empty (" + 
				  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
				  str(datetime.datetime.now().year) + ")")
			print("Setting " + str_expense_item + 
				  " with " + str(value) + "...")
			sh.sheet1.update(month_col+str(option_row), value)
		
def read_expense_value(option):
	# get month column to retrieve values from
	month_col = get_curr_month()

	# find the row corresponding to the menu_option
	option_row = sh.sheet1.find(menu_options[int(option)], in_column=1).row

	if (option_row == None):
		raise Exception("Unexpected error: row for menu option " + option + " not found!")
	else:
		str_expense_item = sh.sheet1.get(COL_OPTIONS+str(option_row))[0][0]

		# there may be no values yet saved...
		try:
			str_expense_value = sh.sheet1.get(month_col+str(option_row))[0][0]	
			print(str_expense_item + " = " + str_expense_value)
			return 0
		except KeyError:
			print("Expenses item '" + str_expense_item + "' is currently empty (" + 
				  calendar.month_name[int(datetime.datetime.now().month)] + " " + 
				  str(datetime.datetime.now().year) + ")")


# main function: evaluates arguments
if __name__ == "__main__":

	arguments = docopt(__doc__, version='DEMO 1.0')
	
	if arguments['-l'] or arguments['--list']:

		auth_and_init()
		print("Menu option items:")
		list_menu_options()

	elif arguments['-a'] or arguments['--add']:
		option = arguments['<option>']
		value = arguments['<value>']

		print('Adding ' + '${:,.2f}'.format(float(value)) + ' to item' + option + '...')

		auth_and_init()
		if(validate_menu_option(option) and validate_value(value)):
			append_value_to_expenses(option, round(float(value), 2))

	elif arguments['-r'] or arguments['--read']:
		option = arguments['<option>']

		auth_and_init()
		if(validate_menu_option(option)):
			read_expense_value(option)

	else:
		print(__doc__)