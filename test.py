from resizer import Resizer
import unittest

class MyTest(unittest.TestCase):
	def test_basic(self):
		resizer = Resizer()
		resizer.process_images_in_dir(input_dir="images", width=32, height=32, overwrite=False)

	def test_overwrite(self):
		resizer = Resizer()
		resizer.process_images_in_dir(input_dir="images", width=32, height=32, overwrite=True)

	def test_invalid_dir(self):
		resizer = Resizer()
		with self.assertRaises(AssertionError) as context:
			resizer.process_images_in_dir(input_dir="does_not_exist", width=32, height=32, overwrite=True)

			self.assertTrue('Throws exception on invalid directory.' in context.exception)

	def test_invalid_width(self):
		resizer = Resizer()
		with self.assertRaises(AssertionError) as context:
			resizer.process_images_in_dir(input_dir="images", width=-1, height=32, overwrite=True)

			self.assertTrue('Throws exception on invalid width.' in context.exception)

	def test_invalid_height(self):
		resizer = Resizer()
		with self.assertRaises(AssertionError) as context:
			resizer.process_images_in_dir(input_dir="images", width=32, height=-1, overwrite=True)

			self.assertTrue('Throws exception on invalid width.' in context.exception)

if __name__ == "__main__":
	unittest.main()
