from kivent_core.systems.staticmemgamesystem cimport (StaticMemGameSystem, 
    MemComponent)
#from kivent_core.systems.renderers cimport RenderComponent
#from kivent_core.systems.rotate_systems cimport RotateComponent2D, RotateSystem2D
#import rotate renderer component?

"""
Note: The SfxRenderer was patterned after rotate_systems.pyx
https://github.com/kivy/kivent/tree/master/modules/core/kivent_core/systems
"""

ctypedef struct SfxStruct2D:
    unsigned int entity_id
    float scale[2]
    float render_rotate
    unsigned char v_color[4]
    float x_trans
    float y_trans
    float x_shear
    float y_shear
    unsigned char  edge_effect_color[4]
    float edge_effect_thresh
    float sfx_flag



cdef class SfxComponent(MemComponent):
    pass


cdef class SfxSystem(StaticMemGameSystem):
    pass
