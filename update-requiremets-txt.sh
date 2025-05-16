#!/bin/bash
echo "exporting the dependencies from poetry to requirments.txt..."

poetry export -f requirements.txt --output requirements.txt --without-hashes

echo "done."