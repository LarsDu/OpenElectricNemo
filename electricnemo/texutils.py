

def main():
    test()
 

def get_tex_size(texture_manager,texkey,groupkey=0):
    tm = texture_manager
    ss_w,ss_h = tm.get_size(groupkey)
    uvs = tm.get_uvs(texkey)
    x= int(ss_w*uvs[0]) #lower left corner
    y= int(ss_h*uvs[1]) #lower left corner
    w = int(ss_w*uvs[2])-x
    h = y-int(ss_h*uvs[3])

    return w,h
    
def get_tex_region(texture_manager,tex_name,groupkey=0):
    tm = texture_manager
    spritesheet = tm.get_texture(groupkey)
    #spritesheet size
    ss_w,ss_h = tm.get_size(groupkey)
    texkey = tm.get_texkey_from_name(tex_name)
    
    uvs = tm.get_uvs(texkey)
    x= int(ss_w*uvs[0]) #lower left corner
    y= int(ss_h*uvs[1]) #lower left corner
    w = int(ss_w*uvs[2])-x
    h = y-int(ss_h*uvs[3])
    kivy_box =  (x,y,w,h)
    
    return spritesheet.get_region(*kivy_box)


def test():
    from kivent_core.managers.resource_managers import texture_manager
    tm = texture_manager
    v1 = tm.load_atlas('../res/img/spritesheet.atlas')
    v2 = tm.load_atlas('../res/img/textsheet.atlas')
    #print get_tex_region(tm,'jewel1',0)

    #print get_tex_region(tm,'let_A',0)
    print v1

if __name__ == "__main__":
    main()
