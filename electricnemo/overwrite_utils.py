from cymunk.cymunk import Circle, BoxShape, Poly, Segment

def replace_cymunk_physics_shapes(cymunk_physics_comp,args,space):

    """
    Given a cymunk physics body and an args dict, overwrite
    shape data while keeping body intact

    #TODO: If the new shape is the same type as the old shape, just replace the old 
    parameters. This should be slightly faster
    """

    body = cymunk_physics_comp.body
    old_shape_type = cymunk_physics_comp.shape_type #Type str (ie:'box')
    new_shape_type = args['main_shape']

    cymunk_physics_comp.shape_type = new_shape_type
    old_shapes = cymunk_physics_comp.shapes #List of cymunk.BoxShape or other objects

    for old_shape in old_shapes:
        #TODO, change params in old_shapes if shape_type matches with new shapes
        space.remove(old_shape)

    #Empty the shapes list. After the old shapes are removed the old addresses will be invalid
    cymunk_physics_comp.shapes = []
    
    for shape in args['col_shapes']:
	shape_info = shape['shape_info']
	if shape['shape_type'] == 'circle':
            new_shape = Circle(body, shape_info['outer_radius'],
                               shape_info['offset'])
        elif shape['shape_type'] == 'box':
            new_shape = BoxShape(body, shape_info['width'],
                                 shape_info['height'])
        elif shape['shape_type'] == 'poly':
            new_shape = Poly(body, shape_info['vertices'],
                             offset=shape_info['offset'])
        elif shape['shape_type'] == 'segment':
            new_shape = Segment(body, shape_info['a'], shape_info['b'],
                    shape_info['radius'])
        else:
            print 'shape not created'
        new_shape.friction = shape['friction']
        new_shape.elasticity = shape['elasticity']
        new_shape.collision_type = shape['collision_type']
        if 'group' in shape:
            new_shape.group = shape['group']
        cymunk_physics_comp.shapes.append(new_shape)
        space.add(new_shape)
        space.reindex_shape(new_shape)
     
    #body = cymunk_physics_comp.body
    #body.angle
    #body.angular_velocity 
    #body.angular_velocity_limit 'ang_vel_limit'
    #body.mass
    #body.movement
    #body.position
    #body.velocity
    #body.velocity_limit 'vel_limit'
    #body.moment 

'''
    
def replace_rotate_renderer(rotate_renderer_comp,rr_dict):
    rr = rotate_renderer_comp
    rr.texture_key = rr_dict['texture']
    rr.width,rr.height = rr_dict['size']
    rr.render = rr_dict['render']
'''
    

def replace_renderer(renderer_comp,
                     args,
                     texture_manager,
                     model_manager,
                     model_format = 'vertex_format_4f'):

    if 'texture' in args:
        texture_key = args['texture']
        texkey = texture_manager.get_texkey_from_name(texture_key)
        w, h = texture_manager.get_size(texkey)
    else:
        texture_key = str(None)
        texkey = -1
    if 'size' in args:
        w, h = args['size']
    copy = args.get('copy', False)
    copy_name = args.get('copy_name', None)
    render = args.get('render', True)
    model_key = args.get('model_key', None)
    model_manager = model_manager
    if model_key is None:
        if copy_name is None:
            copy_name = self.model_format + '_' + texture_key
        model_key = model_manager.load_textured_rectangle(
            model_format,
            w,
            h,
            texture_key,
            copy_name,
            do_copy=copy)
    elif model_key is not None and copy:
        model_key = model_manager.copy_model(model_key,
                                             model_name=copy_name)
                #model = model_manager._models[model_key]
                    
                    
    #r = renderer_comp
    #r.texture_key= renderer_dict['texture']
    #r.model_key = renderer_dict['model']

                    








    
"""
#If component is already present in target entity
#Clear the component, then init a new replacement component
# in its place
old_comp_idx = ent.get_component_index(ncomp)
#Component for this entity
ent_comp = csys.components[old_comp_idx]
print "New components",ncomp,new_args
print "Render id",ent_comp.entity_id,type(ent_comp.entity_id)
#print dir(ent_comp)

#ent.cymunk_physics.body.apply_impulse(100,100)
print dir(ent_comp)
ent_comp.texture_key = 'ring1'
#Other params are height,width,vertex_key,render,index_count,vertex_count
ent_comp.entity_id = -1
#Remove the old component
#csys.remove_component(old_comp_idx)

new_comp_idx = csys.create_component(ent_id,'general',new_args)
                        #print dir(ent.cymunk_physics)
                        #print dir(ent.cymunk_physics.body)
                        #print dir(ent.cymunk_physics.shapes[0])
                        #ent.cymunk_physics.shape_type = 'circle'
                        #cybod = cymunk.cymunk.Body(mass =200,moment=1)
                        #radius = 500
                        #offset = (0,0)
                        #ent.cymunk_physics.shapes[0] = cymunk.cymunk.Circle(cybod,radius,offset)
                        #print ent.cymunk_physics.shapes
                        #print ent.cymunk_physics.shape_type


                        #print ent.cymunk_physics.shapes
                            #Note. If an asteroid hits a powerup and gets the circle
                            #phys shape, then gets removed, the program will crash
                            #print "HERE"
                            pass
                            #new_args['position'] = old_comp.body.position
                            #new_args['velocity'] = old_comp.body.velocity
                            
                            #new_comp = csys.init_component(old_comp_idx,
                            #                               ent_id,
                            #                               zone='general',
                            #                               args=new_args)
                    #else:

                        #Note: Components should never be added dynamically. Only overwritten!
                        #If component is not already present, add it to entity
                        #print "Adding component",comp
                        #comp_idx = ent.get_component_index(comp)
                        #csys.init_component(comp_idx,ent_id,zone='general',args={comp:value})
                   #     print new_args
                   #     component_index = csys.create_component(ent_id,
                   #                                            zone='general',
                   #                                             args=new_args)



old_comp = phys_sys.components[old_comp_idx]
#Overwrite new_args positional parameters
new_args['position'] = (30,30)#old_comp.body.position
new_args['velocity'] = (30,30)#old_comp.body.velocity
new_args['entity_id'] = ent_id
#phys_sys.remove_component(old_comp_idx)
#Init replacement physics component
#phys_sys.init_component(old_comp_idx,
            #                        ent_id,
#                        zone='general',
#                        args=new_args)

circ_dict = {'inner_radius':0,
                         'outer_radius:':100,
'mass':20,
'offset':(10,10)}
print old_comp.shapes
print old_comp.shape_type
phys_sys.space.remove(old_comp.shapes[0])
new_shape = cymunk.cymunk.Circle(old_comp.body,200,(10,10))
phys_sys.space.add(new_shape)
old_comp.shapes[0] = new_shape



            shape.width= 0
            shape.height=0
            shape.mass=0
            shape.offset=(0,0)

            
            shape.inner_radius=0.
            shape.outer_radius=0.
            shape.mass=0.
            shape.offset=(0,0)

            shape.mass = 0
            shape.vertices = []
            shape.offset = (0,0)

            shape.mass = 0
            shape.a = (0,0)
            shape.b =(0,0)
            shape.radius = 0.


"""
