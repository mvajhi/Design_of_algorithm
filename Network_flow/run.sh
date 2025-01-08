#!/bin/bash

if [ -z "$1" ]; then
  echo "Please provide the problem name."
  exit 1
fi

name=$1

if [ ! -f "$name.py" ]; then
  echo "File $name.py does not exist."
  exit 1
fi

for input_file in ${name}*.in; do
  if [ -f "$input_file" ]; then
    echo "Running $name.py on input file $input_file"
    python3 "$name.py" < "$input_file"
    echo "-------------------------"
  else
    echo "No input files matching ${name}*.in found."
    exit 1
  fi
done