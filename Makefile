VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

install:
    virtualenv ${VENV_NAME}
	$(VENV_NAME)/bin/activate
    ${PYTHON} pip install -r requirements.txt