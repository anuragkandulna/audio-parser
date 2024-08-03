#!/usr/bin/env bash

# Function to check if python 3 is installed
check_python_installed() {
  if command -v python3 &> /dev/null
  then
    echo "Python 3 is already installed. Version: $(python3 --version)"
  elif command -v python &> /dev/null
  then
    echo "Python 3 is already installed. Version: $(python --version)"
  else
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
  fi
}

create_virtualenv() {
  # Cleaning up local v-environment
  if [ -d $ENV ]; then
    echo "Python Virtual environment ${ENV} already exist. Cleaning up the environment..."
    rm -rf "${ENV}/"
    echo "Successfully cleared the old environment..."
  fi

  # Creating a new environment
  echo "Creating new virtual environment..."
  if command -v python3 &> /dev/null
  then
    python3 -m venv $ENV
  else
    python -m venv $ENV
  fi

  # Verify environment creation was success
  if [ $? -eq 0 ]; then
    echo "Successfully created virtual environment in directory: ${ENV}"
  else
    echo "Failed to create virtual environment. Exiting now!"
    exit 1
  fi

}


# ------------------------------------------ START HERE ----------------------------------------- #
# Start python virtual environment creation with hidden dir .pyenv312
ENV=".venv"
GIT_IGNORE=".gitignore"

# Invoke functions to do the respective task
check_python_installed
create_virtualenv

# Add ENV to .gitignore
if grep -Fxq "${ENV}" $GIT_IGNORE
then
  echo "Adding ${ENV} to ${GIT_IGNORE} file..."
  echo "" >> $GIT_IGNORE
  echo "# Python virtual environment created by Project Orion" >> $GIT_IGNORE
  echo "${ENV}/" >> $GIT_IGNORE
  echo "Successfully added dir ${ENV} to file ${GIT_IGNORE}. Just commit the changes and push."
else
  echo "Python virtual environment dir ${ENV} already added to ${GIT_IGNORE} file!"
fi