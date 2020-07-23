# add_expense
Simple expenses tool tracking CLI, integrated with your well-defined Google Spreadsheet. 

Makes use of gspread (https://gspread.readthedocs.io/en/latest/), a Python library for Google Sheets API.

## why use it?
This is just a fun program I wrote with Python to exercise a few concepts, but this may still come in handy when all you want is a straightforward approach to fast type and input your monthly expenses (i.e. no mouse pointing and clicking). Sure, it certainly requires improvements so be sure to check out the [Issues area](https://github.com/psgg1981/add_expense/issues).

## how to use it?
First you'll need a spreadsheet similar to [this one](https://docs.google.com/spreadsheets/d/e/2PACX-1vScal8ROjGMx-SyWfGmpc7aAztn-ACMYNFlmx8mZX4DEm4ijTP69DGWcqHlwKvim70LKJI90YbuFAHQ/pubhtml).

![sample expenses in google spreadsheet](https://drive.google.com/uc?export=view&id=1kFs3Jsb_xqS8WqrFxBonAmjNta6aPBv- "Sample Expenses in Google Spreadsheet") 

## how to install it?
1. Clone or download this project

![image showing clone and download actions in GitHub](https://drive.google.com/uc?export=view&id=1h_sGUhFhh7HSAjrTpwFpFFpuI5nOcMjq "GitHub's clone or download")

2. Install [python3](https://www.python.org/downloads/)

3. Setup Google API authentication to your spreadsheet as explained [in gspread's documentation](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account)

4. Configure the month and expense item coordinates (see next section)

## how to configure it?
For now, the spreadsheet cells of each expense item (1st column of the above spreadsheet sample) and each month (first row) need to be referenced in the code. Just edit the following few values, in respect to the location of each column and row:

```python
# Constants
COL_OPTIONS                 = 'A'

ROW_START_HOME 	 	    =  6
ROW_TOTALS_HOME 	    = 18

COL_JAN		            = 'B'
COL_FEB		            = 'C'
COL_MAR		            = 'D'
COL_APR		            = 'E'
COL_MAY		            = 'F'
COL_JUN		            = 'G'
COL_JUL		            = 'H'
COL_AUG		            = 'I'
COL_SEP		            = 'J'
COL_OCT		            = 'K'
COL_NOV		            = 'L'
COL_DEC		            = 'M'
```

## how to run it?

To list the current expense items in your spreadsheet type `add_expense.py --list` or `add_expense.py -l`. This should present something like the below:
```
Authenticating...
Setting up menu options...
Menu option items:
0 Mortage-rent
1 Phone
2 Electricity
3 Gas
4 Water
5 Cable
6 Maintenance-repairs
7 Supplies
8 Other
```

To add a new expense, e.g. to your electricity bill, type `add_expense.py -a 2 80.50` or `add_expense.py --add 2 80.50`

and the result will be something similar to this:

```
Authenticating...
Setting up menu options...
Selected option 2 found: Electricity
Expenses item 'Electricity' is currently empty (July 2020)
Setting Electricity with $80.50...
```
> Note: as of the time of this writing there is still too much verbosity in user's feedback. This will be corrected in the near future.

![example of an updated expense entry in your google spreadsheet](https://drive.google.com/uc?export=view&id=1ckpU2WDfwiKi66Z1nbDYGMy10OIPs_ER "example of an updated expense entry in your google spreadsheet")
> Note: updates are always done to the current date's month.

To read the current expenses from your spreadsheet type `add_expense.py -r 6` or `add_expense.py --read 6` (i.e. *Maintenance/repairs* for this example)

```
Authenticating...
Setting up menu options...
Selected option 6 found: Maintenance/repairs
Maintenance/repairs: 1 117,84 (=391,41+192,45+478,11+55,87)
```
> Note: besides the total, the full formula is also shown.

See more instructions by typing `add_expense.py --help`
```
ADD EXPENSE appends currency amounts to your Google Spreadsheet.

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
```
