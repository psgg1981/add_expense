Feature: simple command line documentation usage

	Scenario: run without any parameters
		Given we have add_expense installed
		 When we call add_expense without any parameters
		 Then add_expense should output the usage instructions

	Scenario: run with help shorthand parameter
		Given we have add_expense installed and will be testing the help shorthand parameter
		 When we call add_expense with help parameter "-h"
		 Then add_expense should output the instructions keyword "Usage"

	Scenario: run with help parameter full label
		Given we have add_expense installed and will be testing the help full spec parameter
		 When we call add_expense with help full label parameter "--help"
		 Then add_expense should output the instructions keyword "Usage" too