import string
from PIL import Image,ImageFont, ImageDraw
import sys

import os

def main(argv):
    # use a truetype font
    font_file = "../res/fonts/kongtext.ttf"
    save_dir = "../res/img/text"
    fsize=16

    all_chars = string.printable
    font = ImageFont.truetype(font_file, fsize)

    for char in all_chars:
        image = Image.new('RGBA',(fsize,fsize))
        draw = ImageDraw.Draw(image)
        draw.text((0,0),str(char),font=font)
        let_fname = save_dir+os.sep+'let_'+str(char)+'.png'
        
        image.save(let_fname)

if __name__ == "__main__":
    main(sys.argv)
