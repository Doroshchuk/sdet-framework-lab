.PHONY: test debug trace typecheck format lint

test:
	pytest

debug:
	pytest -k "$(test)" --headed --slowmo 200 --tracing on

trace:
	@TRACE=$$(find test-results -name trace.zip | tail -n 1); \
	if [ -n "$$TRACE" ]; then \
		playwright show-trace $$TRACE; \
	else \
		echo "No trace.zip found in test-results"; \
	fi

typecheck:
	mypy src

format:
	black src
	ruff check --fix src

lint:
	ruff check src