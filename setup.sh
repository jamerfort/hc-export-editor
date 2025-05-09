#!/bin/bash

if [ ! -d venv ]
then
  echo "Creating required virtual environment"
  python3 -m venv venv

  # Activate the environment
  . venv/bin/activate

  # Install the required packages
  pip install -r requirements.txt

else
  # Activate the environment
  . venv/bin/activate
fi

