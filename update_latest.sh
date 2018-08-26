#!/usr/bin/env bash

set -e
echo "Attemping to update bostadsformedlingen to the lastest version"
parent=${PWD##*/}
echo "Current directory: $parent"
if [ $parent = "bostadsformedlingen" ]; then
        rm -r scripts
        echo "Deleted all files in ./bostadsformedlingen/scripts"
        svn export https://github.com/mmodin/bostadsformedlingen/trunk/scripts
        echo "Updated bostadsformedlingen/scripts/ to the lastest version."
else
        echo "Could not find ../bostadsformedlingen/. Please ensure that you are in the correct directory before updating."
        exit 3
fi

