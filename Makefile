PY=python -m py_compile
.PHONY:
    all
    test
    install
    compile
    clean
#all:
#    @make test
#    @make install
test:
    behave
install:
    pip install -r requirements.txt
compile:
    $(PY) add_expense.py
clean: 
	#rmdir /s /q .\__pycache__
	del /q .\__pycache__\*.*
	rmdir .\__pycache__