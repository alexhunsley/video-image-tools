import os
import re
import sys
import math


def number_bin_digits_needed_to_express_num_values(num_values):
	if num_values == 1:
		return 1

	p = math.log(num_values - 1, 2) + 1

	# int is floor()
	req_digits = int(p)

	# print(f"num_values={num_values} p = {p} req_digits = {req_digits}")
	return req_digits


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
	files = [f for f in os.listdir(directory) if f.endswith(".jpg")]

	if len(files) == 0:
		print("Error: no matching files found, exiting.\n\n")
		sys.exit(1)
		
	first_and_last_images_num_digits = number_bin_digits_needed_to_express_num_values(len(files))

	# files = files.sort()
	files.sort()

	# Pattern to find first decimal number with "_" before it
	pattern = re.compile(r'[_-]\d+')

	# Find the position and length of the first number in the first file
	first_file = files[0]
	match = pattern.search(first_file)
	# print(f"first_file = {first_file} match = {match}")

	start, end = match.start() + 1, match.end()

	# special case for index 0!
	# t    
	for file in files:
		# Extract the decimal number from the filename
		num = int(file[start:end]) - first_input_image_index

		# print(f"num after -1 : {num}")

		# Calculate the number of trailing zeros in the binary representation
		if num == 0 or num == len(files) - 1:
			# Special case for image 0 since we need to represent all possible digits in the binary
			# version of file indexes being 0 (this allows any boo number search term to match first image).
			# We also do same treatment for last file too; we ensure both start end files have a 'boo' 
			# that is greater than any other. This allows searching for just first and last images in a video.
			# (Not so helpful for searching for only first and last images across multiple video thumbnails,
			# as videos are usually different lengths and so the boo number for one's video's start+end frame
			# won't usually be that of another)
			# TODO: also add __start and __end to filenames for first + last images, as a convenience, 
			# to aid seeing just first+last images across many video thumbs.
			number_of_r = first_and_last_images_num_digits
		else:
			number_of_r = count_trailing_zeros(num)

		# print(f"num: {num} trailing zeroes: {number_of_r}")

		# idx += 1
		# if idx == 5:
		# 	sys.exit(0)

		# Construct the new filename
		new_name = f"{file[:end]}__b{'0' * number_of_r}{file[end:]}"
		
		old_filename = os.path.join(directory, file)
		new_filename = os.path.join(directory, new_name)
		# print(f"Dry run: renaming {old_filename} {new_filename}")
		# print(f"Dry run: renaming {file} {new_name}")

		os.rename(old_filename, new_filename)


rename_files_in_directory()
