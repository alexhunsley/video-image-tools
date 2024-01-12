import os
import re
import sys
import math


start_marker = "__bbStart"
middle_marker = "__bbMiddle"
end_marker = "__bbEnd"


def number_bin_digits_needed_to_express_num_values(num_values):

	# edge cases
	if num_values <= 1:
		# 1 value (image) might appear to need 1 bin digit,
		# but 1 is a 2^N+1 value (2^0+1) so we use previous value i.e. 0
		return 0
	elif num_values == 2:
		return 1

	p = math.log(num_values - 2, 2) + 1
	# int is floor()
	req_digits = int(p)
	# print(f"req digits = int(p) = {req_digits}")
	return req_digits


# for i in range(0, 10):
# 	print(f"{i}\t{number_bin_digits_needed_to_express_num_values(i)}")
# sys.exit(0)


# use 1 here if your images start at index 1 (looking at you, ffmpeg)
first_input_image_index = 1
#first_input_image_index = 0


def count_trailing_zeros(num):
	# Convert to binary and remove the "0b" prefix
	binary = bin(num)[2:]
	# Reverse the string and find the first non-zero character
	count = len(binary) - binary.rfind('1') - 1
	return count


def rename_files_in_directory(directory="."):

	working_dir = os.path.abspath(directory)

	print(f"\nRenaming jpgs in directory: {working_dir}\n\n")

	files = [f for f in os.listdir(directory) if f.endswith(".jpg")]

	if len(files) == 0:
		print("Error: no matching files found, exiting.\n\n")
		sys.exit(1)
		
	# helpful bookending tags for minimal search
	# edge cases!
	if len(files) == 1:
		extra_filename_tags = {0: f"{start_marker}{middle_marker}{end_marker}"}
	elif len(files) == 2:
		extra_filename_tags = {0: "start_marker", 1: f"{middle_marker}{end_marker}"}
	else:
		extra_filename_tags = {0: start_marker, int(len(files)/2): middle_marker, len(files) - 1: end_marker}

	print(f"it is: {extra_filename_tags}")

	first_and_last_images_num_digits = number_bin_digits_needed_to_express_num_values(len(files))

	files.sort()

	# find first decimal number with "_" before it
	# pattern = re.compile(r'[_-]\d+')
	# find "__" before digits for the frame number
	pattern = re.compile(r'--\d+')

	# find the first number in the first filename
	first_file = files[0]
	match = pattern.search(first_file)
	frame_num_start_idx, frame_num_end_idx = match.start() + 2, match.end()

	files_processed = 0
	
	for file in files:
		if "__b" in file:
			# Skipping already processed files makes sense, and also allows user to run tool again if images with
			# appropriate continuing numbers were added to an already processed set 
			print(f"** Warning: saw a file that has already been processed? Will not rename it.  {file}")
			continue

		# get decimal number from the filename
		num = int(file[frame_num_start_idx:frame_num_end_idx]) - first_input_image_index

		print(f"num = {num}")
		# Calculate the number of trailing zeros in the binary representation
		if num == 0 or num == len(files) - 1:
			# Special case for image 0 since we need to represent all possible digits in the binary
			# version of file indexes being 0 (this allows any boo number search term to match first image).
			# We also do same treatment for last file too; we ensure both start end files have a 'boo' 
			# that is greater than any other. This allows searching for just first and last images in a video.
			# (Not so helpful for searching for only first and last images across multiple video thumbnails,
			# as videos are usually different lengths and so the boo number for one's video's start+end frame
			# won't usually be that of another)
			number_of_r = first_and_last_images_num_digits
		else:
			number_of_r = count_trailing_zeros(num)

		extra_tag = extra_filename_tags.get(num) or ""

		if len(extra_tag) > 0:
			print(f" ____________________________ HERUS: got extra tag = {extra_tag}")

		new_name = f"{file[:frame_num_end_idx]}__b{'0' * number_of_r}{extra_tag}{file[frame_num_end_idx:]}"

		old_filename = os.path.join(directory, file)
		new_filename = os.path.join(directory, new_name)

		os.rename(old_filename, new_filename)

		files_processed += 1
		print(f"Renamed {old_filename} to {new_filename}")

	print(f"\n\nDone. Processed {files_processed} files.\n\n")


rename_files_in_directory()
