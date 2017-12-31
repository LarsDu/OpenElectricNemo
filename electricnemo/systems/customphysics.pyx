
class CustomCymunkPhysics(CymunkPhysics):
    def __init__(self,**kwargs):
        super(CustomCymunkPhysics,self).__init__(**kwargs)


    def update(self, dt):
        '''Handles update of the cymunk space and updates the component data
        for position and rotate components. '''

        self.space.step(dt)

        cdef void** component_data = <void**>(
            self.entity_components.memory_block.data)
        cdef unsigned int component_count = self.entity_components.count
        cdef unsigned int count = self.entity_components.memory_block.count
        cdef unsigned int i, real_index
        cdef PositionStruct2D* pos_comp
        cdef RotateStruct2D* rot_comp
        cdef PhysicsStruct* physics_comp
        cdef cpBody* body
        cdef cpVect p_position

        for i in range(count):
            real_index = i*component_count
            if component_data[real_index] == NULL:
                continue
            physics_comp = <PhysicsStruct*>component_data[real_index]
            pos_comp = <PositionStruct2D*>component_data[real_index+1]
            rot_comp = <RotateStruct2D*>component_data[real_index+2]
            body = physics_comp.body
            rot_comp.r = body.a
            p_position = body.p
            pos_comp.x = p_position.x
            pos_comp.y = p_position.y


Factory.register('CustomCymunkPhysics',cls=CustomCymunkPhysics)

