"""ADD EXPENSE

Usage:
	add_expense [-h|--help]
	add_expense [-l|--list]
	add_expense [-a|--add] <option> <value>

Options:
	-h --help Show this screen
	-l --list List options
	-a --add Add new expense
"""

import gspread
import datetime
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
	i=ROW_START_HOME
	while (i<ROW_TOTALS_HOME):		
		option_label = sh.sheet1.get(COL_OPTIONS+str(i))
		if (option_label):
			menu_options.append(option_label)
		##print(int(i%ROW_TOTALS_HOME)+1, sh.sheet1.get(COL_OPTIONS+str(i)))
		i = i + 1

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
	print("Authenticating...")
	gc = authenticate_gs()
	print("Setting up menu options...")
	sh = initialize_gs(gc)
	setup_menu_options(sh)

# validates menu option
def validate_menu_option(option):
	if(not option.isnumeric()):
		print("Option must be numeric")
	if(int(option) > 0 and int(option) < len(menu_options)):
		print("Selected option " + option + " found")
		return True
	else:
		print("Selected option " + option + " not found")
		return False

def append_value_to_expenses(option, value):
	# get month column to retrieve values from
	month_col = get_curr_month()
	
	print("Appending " + value + " to " +
		  sh.sheet1.get(COL_OPTIONS+str(ROW_TOTALS_HOME)), 
		  sh.sheet1.get(month_col+str(ROW_TOTALS_HOME)))


# main function: evaluates arguments
if __name__ == "__main__":

	arguments = docopt(__doc__, version='DEMO 1.0')
	
	if arguments['-l'] or arguments['--list']:

		auth_and_init()
		print("Menu options:")
		list_menu_options()

	elif arguments['-a'] or arguments['--add']:
		option = arguments['<option>']
		value = arguments['<value>']

		print('Adding ' + value + ' to ' + option + '...')

		auth_and_init()
		if(validate_menu_option(option)):
			append_value_to_expenses(option, value)

	else:
		print(arguments)