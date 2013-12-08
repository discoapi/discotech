TESTS = test_provider test_providerseacher

.PHONY: tests

install:
	python setup.py install --user

docs: install
	epydoc -v discotech -o docs

tests: install
	cd tests && python -m unittest -v $(TESTS)

discoapi_docs: docs
	python docsExtracter.py && cp api_docs/* /home/stas/Sites/discoapi/public_html/discotech/docs
