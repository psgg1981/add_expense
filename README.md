# add_expense
Simple expenses tool tracking CLI, integrated with a well-defined Google Spreadsheet
Makes use of gspread (https://gspread.readthedocs.io/en/latest/), a Python API for Google Sheets.

## how to use it?
First you'll need a spreadsheet similar to [this one](https://docs.google.com/spreadsheets/d/e/2PACX-1vScal8ROjGMx-SyWfGmpc7aAztn-ACMYNFlmx8mZX4DEm4ijTP69DGWcqHlwKvim70LKJI90YbuFAHQ/pubhtml).

![sample expenses in google spreadsheet](https://drive.google.com/uc?export=view&id=1kFs3Jsb_xqS8WqrFxBonAmjNta6aPBv- "Sample Expenses in Google Spreadsheet") 

## how to install it?
1. Besides [cloning/downloading this project](https://drive.google.com/uc?export=view&id=1h_sGUhFhh7HSAjrTpwFpFFpuI5nOcMjq) you'll also require [python3](https://www.python.org/downloads/). 
2. Setup Google API authentication to your spreadsheet as explained [in this section](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account)

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

To list the current expense items in your spreadsheet type `add_expense.py --list` or `add_expense.py -l`

To add a new expense in your spreadsheet type `add_expense.py -a 1 2` or `add_expense.py --add 1 2`

To read the current expenses from your spreadsheet type `add_expense.py -r 1` or `add_expense.py --read 1` where 1 is the options listed in the first command above

See more instructions typing `add_expense.py --help`
