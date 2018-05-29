
flake8:
	@docker-compose exec web flake8 . --statistics --show-source

flake8_diff:
	@git diff $(from)..$(to) -- web | $(PYTHONPATH)/bin/flake8 --config=web/.flake8 --diff  --statistics --show-source