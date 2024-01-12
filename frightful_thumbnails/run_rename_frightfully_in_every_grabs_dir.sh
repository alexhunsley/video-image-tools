#!/bin/bash

# Iterate over directories matching "*.grabs" in the current directory

for dir in *.grabs; do
    # Check if the directory exists and is a directory
    if [[ -d "$dir" ]]; then
        echo " ---- Entering directory: $dir"
        cd "$dir" # Change into the directory

        # Run script.sh if it exists
        # if [[ -f "script.sh" ]]; then
        #     echo "Running script.sh in $dir"
        #     ./script.sh
        # else
        #     echo "script.sh not found in $dir"
        # fi


        python /Users/alexhunsley/Documents/dev/____currentProjects/video-image-tools/frightful_thumbnails/rename_images_frightfully.py

        cd .. # Come back out of the directory
        echo " ---- Exited directory: $dir"
    fi
done
