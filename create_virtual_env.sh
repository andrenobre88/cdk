#!/bin/bash
# # TODO: Transform this script into Makefile.
# Run following command to execute:
# >. ./create_virtual_env.sh

# Change option if require a fresh venv installation
DELETE_CURRENT_VENV=no
if [ "${DELETE_CURRENT_VENV}" = "yes" ]; then
  unalias python
  unalias pip
  for FOLDER in $(find . -name 'venv' -o -name '*.eggs' -o -name '*.egg-info' -type d);
    do
      rm -rfv "${FOLDER}"
    done
fi

# Setting AWS Dev account as default
export CDK_DEFAULT_ACCOUNT="12345678910"
export CDK_DEFAULT_REGION="eu-west-1"

# Checking current python and pip
if [ -z "$(whereis python3)" ]; then
  brew cleanup
  brew install python3
  alias python=/usr/bin/python3
  which python3
fi

if [ -z "$(whereis pip3)" ]; then
  curl -O https://bootstrap.pypa.io/get-pip.py
  sudo python3 get-pip.py
  alias pip=/usr/bin/pip3
  which pip3
fi

# Checking if pyenv is installed
if [ -z "$(which pyenv)" ]; then
  printf "\nInstalling pyenv library\n"
  brew install pyenv
  exit 3
fi

# Checking if pyenv version is installed
if [ -d "/Users/$(whoami)/.pyenv/versions/3.8.10" ]; then
  printf "\npyenv version 3.8.10 already exist, skipping installation\n"
else
  printf "\nInstalling pyenv 3.8.10\n"
  pyenv install 3.8.10
fi

# Checking if pyenv version is installed
if [ -d "./venv" ]; then
  printf "\nvenv folder already exist, skipping creation\n"
else
  printf "\nCreating venv folder\n"
  virtualenv venv
fi

# Creating virtual environment
pyenv virtualenv 3.8.10 venv -f
pyenv virtualenv $(pyenv version | awk -F '(' {'print $1'}) venv -f
pyenv local venv
if [ $? -ne 0 ]; then
  printf "\nERROR: Could not create virtual environment\n"
  exit 3
fi

# Verifying pip upgrades
./venv/bin/pip install --upgrade pip

# Installing a project in editable mode
./venv/bin/pip install -e .

# Installing based on requirements files
for REQUIREMENTS in $(find . -name 'requirements.txt' -o -name 'requirements-dev.txt' -type f);
  do
    ./venv/bin/pip install -r "${REQUIREMENTS}" --no-cache-dir --upgrade --upgrade-strategy eager
  done

# Activating virtual environment
. ./venv/bin/activate
