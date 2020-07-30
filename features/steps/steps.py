from behave import given, when, then
from hamcrest import assert_that, has_item
import subprocess
import os, logging
from add_expense import AddExpenses

# ##################################################
# Feature: simple command line documentation usage
# ##################################################

# Scenario: run without any parameters
@given(u'we have add_expense installed')
def step_impl(context):
	assert_that(os.listdir(), has_item('add_expense.py'))

@when(u'we call add_expense without any parameters')
def step_impl(context):
	stream = subprocess.Popen("python add_expense.py", shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
	output = stream.read()
	context.cli_output = output.decode("utf-8") 
	logging.debug(context.cli_output)
	pass
 
@then(u'add_expense should output the usage instructions')
def step_impl(context):	
	if(context.cli_output.find('Usage') > -1):
		assert True
	else:
		assert False


# Scenario: run without any help parameter
@given(u'we have add_expense installed for testing with help shorthand parameter')
def step_impl(context):
	context.execute_steps(u'Given we have add_expense installed')

@when(u'we call add_expense with help parameter "{parameter}"')
def step_impl(context, parameter):
	logging.debug("add_expense.py " + parameter) 
	stream = subprocess.Popen("python add_expense.py " + parameter, shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
	output = stream.read()
	context.cli_output = output.decode("utf-8") 
	logging.debug(context.cli_output)
	pass

@then(u'add_expense should output the instructions keyword "{keyword}"')
def step_impl(context, keyword):	
	logging.debug("keyword: " + keyword)
	logging.debug("context.cli_output: " + context.cli_output)
	logging.debug("test: " + str(context.cli_output.find(keyword) > -1))
	if(context.cli_output.find(keyword) > -1):
		assert True
	else:
		assert False


# Scenario: run with help parameter --help
@given(u'we have add_expense installed for testing with the help full spec parameter')
def step_impl(context):
	context.execute_steps(u'Given we have add_expense installed')

@when(u'we call add_expense with help full label parameter "{parameter}"')
def step_impl(context, parameter):
	logging.debug('parameter: ' + parameter)
	string_to_parse = u'When we call add_expense with help parameter "{new_input}"'.format(new_input=parameter)
	logging.debug('string_to_parse: ' + string_to_parse)
	context.execute_steps(string_to_parse)
		 
@then(u'add_expense should output the instructions keyword "{keyword}" too')
def step_impl(context, keyword):	
	logging.debug('keyword: ' + keyword)
	context.execute_steps(u'Then add_expense should output the instructions keyword "{0}"'.format(keyword))



# ##################################################
# Feature: simple command line read-only usage
# ##################################################

TEST_SPREADSHEET_ID = '2PACX-1vScal8ROjGMx-SyWfGmpc7aAztn-ACMYNFlmx8mZX4DEm4ijTP69DGWcqHlwKvim70LKJI90YbuFAHQ'

# Scenario: run to list options
@given(u'that we have a sample spreadsheet')
def step_impl(context):
	try:
#		addexpenses = AddExpenses()

#		gc = addexpenses.authenticate_gs()

#		gc.client.open(TEST_SPREADSHEET_ID)
	except Exception as exception: 
		logging.exception(str(exception).strip('\''))
		assert False, "Error occurred"

	raise NotImplementedError(u'STEP: Given that we have a sample spreadsheet')

@when(u'we call add_expense with list parameter "{parameter}"')
def step_impl(context, parameter):
    raise NotImplementedError(u'STEP: When we call add_expense with list parameter "-l"')

@then(u'add_expense should output the list of options available on the sample spreadsheet')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then add_expense should output the list of options available on the sample spreadsheet')

# Scenario: run to list options
@given(u'that we have a sample spreadsheet, too')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given that we have a sample spreadsheet, too')

## see above @when(u'we call add_expense with list parameter "-list"')

@then(u'add_expense should output the list of options available on the sample spreadsheet, too')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then add_expense should output the list of options available on the sample spreadsheet, too')