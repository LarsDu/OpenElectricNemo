
import sys
import json
from PIL import Image
import os
def main(argv):
    """
    Kivy uses a bottem left corner (0,0) coordinate system I like
    to index my sprite sheets from the top left corner.  This script
    performs coordinate conversion

    Given a basename corresponding to a json and an image name (ie:
    'spritesheet.png' and spritesheet.json' have a basename
    'spritesheet').  Reverse the y coordinates of the json and create
    a copy with a '.atlas extension'
    """
    basename = os.path.splitext(argv[1])[0]
    imagef = basename+'.png'
    jsonf = basename+'.json'
    
    json_to_atlas(imagef,jsonf)
    
def json_to_atlas(imagef,jsonf):
    """
    Reverse y coordinate values in 
    """
    im = Image.open(imagef)
    _,h = im.size
    
    with open(jsonf,'r') as f:
        atdict = json.load(f)[imagef]
        fixed_atlas = reverse_y(h,atdict)

        atlas_fname = os.path.splitext(jsonf)[0]+'.atlas'
        with open(atlas_fname,'w') as af:
            jstr = json.dumps(fixed_atlas,separators=(',',':'),indent=4)
            af.write(jstr)
        
        
def reverse_y(h,atlas_dict):
    #print atlas_dict['aster1'][0]

    return { k:[v[0],h-v[1],v[2],v[3] ] for (k,v) in atlas_dict.items()}

if __name__ == "__main__":
    main(sys.argv)
