from behave import given, when, then
import subprocess

# Scenario: run without any parameters
@given(u'we have add_expense installed')
def step_impl(context):
	pass

@when(u'we call add_expense without any parameters')
def step_impl(context):
	stream = subprocess.Popen("add_expense.py", shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
	output = stream.read()
	context.cli_output = output.decode("utf-8") 
	#DEBUG print(context.cli_output)
	pass
 
@then(u'add_expense should output the usage instructions')
def step_impl(context):	
	if(context.cli_output.find('Usage') > -1):
		assert True
	else:
		assert False


# Scenario: run without any help parameter
@given(u'we have add_expense installed and will be testing the help shorthand parameter')
def step_impl(context):
	pass

@when(u'we call add_expense with help parameter "{parameter}"')
def step_impl(context, parameter):
	#DEBUG print("add_expense.py " + parameter) 
	stream = subprocess.Popen("add_expense.py " + parameter, shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
	output = stream.read()
	context.cli_output = output.decode("utf-8") 
	#DEBUG print(context.cli_output)
	pass

@then(u'add_expense should output the instructions keyword "{keyword}"')
def step_impl(context, keyword):	
	#DEBUG print("keyword: " + keyword)
	#DEBUG print("context.cli_output: " + context.cli_output)
	#DEBUG print("test: " + str(context.cli_output.find(keyword) > -1))
	if(context.cli_output.find(keyword) > -1):
		assert True
	else:
		assert False


# Scenario: run with help parameter --help
@given(u'we have add_expense installed and will be testing the help full spec parameter')
def step_impl(context):
	pass

@when(u'we call add_expense with help full label parameter "{parameter}"')
def step_impl(context, parameter):
	print('parameter: ' + parameter)
	string_to_parse = u'When we call add_expense with help parameter "{new_input}"'.format(new_input=parameter)
	print('string_to_parse: ' + string_to_parse)
	context.execute_steps(string_to_parse)
		 
@then(u'add_expense should output the instructions keyword "{keyword}" too')
def step_impl(context, keyword):	
	print('keyword: ' + keyword)
	context.execute_steps(u'Then add_expense should output the instructions keyword "{0}"'.format(keyword))