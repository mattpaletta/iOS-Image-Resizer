import os
import sys
from sys import version_info
import PIL
from PIL import Image


class Resizer(object):
	def get_user_input(self):

		print("\n\tiOS Image Resizer by Matthew Paletta\n")

		while not os.path.exists("images"):
			print("Creating images folder...")
			os.makedirs("images")
			_ = input(
					"It seems there was no images directory here.  We just created one for you!  Drag any images you "
					"would "
					"like to use in that folder, then press enter to continue.")

		# continue from while loop
		print("Input folder found")

		if not os.path.exists("output"):
			print("Creating output folder...")
			os.makedirs("output")

		print("Output folder found\n")

		# Are we in Python 2 or 3?
		if version_info[0] > 2:
			# print("Using Python 3.X")
			width = input("Please enter the desired width of the image(s) (in pixels) ")
			height = input(
					"Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in "
					"pixels) ")
			over = input("Should overwrite previous? [y/N] ")
			if over == 'y' or over == 'Y':
				overwrite = True
			else:
				overwrite = False
		else:
			# print("Using Python 2.X")
			width = raw_input("Please enter the desired width of the image(s) (in pixels) ")
			height = raw_input(
					"Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in "
					"pixels) ")
			over = raw_input("Should overwrite previous? [y/N] ")
			if over == 'y' or over == 'Y':
				overwrite = True
			else:
				overwrite = False

		self.process_images_in_dir("images", width, height, overwrite)
		print("\n")

	def process_images_in_dir(self, input_dir, width, height, overwrite):
		if not os.path.exists("output"):
			#print("Creating output folder...")
			os.makedirs("output")


		total = 0
		i = 0

		assert width > 0, "Width must be > 0"
		assert height > 0, "Height must be > 0"
		assert os.path.exists(input_dir), "Input directory does not exist."

		# Count the number of files first, so we can create a __progress bar.
		for root, subFolders, files in os.walk(input_dir):
			for _ in files:
				total += 1

		for root, subFolders, files in os.walk(input_dir):
			for file in files:
				self.__progress(i, total, "Reading: " + file)
				i += 1

				# Process PNG are easy
				if (file.endswith('.png') or file.endswith('.jpg')) \
						and not os.path.islink(os.path.join(root, file)):
					self.resize(root, file, int(width), int(height), overwrite)

				# Process .AI or .PSD, we have to convert to PNG first.
				elif (file.endswith('.ai') or file.endswith('.psd')) \
						and not os.path.islink(os.path.join(root, file)):
					self.__aiToPNG(root, file)
					filename = os.path.splitext(file)[0]
					self.resize(root, filename + ".png", int(width), int(height), overwrite)

					# Remove the temporary file afterwards.
					os.remove(os.path.join(root, filename + ".png"))

			if os.path.exists("log.txt"):
				os.remove("log.txt")
			self.__progress(total, total)

	def resize(self, root, file, width, height=0, overwrite=True):
		"""
		Resizes and saves an image in a variety of sizes (1x, 2x, 3x)

		:requires: `width > 0`.
		:requires: `width >= (width of the original image) / 3`.
		:requires: 'height >= 0'

		:param str root: The path to the folder
		:param str file: The input file, contained in the root folder
		:param int width: An optional parameter specifying the width of the output image
		:param int height: An optional parameter specifying the height of the image
		:returns: None
		"""

		filename = os.path.join(root, file)

		path = root.split('/')
		if len(path) > 1:  # contains a sub directory
			if self.__isInt(path[len(path) - 1]):
				width = int(path[len(path) - 1])  # set width to the name of the parent folder

		img = Image.open(filename)

		# Either use height passed in (if 0), or calculate proportional new height.
		wpercent = width / float(img.size[0])
		if height > 0:
			hsize = int(height / float(img.size[1]))
		else:
			hsize = int((float(img.size[1]) * float(wpercent)))

		# Iterate over the 3 output sizes we want to make
		# 1x, 2x, 3x
		for new_scale in range(1, 3 + 1):
			# Add the one, so height is never 0 on small images.
			img = img.resize((width * new_scale + 1, hsize * new_scale + 1), PIL.Image.ANTIALIAS)

			fileext = os.path.splitext(file)[1]
			filename = os.path.splitext(file)[0]

			path_has_subdirectory = len(path) > 1

			if path_has_subdirectory:  # was in a sub folder, write into same subfolder
				if not os.path.exists("output/" + self.__convertToString(path[1:], "/")):
					os.makedirs("output/" + self.__convertToString(path[1:], "/"))

				if new_scale == 1:
					output_file_name = self.__get_next_available_filename(parent_dir="output/",
					                                                      sub_dir=self.__convertToString(path[1:],
					                                                                                     "/"),
					                                                      filename=filename,
					                                                      file_ext=fileext,
					                                                      overwrite=overwrite)

					img.save(output_file_name)
				else:
					output_file_name = self.__get_next_available_filename(parent_dir="output/",
					                                                      sub_dir=self.__convertToString(path[1:],
					                                                                                     "/"),
					                                                      filename=filename,
					                                                      file_ext='@' + str(new_scale) + 'x' +
					                                                               fileext,
					                                                      overwrite=overwrite)
					img.save(output_file_name)
			else:
				if new_scale == 1:
					output_file_name = self.__get_next_available_filename(parent_dir="output/",
					                                                      sub_dir="",
					                                                      filename=filename,
					                                                      file_ext=fileext,
					                                                      overwrite=overwrite)

					img.save(output_file_name)

				else:
					output_file_name = self.__get_next_available_filename(parent_dir="output/",
					                                                      sub_dir="",
					                                                      filename=filename,
					                                                      file_ext='@' + str(new_scale) + 'x' +
					                                                               fileext,
					                                                      overwrite=overwrite)
					img.save(output_file_name)

	def __checkGhostScript(self):
		if os.system("which gs > /dev/null") != 0:
			print("Brewing Ghostscript...")
			os.system("brew install ghostscript > log.txt")

	def __aiToPNG(self, root, file):
		self.__checkGhostScript()
		filename = os.path.join(root, file)
		fileext = os.path.splitext(file)[1]
		fileN = os.path.splitext(file)[0]

		didRename = False

		if len(fileN.split(" ")) > 1:
			fileN = self.__convertToString(fileN.split(" "), "_")
			os.rename(os.path.join(root, file), os.path.join(root, fileN + fileext))
			didRename = True

		# print(filename, fileN, fileext)

		os.system("gs -dNOPAUSE -dBATCH -sDEVICE=pngalpha -r300 -sOutputFile=" +
		          os.path.join(root,
		                       fileN + ".png")
		          + " " + os.path.join(root, fileN + fileext) + "> log.txt")

		if didRename == True:  # if did rename, undo the actions
			fileN = self.__convertToString(fileN.split("_"), " ")
			os.rename(os.path.join(root, file), os.path.join(root, fileN + fileext))

	def __convertToString(self, a, s):
		return s.join(map(lambda c: str(c), a))  # map each character to a string

	def __isInt(self, s):
		try:
			int(s)
			return True
		except ValueError:
			return False

	def __progress(self, count, total, suffix=''):
		"""
		Updates the __progress bar in the terminal window
		
		:requires (count <= total)
		
		:param int count: The current index out of the total
		:param int total: The total number of items to process
		:param str suffix: An optional parameter specifying any text at the end of the output
		:return: None
		"""

		assert count <= total, "Count must be less than total."

		bar_len = 60
		filled_len = int(round(bar_len * count / float(total)))

		percents = round(100.0 * count / float(total), 1)
		bar = '=' * filled_len + '-' * (bar_len - filled_len)

		sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
		sys.stdout.flush()  # As suggested by Rom Ruben

	def __get_next_available_filename(self, parent_dir, sub_dir, filename, file_ext, overwrite):

		output_file_name = os.path.join(parent_dir, sub_dir, filename)
		add = ""

		while os.path.exists(output_file_name + str(add) + file_ext) and overwrite is False:
			if add == "":
				add = 1
			else:
				add += 1

		return output_file_name + str(add) + file_ext


if __name__ == "__main__":
	resize = Resizer()
	resize.get_user_input()
