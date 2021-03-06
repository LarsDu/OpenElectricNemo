import params
import json
import pandas as pd
from pandas.io.json import json_normalize
def main():

    '''
    TODO:
    1. Refactor entity creation code
    2. Refactor entities to load from json
    3. Construct powerup scroll ent generator
    4. Construct and test powerup system
    5. Test out the shield system
    6. Implement the menu
    7. Implement the levelup system
    8. Implement enemy AI
    9. Fine tune
    10. Polish, polish, polish
    '''
    
    lib = EntityDump()
    fdump = 'entity_templates.json'
    jdict = lib.json_dump(fdump)

    print jdict

    '''
    df = pd.read_json(fdump)
    print df.info()
    print df.rocket1
    dfn = json_normalize(jdict)
    dfn.info()

    print dfn
    '''
class EntityDump(object):
    #Try to restructure game entities as json files
    #or even pandas dataframes
    
    def __init__(self):
        self.lib = {}


    def json_dump(self,json_fname):
        ship_dict,ship_init = EntityDump.create_player_ship()
        ship_dict['ship_init'] = ship_init

        shield_dict,shield_init = EntityDump.create_shield1()
        shield_dict['init_order'] = shield_init

        rocket_dict,rocket_init = EntityDump.create_rocket1()
        rocket_dict['init_order'] = rocket_init

        asteroid_dict,asteroid_init = EntityDump.create_asteroid1()
        asteroid_dict['init_order'] = asteroid_init

        
        uber_dict = { 'player_ship':ship_dict,
                      'shield1':shield_dict,
                      'rocket1':rocket_dict,
                      'asteroid1':asteroid_dict}
        with open(json_fname ,'w') as jf:
            json.dump(uber_dict,jf,sort_keys=True,indent=4,ensure_ascii=True)

        return uber_dict
        
        

    @classmethod
    def create_player_ship(cls):
        shape_dict = {
            'width':31.,
            'height':16.,
            'mass':1000000.,
            'offset':(7,1)
        }

        col_shape = {
            'shape_type': 'box',
            'elasticity': 1,
            'collision_type': 0,
            'shape_info': shape_dict,
            'friction': 1.0
        }

        rotate_render_dict = { 'texture':'ship1',
                               'size': (32, 32),
                               'render': True
        }

        pos = (0,0)
        
        physics_dict = {'main_shape':'box',
                        'position': pos,
                        'angle':0,
                        'velocity':(0,0),
                        'angular_velocity':0,
                        'vel_limit':500,
                        'ang_vel_limit': 0,
                        'mass': 100000,
                        'col_shapes':[col_shape]
        }

        weapon_dict = {'input_source':'player_control',
                       'xoff':0,
                       'yoff':0,
                       'projectile':'rocket1'}
        
        create_dict = {
            'player_control': {'state':'default'},
            'thruster_comp':{'up':(0,25),'down':(0,-25)},
            'rotate_renderer': rotate_render_dict,
            'rotate':0,
            'cymunk_physics':physics_dict,
            'pindown_comp':{'px':pos[0],'vx':5,'angle':0,'angular_velocity':0},
            'position': pos,
            'off_camera_comp':{'kill_off_camera':True},
            'text_comp': {'text':'Click!','xoff':0,'yoff':0},
            'acceleration':{'ax':0,'ay':0}, #-.8.5
            'health_comp': {'health': 10000},
            'damage_comp': {'damage': -10},
            'destruct_comp':{'explosion':'explode1',
                            'explosion_damage': 0,
                            'explosion_timer': 1},
            'weapon_comp': weapon_dict
            }
        
        init_order = ['player_control',
                      'thruster_comp',
                      'position',
                      'rotate',
                      'rotate_renderer',
                      'cymunk_physics',
                      'pindown_comp',
                      'acceleration',
                      'weapon_comp',
                      'text_comp',
                      'off_camera_comp',
                      'damage_comp',
                      'health_comp',
                      'destruct_comp']
        return create_dict,init_order

    
    @classmethod
    def create_rocket1(cls,xpos=0,ypos=0,xoff=0,yoff=0,collision_type=0):
        shape_dict = {
            'width':27.,
            'height':14.,
            'mass':20,
            'offset':(2,20)
        }

        col_shape = {
            'shape_type': 'box',
            'elasticity': .5,
            'collision_type': collision_type,
            'shape_info': shape_dict,
            'friction': 1.0
        }

        rotate_render_dict = { 'texture':'rocket1',
                               'size': (32,32),
                               'render': True
        }

        physics_dict = {'main_shape':'box',
                        'position': (xpos,ypos),
                        'angle':3.14,
                        'velocity':(400,0),
                        'angular_velocity':0,
                        'vel_limit':500,
                        'ang_vel_limit': 20,
                        'mass': 200,
                        'col_shapes':[col_shape]
        }

        create_dict = {'position': (xpos,ypos),
                       'rotate_renderer': rotate_render_dict,
                       'rotate': 0, 
                       'cymunk_physics': physics_dict,
                       'off_camera_comp':{'kill_off_camera':True},
                       'acceleration': {'ax':.25},
                       'health_comp': {'health': 10},
                       'damage_comp': {'damage': -25},
                       'destruct_comp':{ 'explosion':'explode1',
                                        'explosion_damage': 0,
                                        'explosion_timer': 1}
                       }

        
        init_order = ['position',
                      'rotate',
                      'rotate_renderer',
                      'cymunk_physics',
                      'off_camera_comp',
                      'acceleration',
                      'health_comp',
                      'damage_comp',
                      'destruct_comp'
         ]
        return create_dict,init_order

    @classmethod
    def create_shield1(cls,xpos=0,ypos=0,xoff=0,yoff=0,outer_radius=32,collision_type=0):

        shape_dict = {'inner_radius': 0, 'outer_radius': outer_radius,
                      'mass': 50, 'offset': (xoff, yoff)}

        col_shape = {'shape_type': 'circle', 'elasticity': 1,
                     'collision_type': collision_type, 'shape_info': shape_dict, 'friction': 1.0}

        rotate_render_dict = { 'texture':'shield1',
                               'size': (32, 32),
                           'render': True
        }
        
        physics_dict = {'main_shape':'circle',
                        'position': (xpos,ypos),
                        'angle':0,
                        'velocity':(0,0),
                        'angular_velocity':0,
                        'vel_limit':500,
                        'ang_vel_limit': 20,
                        'mass': 200,
                        'col_shapes':[col_shape]
        }

        create_dict = {'position': (xpos,ypos),
                       'rotate_renderer': rotate_render_dict,
                       'rotate': 0, 
                       'cymunk_physics': physics_dict,
                       'off_camera_comp':{'kill_off_camera':True},
                       'acceleration': {'ax':0,'ay':0},
                       'health_comp': {'health': 300},
                       'damage_comp': {'damage': -50},
        }

        
        init_order = ['position',
                      'rotate',
                      'rotate_renderer',
                      'cymunk_physics',
                      'off_camera_comp',
                      'acceleration',
                      'health_comp',
                      'damage_comp',
        ]

        return create_dict,init_order

    @classmethod 
    def create_asteroid1(cls,rand_texture='asteroid1',xpos=0,ypos=0,vx=0,vy=0,collision_type=0):
        rotate_render_dict = { 'texture':rand_texture,
                               'size': (32,32),
                               'render':True}
        
        #angle = radians(randint(-360, 360))
        #angular_velocity = radians(randint(-150, -150))
        shape_dict = {'inner_radius': 0, 'outer_radius': ((32-2)//2),
                      'mass': 50, 'offset': (0, 0)}
        col_shape = {'shape_type': 'circle', 'elasticity': 1,
                     'collision_type': collision_type,
                     'shape_info': shape_dict, 'friction': 1.0}

                
        physics_dict = { 'main_shape':'circle',
                         'position': (xpos,ypos),
                         'angle': 0,
                         'velocity': (vx,vy),
                         'angular_velocity':0,
                         'vel_limit':500,
                         'ang_vel_limit': 0,
                         'mass': 50,
                         'col_shapes':[col_shape]
        }

                
        create_dict = { 'cymunk_physics':physics_dict,
                        'rotate_renderer': rotate_render_dict,
                        'position': (xpos,ypos),
                        'rotate':0,
                        'off_camera_comp':{'kill_off_camera':True},
                        'health_comp': {'health': 100},
                        'damage_comp': {'damage': 10},
                        'destruct_comp':{'explosion':'explode1',
                                        'explosion_damage': 0,
                                        'explosion_timer': 1}
        }

        init_order = ['position',
                      'rotate',
                      'rotate_renderer',
                      'cymunk_physics',
                      'damage_comp',
                      'health_comp',
                      'destruct_comp',
                      'off_camera_comp']

        return create_dict,init_order
    
if __name__ == "__main__":
    main()
