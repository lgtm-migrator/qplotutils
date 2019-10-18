#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR/..
source ~/venvs/python3.7_minimal/bin/activate

pytest --cov=qplotutils --cov-report html:coverage $DIR/../tests
deactivate

cd "$DIR/../docs"
make html