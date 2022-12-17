#!/bin/bash

# Print the latest version notes from chagelog.md

# Store the filepath in a variable
filepath="docs/source/changelog.md"

# Read the contents of the file into a variable
contents=$(<"$filepath")

# Set a flag to track whether we are inside the desired block of text
in_block=false
count=0
# Loop through each line in the file
while read -r line; do
  # Check if the line starts with a "#" character
  if [[ $line =~ ^# ]]; then
    # Set the flag to indicate that we are inside the block
    in_block=true
  fi

  # Check if the line contains the "##" pattern
  if [[ $line =~ "##" ]]; then
    # If we are inside the block, set the flag to indicate that we are no longer inside the block
    if $in_block; then
    #   in_block=false
      count=$((count + 1))
    fi
  fi

  if [ $count -ge 3 ]; then
    # Break
    break
  fi

#   # If we are inside the block, print the line
#   if $in_block; then
  echo "$line"
#   fi
done <<< "$contents"
