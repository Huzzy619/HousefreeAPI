PYTEST_PROCCESS_COUNT = 4

test-sample_app:
	pytest -n $(PYTEST_PROCCESS_COUNT) --cov=sample_app sample_app/tests --cov-report term-missing

test-book_ticket:
	pytest -n $(PYTEST_PROCCESS_COUNT) --cov=ticketing_app ticketing_app/tests --cov-report term-missing

test:
	pytest -n $(PYTEST_PROCCESS_COUNT) \
		--cov=ticketing_app ticketing_app/tests \
		--cov=volunteer_app volunteer_app/tests \
		--cov=emailer emailer/tests \
		--cov=attendee_kyc attendee_kyc/tests \
		--cov-report term-missing

test-seperated-report:
	make test-sample_app
	make test-book_ticket


dev-setup : 
	$ pip install --upgrade pip
	$ pip install -r requirements.dev.txt
	$ pre-commit install


format : 
	$ python -m autoflake --in-place --remove-unused-variables --recursive ./*/*.py
	$ python -m black --preview ./*/*.py 
