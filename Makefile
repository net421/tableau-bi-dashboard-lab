.PHONY: install generate build validate test evidence verify clean-generated

install:
	python -m pip install -r requirements.txt

generate:
	python data/generate_bi_source.py

build: generate
	python validation/build_dashboard_exports.py

validate:
	python validation/validate_bi_metrics.py

test:
	python -m pytest -q

evidence:
	python validation/generate_dashboard_evidence.py

verify: clean-generated build validate test evidence

clean-generated:
	rm -f data/tableau_ready_exports/*.csv
	rm -f screenshots/*.png
	rm -f validation/bi_metric_validation_report.csv
