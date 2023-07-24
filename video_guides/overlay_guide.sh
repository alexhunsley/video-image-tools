#!/bin/bash
#
# overlay_guide.py
#

if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    echo "Usage: $0 <file1.mp4> <file2.mp4> ... or $0 all"
    exit 1
fi

image_path="/Users/alexhunsley/Documents/dev/____currentProjects/video-image-tools/video_guides/grid.png"

if [ "$1" == "all" ]; then
    files=(*.mp4)
else
    files=("$@")
fi


for file in "${files[@]}"; do

    base_name=$(basename "$file" .mp4)

	ffmpeg -y -i "$file" -loop 1 -i "$image_path" \
	   -filter_complex "\
	    [0:v]scale='min(768,iw)':-2,hue=s=0,negate,setsar=1[video]; \
	    [1:v][video]scale2ref[img][mv]; \
	    [mv][img]overlay=eof_action=pass[ovr]; \
	    [ovr]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:text='%{eif\:mod(t,3600)/60\:d\:2}\:%{eif\:mod(t,60)\:d\:2}\:%{eif\:mod(t*100,100)\:d\:2}':fontcolor=red@0.8:x=10:y=10[txt]; \
	    [txt]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:text='$file':fontcolor=red@0.8:x=10:y=70:enable='between(t,0,1)'[out]; \
	    [0:v]scale=-1:40,fps=5[small]; \
	    [out][small]overlay=W-w-10:10[vout]" \
	   -map "[vout]" -r 5 "${base_name}_i.mp4"

done
