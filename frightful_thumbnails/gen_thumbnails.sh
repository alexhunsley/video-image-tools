#!/bin/bash

# 1 frame every other second
FPS="1/2"

for i in *.mp4
do
	echo "${i}"
	mkdir "${i}.grabs"

	ffmpeg -i "${i}" -r "${FPS}" -f image2 "${i}.grabs/${i}--%09d.jpg"
done

echo "Done"
echo
