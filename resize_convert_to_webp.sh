#!/bin/bash

# Check if a directory was provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Directory to process
INPUT_DIR=$1

# Find and process all .png files in the directory and its subdirectories
find "$INPUT_DIR" -type f -name "*.png" | while read -r file; do
    # Get the directory and base name of the file
    dir=$(dirname "$file")
    base=$(basename "$file" .png)

    # Temporary file and output file
    tmp_file="${dir}/tmp_${base}.png"
    webp_file="${dir}/${base}.webp"

    echo "Processing: $file"

    # Step 1: Shrink the image using vips
    vips shrink "$file" "$tmp_file" 2 2

    # Step 2: Convert the shrunken image to WebP using cwebp
    cwebp "$tmp_file" -o "$webp_file"

    # Step 3: Remove the temporary file
    rm "$tmp_file"

    echo "Created: $webp_file"
done

