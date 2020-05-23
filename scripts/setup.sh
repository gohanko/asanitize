#!/bin/bash

if [ $VIRTUAL_ENV ] ; then
    echo "User is inside a virtual environment, deactivating ..."
    deactivate
fi

python3 -c "import virtualenv"

if [ $? -eq 1 ] ; then
    echo ""
    echo "Installing virtualenv using pip ..."
    pip3 install virtualenv --quiet
fi

if [ -d "./venv" ] ; then
    echo "Deleting existing venv environment ..."
    rm -rf ./venv/
fi

echo "Creating virtual environment called venv ..."
python3 -m virtualenv venv --quiet

echo "Activating the virtual environment ..."
source ./venv/bin/activate

echo "Installing dependencies in the virtual environment ..."
pip install -r requirements.txt --quiet