import cymunk

def overwrite_cymunk_body(cymunk_physics_comp,body_dict,pos):

    """
    Given a cymunk physics body and a body dict,
    overwrite the values in the the body dict
    """
    shape_type = cymunk_physics_comp.shape_type #Type str (ie:'box')
       
    shapes = cymunk_physics_comp.shapes #List of cymunk.BoxShape or other objects

    #Shapes list needs to be replaced

    #Replace shapes
    for shape in shapes:
        if shape_type == 'box':
            shape.width= 0
            shape.height=0
            shape.mass=0
            shape.offset=(0,0)
        elif shape_type == 'circle':
            shape.inner_radius=0.
            shape.outer_radius=0.
            shape.mass=0.
            shape.offset=(0,0)
        elif shape_type == 'poly':
            shape.mass = 0
            shape.vertices = []
            shape.offset = (0,0)
        elif shape_type == 'segment':
            shape.mass = 0
            shape.a = (0,0)
            shape.b =(0,0)
            shape.radius = 0.
    
    
    body = cymunk_physics_comp.body
    body.angle
    body.angular_velocity 
    body.angular_velocity_limit 'ang_vel_limit'
    body.mass
    body.movement
    body.position
    body.velocity
    body.velocity_limit 'vel_limit'
    body.moment 


    
def overwrite_rotate_renderer(rotate_renderer_comp,rr_dict):
    rr = rotate_renderer_comp
    rr.texture_key = rr_dict['texture']
    rr.width,rr.height = rr_dict['size']
    rr.render = rr_dict['render']

    

def overwrite_renderer(renderer_comp,renderer_dict):
    r = renderer_comp
    r.texture_key= renderer_dict['texture']
    r.model_key = renderer_dict['model']












    
'''
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

    
