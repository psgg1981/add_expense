clean: 
	rmdir /s __pycache__

init:
	pip install -r requirements.txt

test:
	behave