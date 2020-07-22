from behave import *
import subprocess

@given('we have add_expense installed')
def step_impl(context):
	pass

@when('we call add_expense without any parameters')
def step_impl(context):
	#stream = os.popen('add_expense.py')
	stream = subprocess.Popen("add_expense.py", shell=True, bufsize=0, stdout=subprocess.PIPE).stdout
	output = stream.read()
	context.cli_output = output.decode("utf-8") 
	print(context.cli_output)
	pass
 
@then('add_expense should output the usage instructions')
def step_impl(context):	
	if(context.cli_output.find('Usage') > -1):
		assert True
	else:
		assert False