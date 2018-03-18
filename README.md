# iOS-Image-Resizer
Resizes images from a folder and creates 1x, 2x, and 3x versions.

[![Build Status](https://travis-ci.org/mattpaletta/iOS-Image-Resizer.svg?branch=master)](https://travis-ci.org/mattpaletta/iOS-Image-Resizer)

By [Matthew Paletta](http://mrated.ca).

**iOS Image Resizer** takes the images you've already created and lets you create the variety of sizes for importing into Xcode.

## Installation

First, ensure requirements are installed, and up-to-date
```console
pip install -r requirements.txt
```

## Usage
Images are loaded from the images/ folder.  If this directory does not exist, the program will will automatically create this folder and prompt the user to drag images into that folder before continuing.<br />
Images are processed and output into the output folder.<br />
The user will be asked to enter the width, height, and an overwrite option.<br />

WIDTH: determines the width for the 1x version of all photos (see exception below)<br />
HEIGHT (optional): if 0, the original aspect ratio is maintained for all images.  If there is some other positive number entered, this will be the height for all 1x output images.<br />
OVERWRITE: Flag used to indicate if an output images already exists, should the program replace it, or make a numbered version for the new file.<br />

- If the images are in subfolders, those subfolders are maintained.
- If the images are in subfolders that are an integer, that number is used as a width for all images within that subfolder.  This allows for more ease of batch processing images.

## Example
To run the program with the example images, run:
```console
python resizer.py
```
<br />
When prompted for the width, type: 32<br />
When prompted for the height, type: 0<br />
When prompted for the overwrite, type: y<br />
<br />
The system will process the example images.  Notice, in the "drawable-mdpi" folder, there is another folder "37".  All of the 1x images in the output folder will be 32x32, except for the image in the "drawable-mdpi" folder, which is "37x37" pixels.
<br />

## Information

The following image formats are supported:
- BMP
- AI
- EPS
- ICNS
- IM
- JPEG
- JPEG 2000
- MSP
- PCX
- PNG
- PPM
- WebP
- XBM

.AI files are automatically converted to PNG format, then resized.  This process uses ghostscript in the command line.  Tested on OSX only.

### Questions, Comments, Concerns, Queries, Qwibbles?

If you have any questions, comments, or concerns please leave them in the GitHub
Issues tracker:

https://github.com/mattpaletta/iOS-Image-Resizer/issues

### Bug reports

If you discover any bugs, feel free to create an issue on GitHub. Please add as much information as
possible to help us fixing the possible bug. We also encourage you to help even more by forking and
sending us a pull request.

https://github.com/mattpaletta/iOS-Image-Resizer/issues

## Maintainers

* Matthew Paletta (https://github.com/mattpaletta)

## License

MIT License. Copyright 2017 Matthew Paletta. http://techguyification.com
