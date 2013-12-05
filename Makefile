TESTS = test_provider test_providerseacher

.PHONY: tests

install:
	python setup.py install --user

docs: install
	epydoc -v discotech -o docs

tests: install
	cd tests && python -m unittest -v $(TESTS)
