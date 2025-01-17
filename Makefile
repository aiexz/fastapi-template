registry := docker.io
image := image
version := $(shell python -c 'import app;print(app.__version__)')
platform := linux/amd64
build:
	docker build -t $(registry)/$(image):$(version) . --platform $(platform)

push:
	docker push $(registry)/$(image):$(version)

publish: build push