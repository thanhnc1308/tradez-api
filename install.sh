#!/bin/sh

while read requirements_file; do
dependency ="$(echo "${requirements_file}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
if pip install "$dependency"; then
    echo "$dependency is installed correctly"
else
    echo "Could not install following dependency"
    fi
done < requirements/development.txt