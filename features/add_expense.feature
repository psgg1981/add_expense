Feature: simple program command line call with no parameters

	Scenario: run without any parameters 
		Given we have add_expense installed
		 When we call add_expense without any parameters
		 Then add_expense should output the usage instructions