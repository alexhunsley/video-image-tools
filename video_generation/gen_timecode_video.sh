!#/bin/bash

# Generates a low FPS video with the elapsed hours/mins/secs/millisecs since video start

# replace with "" to disable force overwrite
FORCE_OVERWRITE="-y"

VIDEO_LENGTH_MINS=60
VIDEO_RES="480x270"
FPS=2
OUTPUT_VIDEO_FILENAME=output.mp4

VIDEO_LENGTH_SECS="$((${VIDEO_LENGTH_MINS} * 60))"

FONT_FILE="/Library/Fonts/Arial Unicode.ttf"
FONT_SIZE=60

ffmpeg ${FORCE_OVERWRITE} -f lavfi -i color=c=black:s=${VIDEO_RES}:d=${VIDEO_LENGTH_SECS} -r ${FPS} \
	-vf "drawtext=fontfile=${FONT_FILE}:fontsize=${FONT_SIZE}:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:text='%{pts\:hms}'" ${OUTPUT_VIDEO_FILENAME}
