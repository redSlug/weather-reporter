from PIL import Image
from sys import argv
im = Image.open(argv[1])
im.save(argv[2])