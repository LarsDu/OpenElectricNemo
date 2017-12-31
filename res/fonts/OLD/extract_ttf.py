import string
from PIL import Image,ImageFont, ImageDraw

# use a truetype font
fsize=16
font = ImageFont.truetype("kongtext.ttf", fsize)
all_chars = string.printable

image = Image.new('RGBA',(fsize*len(all_chars),fsize))
draw = ImageDraw.Draw(image)

draw.text((0,0),string.printable , font=font)

image.show()
