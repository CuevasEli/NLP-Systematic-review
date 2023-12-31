.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn api.topic_api:app --reload

install_package:
	pip install -e .

docker_build:
	docker build --platform linux/amd64 -t ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod .

docker_push:
	docker push ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod

docker_run:
	docker run -e PORT=8000 -p 8000:8000 --env-file .env ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod

docker_interactive:
	docker run -it --env-file .env ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod /bin/bash

docker_deploy:
	gcloud run deploy --image ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod --memory ${GCR_MEMORY} --region ${GCP_REGION}
