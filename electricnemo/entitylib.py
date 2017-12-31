import json

def main():
    import pprint
    elib = EntityLib('entity_templates88.json',scale=4)
    cd, io = elib.get_template('rocket1',pos=(4,3))
    pprint.pprint( cd)
    pprint.pprint( io)

    
class EntityLib(object):
    """
    Converts json files containing entity templates to 

    Having a library of entities is useful for reuse of the same entities in 
    different systems.

    Resulting create_dict and init_order can be further modified or overridden in 
    game code for things like random damage.

    Height, width, size, physics vertex coordinates, and other attributes can also
    be rescaled from original templates
    """
    def __init__(self,json_fname,scale = 1):
        self.json_fname = json_fname
        self.scale = scale
        
        with open(self.json_fname,'r') as jf:
            self.entity_dict = json.load(jf,object_hook=_decode_dict)
        
        for create_dict in self.entity_dict.values():
            self.rescale(create_dict)
    def rescale(self,create_dict):
        if self.scale == 1:
            return

        scale = self.scale
        renderers = []

        for key in create_dict.keys():
            if key.endswith('renderer',0,-1): #equiv to 'renderer*'
                renderers.append(key)
        #Rescale physics bodies and textures
        
        for renderer in renderers:
            rsize = create_dict[renderer]['size']
            create_dict[renderer]['size'] = [dim*scale for dim in rsize]

        if 'cymunk_physics' in create_dict:
            col_shapes = create_dict['cymunk_physics']['col_shapes']
            for i in range(len(col_shapes)):
                shape = col_shapes[i]['shape_info']
                shape['offset'] = [dim*scale for dim in shape['offset']]
                if 'width' in shape and 'height' in shape:
                    shape['width'] *= scale
                    shape['height'] *= scale
                elif 'inner_radius' in shape and 'outer_radius' in shape:
                    shape['inner_radius'] *= scale
                    shape['outer_radius'] *= scale

                elif 'vertices' in shape:
                    verts = shape['vertices']
                    shape['vertices'] = [scale*vert for vert in verts]
                elif 'a' in shape and 'b' in shape and 'radius' in shape:
                    shape['a'] *= scale
                    shape['b'] *= scale
                    shape['radius'] *= scale

        
    def get_template(self, key, collision_type=0, pos=None, vel=None):
        #Get an entity create_dict 
        create_dict = self.entity_dict[key].copy()
        init_order = self.entity_dict[key]['init_order']
        #Remove init_order from dict (it's not a component!)
        del create_dict['init_order']
        assert set(create_dict.keys()) == set(init_order),\
            "init_order list does not match with create_dict keys"
        if collision_type is not None and 'cymunk_physics' in create_dict:
            for shape in create_dict['cymunk_physics']['col_shapes']:
                shape['collision_type'] = collision_type
        if pos is not None and 'cymunk_physics' in create_dict:
            create_dict['cymunk_physics']['position'] = pos
        if pos is not None and 'position' in create_dict:
            assert len(pos) == 2, "pos must have 2 values"
            create_dict['position'] = pos
        if vel is not None:
            assert len(vel) == 2, "vel must have 2 values"
            if 'movement' in create_dict and vel is not None:
                create_dict['movement']['vx'] = vel[0]
                create_dict['movement']['vy'] = vel[1]
            elif 'cymunk_physics' in create_dict:
                create_dict['cymunk_physics']['velocity'] = vel
                
        return create_dict,init_order


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

    
if __name__ == "__main__":
    main()

    
