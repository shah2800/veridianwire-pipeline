#!/bin/bash
# Roll back to last git tag on deploy failure
set -e
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  echo "No tag found for rollback"
  exit 1
fi
git checkout "$LAST_TAG"
echo "Rolled back to $LAST_TAG"
