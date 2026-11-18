PYTHON ?= python3
export PYTHONPATH := src

.PHONY: example evidence test figures
example evidence:
	$(PYTHON) -m oil_evidence

test:
	$(PYTHON) -m unittest discover -s tests -v

figures: evidence
	$(PYTHON) research/figures.py
