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
    behave --stop -s
    # use this instead to capture all debug entries: behave --stop --no-logcapture --logging-level DEBUG
lint:
    pylint add_expense.py
clean: 
    rmdir /s /q .\src\__pycache__
    rmdir /s /q .\dist
install:
    pip install -r requirements.txt
compile:
    clean
    install
    $(PY) add_expense.py