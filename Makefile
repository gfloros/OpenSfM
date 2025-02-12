# Default shell is sh, set to bash
SHELL := /bin/bash

# Run as single shell session
.ONESHELL:

# Use bash strict mode
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
.SHELLFLAGS := -eu -o pipefail -c

# Delete target if make rule fails
# https://innolitics.com/articles/make-delete-on-error/
.DELETE_ON_ERROR:

# Warn if using undefined variables
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.DEFAULT_GOAL := help

.PHONY: help install local bash env

# Self documenting makefile
# To add documentation for a specific target
# add a comment starting with ## after the rule name
help:
	@echo "OpenSfM"
	@grep -E '^[a-zA-Z_0-9%-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

local: ## Build docker image locally
	docker build -f $(shell pwd)/Dockerfile.ceres2 -t opensfm-poselab .

bash: ## Start a bash session inside the container
	docker run -v $(shell pwd)/data/:/data -v $(shell pwd):/code --rm -it --entrypoint bash opensfm-poselab
