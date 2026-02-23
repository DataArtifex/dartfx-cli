#!/bin/bash

# Simple script to rename the project and package
# Usage: ./rename.sh "new-project-name" "new_package_name"

OLD_PROJECT="dartfx-cli"
OLD_PACKAGE="cli"

NEW_PROJECT=$1
NEW_PACKAGE=$2

if [ -z "$NEW_PROJECT" ] || [ -z "$NEW_PACKAGE" ]; then
    echo "Usage: ./rename.sh <new-project-name> <new_package_name>"
    echo "Example: ./rename.sh my-cool-app my_cool_app"
    exit 1
fi

echo "Renaming project from $OLD_PROJECT to $NEW_PROJECT"
echo "Renaming package from $OLD_PACKAGE to $NEW_PACKAGE"

# 1. Rename the package directory
if [ -d "src/dartfx/$OLD_PACKAGE" ]; then
    mv "src/dartfx/$OLD_PACKAGE" "src/dartfx/$NEW_PACKAGE"
fi

# 2. Remove stale lock files and environments if they exist
rm -f uv.lock
rm -rf .hatch/
rm -rf .venv/

# 3. Replace strings in files
# Using LC_ALL=C to avoid sed issues on macOS with non-UTF8 characters if any
# We use -i '' for macOS compatibility (sed)
# We also exclude __pycache__ to avoid processing binary files
FIND_CMD="find . -type f -not -path '*/.*' -not -path '*/__pycache__*' -not -path './rename.sh'"

export LC_ALL=C
export LANG=C

$FIND_CMD -exec sed -i '' "s/$OLD_PROJECT/$NEW_PROJECT/g" {} +
$FIND_CMD -exec sed -i '' "s/$OLD_PACKAGE/$NEW_PACKAGE/g" {} +
$FIND_CMD -exec sed -i '' "s/DataArtifex\/$OLD_PROJECT/DataArtifex\/$NEW_PROJECT/g" {} +

# Specific fix for ruff known-first-party if it uses the top-level folder
sed -i '' "s/known-first-party = \[\"dartfx\"\]/known-first-party = \[\"dartfx\", \"$NEW_PACKAGE\"\]/g" pyproject.toml

echo "Done! Please verify changes and run 'uv sync'."
