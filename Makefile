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
    behave --stop
    # use this instead to capture all debug entries: behave --stop --no-logcapture --logging-level DEBUG
install:
    pip install -r requirements.txt
compile:
    $(PY) add_expense.py
clean: 
	#rmdir /s /q .\__pycache__
	del /q .\__pycache__\*.*
	rmdir .\__pycache__