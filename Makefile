export PYTHONPATH=.

all: setup test

setup:
	@pip install --quiet -r development.txt

test:
	@py.test -vvv -s tests/


server:
	@python -m redys.server
