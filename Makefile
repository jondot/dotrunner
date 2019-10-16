init:
	pip install pipenv
travis-enable:
	travis enable
install:
	pipenv install --dev
env:
	pipenv shell
test:
	pytest
watch:
	ptw -- -v
dist:
	rm -rf dist
	rm -rf build
	pandoc --from=markdown --to=rst --output=README.rst README.md
	python setup.py sdist bdist_wheel
dist-install:
	python setup.py install
dist-release:
	make dist && make release
release:
	twine upload dist/*
wtf:
	rm -rf .cache
.PHONY: init install test dist
