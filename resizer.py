import fileinput
import os
from sys import version_info
import PIL
from PIL import Image

def resize(root, file, width, height):
    filename = os.path.join(root, file)
    img = Image.open(filename)
    wpercent = width / float(img.size[0])
    if height > 0:
        hsize = int(height / float(img.size[1]))
    else:
        hsize = int((float(img.size[1]) * float(wpercent)))
    for i in range(3):
        iteration = i+1
        img = img.resize((width * iteration, hsize * iteration), PIL.Image.ANTIALIAS)
        if iteration == 1:
            img.save('output/'+file)
        else:
            fileext = os.path.splitext(file)[len(os.path.splitext(file))-1]
            img.save('output/'+os.path.basename(file)+'@'+str(iteration)+'x'+fileext)

py3 = version_info[0] > 2
width = 0
height = 0

print("\n\tiOS Image Resizer by Matthew Paletta\n")

if py3:
    width = input("Please enter the desired width of the image(s) (in pixels)")
    height = input("Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in pixels)")
else:
    width = input("Please enter the desired width of the image(s) (in pixels)")
    height = input("Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in pixels)")



for root, subFolders, files in os.walk("images"):
    for file in files:
        print "Reading: "+file
        if (file.endswith('.png') or file.endswith('.jpg')) and os.path.islink(os.path.join(root, file)) == False:
            
            resize(root, file, int(width), int(height))
