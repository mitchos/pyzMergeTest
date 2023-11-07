COLOR_OK=\\x1b[0;32m
COLOR_NONE=\x1b[0m
COLOR_ERROR=\x1b[31;01m
COLOR_WARNING=\x1b[33;01m
COLOR_ZSCALER=\x1B[34;01m

VERSION=$(shell grep -E -o '(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?' ./zscaler/__init__.py)

help:
	@echo "$(COLOR_ZSCALER)"
	@echo "  ______              _           "
	@echo " |___  /             | |          "
	@echo "    / / ___  ___ __ _| | ___ _ __ "
	@echo "   / / / __|/ __/ _\` | |/ _ \ '__|"
	@echo "  / /__\__ \ (_| (_| | |  __/ |   "
	@echo " /_____|___/\___\__,_|_|\___|_|   "
	@echo "                                  "
	@echo "                                  "
	@echo "$(COLOR_NONE)"
	@echo "$(COLOR_OK)Zscaler SDK Python$(COLOR_NONE) version $(COLOR_WARNING)$(VERSION)$(COLOR_NONE)"
	@echo ""
	@echo "$(COLOR_WARNING)Usage:$(COLOR_NONE)"
	@echo "$(COLOR_OK)  make [command]$(COLOR_NONE)"
	@echo ""
	@echo "$(COLOR_WARNING)Available commands:$(COLOR_NONE)"
	@echo "$(COLOR_OK)  help$(COLOR_NONE)           Show this help message"
	@echo "$(COLOR_WARNING)build$(COLOR_NONE)"
	@echo "$(COLOR_OK)  build:dist                  Build the distribution for publishing$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)publish$(COLOR_NONE)"
	@echo "$(COLOR_OK)  publish:test                Publish distribution to testpypi (Will ask for credentials)$(COLOR_NONE)"
	@echo "$(COLOR_OK)  publish:prod                Publish distribution to pypi (Will ask for credentials)$(COLOR_NONE)"

build\:dist:
	python3 setup.py sdist bdist_wheel
	rm -rf __pycache__
	rm -rf dist
	rm -rf zscaler_sdk_python.egg-info

publish\:test:
	python3 -m twine upload --repository testpypi dist/*

publish\:prod:
	python3 -m twine upload dist/*
