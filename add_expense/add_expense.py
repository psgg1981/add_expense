"""ADD EXPENSE appends currency amounts to your Google Spreadsheet.

Usage:
	add_expense [-h|--help]
	add_expense [-l|--list]
	add_expense [-a|--add] (<option> <value>) [<month>]
	add_expense [-r|--read] <option> [<month>]

Options:
	-h --help  Show this screen
	-l --list  List options
	-a --add   Add new expense (to current month, by default, else use month 3-letter name e.g. Jan Feb Mar etc.)
	-r --read  Reads expenses amount and formula (of current month, by default, else use month 3-letter name e.g. Jan Feb Mar etc.)
"""

from docopt import docopt
import datetime
import calendar
from add_expense_lib import AddExpenses

# exceptions
class InvalidMonthAbbreviation(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


# main function: evaluates arguments
if __name__ == "__main__":

	addexpenses = AddExpenses()

	try:
		arguments = docopt(__doc__, version='DEMO 1.0')
		
		if arguments['-l'] or arguments['--list']:

			addexpenses.listOptions()

		elif arguments['-a'] or arguments['--add']:
			option = arguments['<option>']
			value = arguments['<value>']
			month = arguments['<month>']

			# if no month option entered then default to current
			if month == None:

				month = int(datetime.datetime.now().month)		# find the month number from today's date
				month = calendar.month_abbr[month]				# find the month abbreviation e.g. Jan from the month number

			addexpenses.submit(option, value, month)

		elif arguments['-r'] or arguments['--read']:

			option = arguments['<option>']
			month = arguments['<month>']

			# if no month option entered then default to current
			if month == None:

				month = int(datetime.datetime.now().month)		# find the month number from today's date
				month = calendar.month_abbr[month]				# find the month abbreviation e.g. Jan from the month number

			addexpenses.readOption(option, month)

		else:
			print(__doc__)

	except AuthenticationFailedException as exception: 
		print("Error: " + str(exception).strip('\''))
	except Exception as exception:
		print("Unknown error occurred.")