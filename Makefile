.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn api.topic_api:app --reload

install_package:
	pip install -e .
