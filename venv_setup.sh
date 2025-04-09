#!/bin/bash

# Create virtual environment
python3 -m venv env

# Activate it and install dependencies
source ./env/Scripts/activate
source ./env/Scripts/activate pip install --upgrade pip
source ./env/Scripts/activate pip install -r requirements.txt
source ./env/Scripts/activate pip install ipykernel

# Add as Jupyter kernel
source ./env/Scripts/activate python -m ipykernel install --user --name=ask-your-pdf-env --display-name "Python (ask-your-pdf-env)"

echo "etup complete. Kernel 'Python (ask-your-pdf-env)' is ready."

deactivate
