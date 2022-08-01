#!/bin/bash

# Remove old docs to force rebuild
rm -r _build/
# Generate API docs
sphinx-apidoc -f -o . ../nedrex/

sed -i .bak 's/^nedrex$/API/g' modules.rst
rm modules.rst.bak
sed -i .bak 's/^======$/===/g' modules.rst
rm modules.rst.bak

make html
