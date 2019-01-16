export PYTHONPATH=.
export STATS_FILE = stats.prof
export STATS_METRIC ?= cumtime


all: setup test

setup:
	@pip install --quiet -r development.txt

test:
	@py.test -vvv -s tests/


server:
	@python -m redys.server


performance-server:
	python -m cProfile -o $(STATS_FILE) redys/server.py

performance-stats:
	python -c 'import pstats ; pstats.Stats("$(STATS_FILE)").sort_stats("$(STATS_METRIC)").print_stats()' | less
