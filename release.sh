#!/bin/bash
# For release 0.1.2:
# 1. Ensure git working directory is clean.
# 2. Run this file providing one argument: version. Example:
# ./release.sh 0.1.2

# Validate input arguments.
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # no color

if [ $# -eq 0 ]; then
    echo -e "${RED}ERROR:${NC} Release version must be specified! For example:"
    echo -e "${GREEN}./release.sh 0.1.2${NC}"
    exit 1
elif [ $# -gt 1 ]; then
    echo -e "${RED}ERROR:${NC} Unexpected arguments! There must be exactly one argument: version. For example:"
    echo -e "${GREEN}./release.sh 0.1.2${NC}"
    exit 1
fi

if ! [[ "$1" =~ ^[0-9](\.[0-9])*$ ]]; then
    echo -e "${RED}ERROR:${NC} Version must comply with '^[0-9](\.[0-9])*$' regex! For example:"
    echo -e "${GREEN}0${NC}"
    echo -e "${GREEN}0.1${NC}"
    echo -e "${GREEN}0.1.2${NC}"
    exit 1
fi

# Echo each command from now onwards:
set -x
# 0. Checkout to master:
git checkout master
git pull
# 1. Update pyproject.toml version:
sed -E -i "s/version = \"[0-9](\.[0-9])*\"/version = \"$1\"/g" pyproject.toml
# 2. Update pyproject.toml requires-python if needed.
# 3. Update pyproject.toml classifiers if needed.
# 4. Prepare release commit and tag:
git commit --allow-empty -m "Release $1"
git tag -a "$1" -m"Release $1 tag"
# 5. Build pypi package:
python3 -m build
# 6. Push package to pypi:
python3 -m twine upload --repository pypi dist/*
# 7. Push release commit and tag to origin:
git push