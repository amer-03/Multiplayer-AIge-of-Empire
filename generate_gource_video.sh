#!/bin/bash

# Check if the user provided an argument for the output video name
if [ -z "$1" ]; then
  echo "Usage: $0 <output_video_name>"
  exit 1
fi

# Get the date of the last commit
LAST_COMMIT_DATE=$(git log -1 --format=%cd --date=format:'%Y-%m-%d')

# Append the last commit date to the output video name
OUTPUT_VIDEO="${1}_${LAST_COMMIT_DATE}.mp4"

gource --font-size 20 --seconds-per-day 0.1 --auto-skip-seconds 1 --viewport 1920x1080 -o | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i --vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 23 -vf scale=1280:-2 -threads 0 -bf 0-b:v 2M "$OUTPUT_VIDEO"

