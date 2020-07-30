Feature: simple command line read-only usage

	Scenario: run with list shorthand parameter
		Given that we have a sample spreadsheet
		 When we call add_expense with list parameter "-l"
		 Then add_expense should output the list of options available on the sample spreadsheet

	Scenario: run with list parameter full label
		Given that we have a sample spreadsheet, too
		 When we call add_expense with list parameter "-list"
		 Then add_expense should output the list of options available on the sample spreadsheet, too
