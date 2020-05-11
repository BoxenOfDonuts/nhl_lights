.PHONY: prepare_venv cache build deploy

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

prepare_venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
    test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
    ${PYTHON} -m pip install -U pip
    ${PYTHON} -m pip install -r requirements.txt
    touch $(VENV_NAME)/bin/activate