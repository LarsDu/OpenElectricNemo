#TODO:
#auto-rescale phys object sizes
#Implement enemy AI system
#Add front facing menu

import os
from os import sep
from os.path import dirname, join, abspath

import cymunk
#from cymunk import Vec2d

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint, choice

import kivent_core
import kivent_cymunk
from kivent_cymunk.physics import CymunkPhysics
from kivent_core.gameworld import GameWorld
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_core.systems.renderers import Renderer
from kivent_core.systems.gamesystem import GameSystem
from kivent_core.managers.resource_managers import texture_manager
import kivent_core.rendering.vertex_formats as vertex_formats
from kivy.properties import (NumericProperty, BooleanProperty, ObjectProperty,
                                 ListProperty, StringProperty)

from kivy.factory import Factory
import params

from math import radians, pi, sin, cos

import random
import texutils #Hacks for directly accessing texture regions
from entitylib import EntityLib
import overwrite_utils

from kivy.config import Config
from kivy.core.window import Window

""" Load custom Sfx renderer """
from nemo_sfx.sfx import SfxComponent,SfxSystem
from nemo_sfx.sfx_renderer import SfxRenderer

Config.set('graphics', 'width', str(params.screen_width))
Config.set('graphics', 'height', str(params.screen_height))
Config.set('graphics','resizable',False)




Window.size = (params.screen_width,params.screen_height)

atlas_dir = join(params.res_path,'img')
spritesheet_kdict = texture_manager.load_atlas(atlas_dir+os.sep+'spritesheet.atlas')
textsheet_kdict = texture_manager.load_atlas(atlas_dir+os.sep+'textsheet.atlas')



class ElectricNemo(Widget):
    def __init__(self, **kwargs):
        super(ElectricNemo, self).__init__(**kwargs)
        self.gameworld.init_gameworld([
            'position',
            'movement',
            'acceleration', 
            'rotate',
            'cymunk_physics',
            'rotate_renderer1',
            'rotate_renderer2',
            'rotate_renderer3',
            'bgstars',
            'asteroids',
            'rings',
            'jewels',
            'top_renderer1',
            'mid_renderer1',
            'bg_renderer1',
            'text_comp',
            'camera1',
            'health_comp',
            'damage_comp',
            'powerup_comp',
            'robo_ai_comp',
            'level_comp',
            'off_camera_comp',
            'thruster_comp',
            'weapon_comp',
            'destruct_comp',
            'shield_comp', 
            'player_control',
            'attach_to',
            'pindown_comp'
        ],
        callback=self.init_game)
        

        
    def init_game(self):
        self.setup_states()
        self.set_state()
        self.load_models()
        self.load_entitylib()
        self.register_collisions()
        self.create_bg()
        self.create_player_ship()


    def load_entitylib(self):
        self.entitylib = EntityLib('electricnemo'+sep+'entity_templates.json',scale=params.scale)
        #cd,io = self.entitylib.get_template('ring1')

    def register_collisions(self):
        """
        Enumerate the types of collisions 
        cymunk_physics will handle

        Then tie each type of collision to a 
        """
        physics_system = self.ids['cymunk_physics']

        #Each collision type is an integer
        #This integer corresponds to collision type in col_shape parameter for
        #begin_func is called whenever a particular collision pair occurs

        #Generate a collision type integer
        #General collision which gets solved and exchanges damage
        self.general_collision = physics_system.register_collision_type('general')
        game = self.gameworld.parent
        physics_system.add_collision_handler(
            self.general_collision,
            self.general_collision,
            separate_func=game.ids['damage_comp'].on_collision_separate_general)


        #Collision which doesn't get solved, but exchanges damage
        #The longer the colision, the more the damage

        self.laser_collision = physics_system.register_collision_type('laser')
        physics_system.add_collision_handler(
            self.general_collision,
            self.laser_collision,
            begin_func = game.ids['damage_comp'].on_collision_begin_laser,
            pre_solve_func=None,
            post_solve_func=None,
            separate_func=None)



        
        self.powerup_collision = physics_system.register_collision_type('powerup')

        physics_system.add_collision_handler(
            self.general_collision,
            self.powerup_collision,
            begin_func=game.ids['powerup_comp'].on_collision_powerup,
            pre_solve_func = game.ids['damage_comp'].on_collision_separate_general)



        self.collisions = {
            'general':self.general_collision,
            'laser':self.laser_collision,
            'powerup':self.powerup_collision
        }
        
    def no_collision(self,space,arbiter):
        return False
            

    def load_models(self):
        print "Vertex formats", id(vertex_formats)
        model_manager = self.gameworld.model_manager
        stdw = 32.*params.scale
        stdh = 32.*params.scale
        '''
        model_manager.load_textured_rectangle('vertex_format_4f', stdw, stdh,
                                                            'star1', 'star1a')

        
        model_manager.load_textured_rectangle('vertex_format_4f',
                                              stdw,
                                              stdh,
                                             'ship1','ship1_mod')

        model_manager.load_textured_rectangle( 'vertex_format_4f',
                                               stdw*2,
                                               stdw*2,
                                               'shield1','shield1a')
        '''                                
        #Get all text sprites
        
        model_manager.load_textured_rectangle('vertex_format_4f',
                                              params.screen_width,
                                              params.screen_height,
                                              'space1','space1_bg')

        
        for texname,texkey in spritesheet_kdict.items():
            w,h=texutils.get_tex_size(texture_manager,texkey,groupkey=0)
            
            width = w*params.scale
            height= h*params.scale
            #print texname,texkey,width,height
            #text_size = params.scale*params.text_size
            model_manager.load_textured_rectangle('vertex_format_4f',
                                                  width,
                                                  height,
                                                  texname,
                                                  texname+'_mod')
                                                  #do_copy=True)
            
        
        for key in textsheet_kdict.viewkeys():
            text_size = params.scale*params.text_size
            model_manager.load_textured_rectangle('vertex_format_4f',
                                                  text_size,
                                                  text_size,
                                                  key,
                                                  key+'_mod')
        
    def set_state(self):
        self.gameworld.state = 'main'

        
    def setup_states(self):
        #self.gameworld.add_state(
        #    state_name='main_menu',
        #    screenmanager_screen='main_menu'
        #)
        self.gameworld.add_state(
            state_name='main',
            systems_added=[
                'position',
                'rotate',
                'sfx',
                'rotate_renderer1',
                'rotate_renderer2',
                'bg_renderer1',
                'mid_renderer1',
                'top_renderer1',
             #              'camera1',
             #              'input',
             #              'player_control',
             #              'attach_to',
             #              'text_comp',
                           'off_camera_comp',
             #              'health_comp',
             #              'damage_comp',
             #              'powerup_comp',
             #              'robo_ai_comp',
                           'level_comp'],
            systems_removed=[], systems_paused=[],
            systems_unpaused=[
                'position',
                'rotate',
                'sfx',
                'movement',
                'acceleration',
                'bg_renderer1',
                'mid_renderer1',
                'rotate_renderer1',
                'rotate_renderer2',
                'camera1',
                'player_control',
                'attach_to',
                'text_comp',
                'off_camera_comp',
                'health_comp',
                'powerup_comp',
                'robo_ai_comp',
                'level_comp',
                'damage_comp',
                'thruster_comp',
                'weapon_comp',
                'shield_comp',
                'destruct_comp'],
            screenmanager_screen='main')
        

    def create_bg(self):
        bg_dict = {'position':(params.screen_width//2,params.screen_height//2),
                   'bg_renderer1':{'texture':'space1','model_key':'space1_bg'}}
        ent_id = self.gameworld.init_entity(bg_dict,['position','bg_renderer1'])



        
    def create_player_ship(self):

        shape_dict = {
            'width':31.*params.scale,
            'height':16.*params.scale,
            'mass':1000000.,
            'offset':(7,1)
        }

        col_shape = {
            'shape_type': 'box',
            'elasticity': 1,
            'collision_type': self.general_collision,
            'shape_info': shape_dict,
            'friction': 1.0
        }

        rotate_render_dict = { 'texture':'ship1',
                               'size': (32*params.scale, 32*params.scale),
                               'render': True,
                               'copy':True
                               
        }
        
        rotate_render_dict2 = { 'texture':"blank1",
                                'size': (1,1),
                                'render': False,
                                'copy':True
        }
        
        

        pos = (params.screen_width/3.5,params.screen_height//2)
        
        physics_dict = {'main_shape':'box',
                        'position': pos,
                        'angle':0,
                        'velocity':(0,0),
                        'angular_velocity':0,
                        'vel_limit':400,
                        'ang_vel_limit': 0,
                        'mass': 100000,
                        'col_shapes':[col_shape]
        }

        weapon_dict = {'input_source':'player_control',
                       'xoff':0,
                       'yoff':0,
                       'projectile':'rocket1'}
        
        ship_dict = {
            'player_control': {'state':'default','do_tap':False},
            'thruster_comp':{'up':(0,700),'down':(0,-100)},
            'rotate_renderer1': rotate_render_dict,
            'rotate_renderer2':rotate_render_dict2,
            'rotate':0,
            'cymunk_physics':physics_dict,
            'pindown_comp':{'px':pos[0],'vx':5,'angle':0,'angular_velocity':0},
            'position': pos,
            'off_camera_comp':{'kill_off_camera':True},
            'acceleration':{'ax':0,'ay':-5}, #-.8.5
            'health_comp': {'health': 300},
            'damage_comp': {'damage': -10},
            'destruct_comp':{'explosion':'explode1',
                             'explosion_damage': 0},
            'weapon_comp': weapon_dict
            }
        init_order = ['player_control',
                      'thruster_comp',
                      'position',
                      'rotate',
                      'rotate_renderer1',
                      'rotate_renderer2',
                      'cymunk_physics',
                      'pindown_comp',
                      'acceleration',
                      'weapon_comp',
                      'off_camera_comp',
                      'damage_comp',
                      'health_comp',
                      'destruct_comp']

        #assert sorted(ship_dict.keys()) == sorted(init_order),"Error in ship init order"
        #print ship_dict
        #print init_order

        ent_id = self.gameworld.init_entity(ship_dict,init_order )

        #Add to ship entity list so we can access it later in other systems
        game = self.gameworld.parent
        #game.ids['player_control'].player_entity_id = ent_id
        self.player_id = ent_id


class MainMenu(Widget):
    def __init__(self,**kwargs):
        super(MainMenu,self).__init__(**kwargs)
    def exit():
        sys.exit(0)


        
class DefaultGameSystem(GameSystem):
    """
    Loads default arguments when initializing any component for this 
    gamesystem.
    
    """	
	
    default_args = {}

    def __init__(self,**kwargs):
        super(DefaultGameSystem,self).__init__(**kwargs)

    def init_component(self, component_index, entity_id, zone, args):
        #Start with default arguments and replace entries with user defined args
        # on initialization (pre-filtering)
        combined_args = self.default_args.copy()
        combined_args.update(args)
        super(DefaultGameSystem,self).init_component(component_index,entity_id,zone,combined_args)
        self.create_sys_entity(component_index,entity_id,zone,args)
        
    def create_sys_entity(self,component_index,entity_id,zone,args):
        pass
        
Factory.register('DefaultGameSystem',cls=DefaultGameSystem)


class DebugPanel(Widget):
    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self,dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)


        
class ElectricNemoApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1.)
        #top = Widget(size=(params.screen_width,params.screen_height))
        #top.add_widget(MainMenu())





        
class SimpleMovementSystem2D(DefaultGameSystem):
    """
    Handles velocity for non-cymunk physics objects
    """
    
    term_vx = -700
    term_vy = -700

    default_args = {'vx':0,'vy':0}
    def update(self,dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None and hasattr(component,'vx'):
                entity_id = component.entity_id
                entity = entities[entity_id]
                if hasattr(entity,'position'):
                    if component.vx < self.term_vx:
                        component.vx = self.term_vx
                    if component.vy < self.term_vy:
                        component.vy = self.term_vy
                            #component.vx += component.ax
                            #component.vy += component.ay
                            #entity.position.x += (component.vx)*dt
                            #entity.position.y += (component.vy) *dt
                    entity.position.x += component.vx
                    entity.position.y += component.vy

    
Factory.register('SimpleMovementSystem2D',cls=SimpleMovementSystem2D)

class AccelerationSystem2D(DefaultGameSystem):
    """
    Applies acceleration 
    """
    term_vx= -700
    term_vy= -700

    default_args = {'ax': 0,
                    'ay': 0}
    
    def update(self,dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]
                #Apply acceleration to velocity system 2D if it is present
                if hasattr(entity,'movement'):
                    entity.movement.vx += component.ax
                    entity.movement.vy += component.ay
                #Apply acceleration to cymunk_physics if present
                elif hasattr(entity,'cymunk_physics'):
                    body = entity.cymunk_physics.body
                    body.velocity += (component.ax,component.ay)
                    
                    
    
Factory.register('AccelerationSystem2D',cls=AccelerationSystem2D)



#class ShipSystem(DefaultGameSystem):
#    def __init__(self,**kwargs):
#        super(ShipSystem,self).__init__(**kwargs)
#        pass
#Factory.register('ShipSystem',cls=ShipSystem)


#Note this may be better as a state
class DeathSystem(DefaultGameSystem):
    def __init__(self,**kwargs):
        super(DeathSystem,self).__init__(**kwargs)
        pass
Factory.register('DeathSystem',cls=DeathSystem)

class DestructSystem(DefaultGameSystem):
    '''
    Depends on HealthSystem
    When an entity with a destruction system and a health system reaches 0 health,
    Remove the entity, and replace it with an explosion entity that may cause damage
    

    Default component args:
         explosion_damage:
         explosion_timer: How many ticks the explosion entity lasts before disappearing

    
    '''
    default_args = { 'xoff':0,
                     'yoff':0,
                     'explosion': 'explode1',
                     'explosion_damage': 0,
                   }

    
    def __init__(self,**kwargs):
        super(DestructSystem,self).__init__(**kwargs)
        self.explosions = {
                'impact_vel': 0,
                'explode1':self.create_explode1,
                'spark1':self.create_spark1
        }
        
        
    def update(self,dt):
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                if hasattr(entity,'health_comp'):
                    if entity.health_comp.health <= 0:
                        collision_type = self.gameworld.parent.laser_collision
                        create_explosion = self.explosions[component.explosion]
                        pos = (entity.position.x, entity.position.y)
                        if hasattr(entity,'movement'):
                            vel = entity.movement.vx,entity.movement.vy
                        elif hasattr(entity,'cymunk_physics'):
                            #vel = entity.cymunk_physics.body.velocity
                            vel = (0,0)
                            collision_type = self.gameworld.parent.laser_collision
                            explode_dict, init_order = create_explosion( pos,
                                                                     vel,
                                                                     component.explosion_damage,
                                                                     collision_type)
                            
                        explode_ent = self.gameworld.init_entity(explode_dict,init_order)
                        self.gameworld.remove_entity(entity_id)





                        
    def create_explode1(self,pos,vel,damage,collision_type):
        elib = self.gameworld.parent.entitylib
        create_dict, init_order = elib.get_template('boom1',
                                                    collision_type,
                                                    pos=pos,
                                                    vel=vel)

        #Apply custom damage
        if 'damage_comp' in create_dict:
            create_dict['damage_comp']['damage'] = damage
        return create_dict,init_order


    def create_spark1(self,pos,vel,damage,collision_type):
        elib = self.gameworld.parent.entitylib
        create_dict, init_order = elib.get_template('spark1',
                                                    collision_type,
                                                    pos=pos,
                                                    vel=vel)
        #Apply custom damage
        if 'damage_comp' in create_dict:
            create_dict['damage_comp']['damage'] = damage
        return create_dict,init_order

    
Factory.register('DestructSystem',cls=DestructSystem)



class AttachSystem(DefaultGameSystem):
    """
    An attach entity will hook up two entities to each other
    Each attach entity has an a parent and child entity

    The child's position is always relative to the parent
    https://gamedev.stackexchange.com/questions/31888
    """
    default_args = {'parent_id':None}

    def update(self,dt):
        for component in self.components:
            if component is not None:
                aentity_id = component.entity_id
                attach_ent = self.gameworld.entities[aentity_id]
                parent_ent = self.gameworld.entities[component.parent_id]
                if parent_ent.load_order != []:
                    if (component.lifespan is not None) and (component.lifespan > 0):
                        component.lifespan -= 1
                
                        if (parent_ent.position is not None
                            and attach_ent.position is not None
                            and component.lifespan > 0) :
                            attach_ent.position.x = parent_ent.position.x+component.xoff
                            attach_ent.position.y = parent_ent.position.y+component.yoff
    
Factory.register('AttachSystem',cls=AttachSystem)


class TextSystem(DefaultGameSystem):
    """
    Create text entities with position and movement components
    """
    text = ''
    xoff = 0
    yoff = 0
    spacing = params.scale*params.text_size-3
    renderer = 'mid_renderer1'
    longevity = 300
    
    def __init__(self,**kwargs):
        super(TextSystem,self).__init__(**kwargs)

    #def update(self,dt):
    #    for component in self.components:
    #        if component is not None:
    #            entity_id = component.entity_id
    #            entity = self.gameworld.entities[entity_id]
    #            pos = entity.position

    #def on_touch_down(self,touch):
        
    #    self.create_chars()
        #component = self.components[0]
        #entity = self.gameworld.entities[component.entity_id]
        #for component in self.components:
        #    print component.text
        #self.create_chars()
        #print self.gameworld.ids
        pass
        
            
    def create_chars(self):
        """
        Create letter entities to display text at a given position
        """
        init_entity = self.gameworld.init_entity
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                comp_text = component.text
                for i in xrange(len(comp_text)):
                    char = component.text[i]
                    if char == ' ':
                        continue
                    if hasattr(entity,'position'):
                        xorg = entity.position.x
                        yorg = entity.position.y
                    else:
                        xorg = 0
                        yorg = 0
                    let_xoff = component.xoff + i*TextSystem.spacing
                    let_yoff = component.yoff
                    x = xorg + let_xoff
                    y = yorg + let_yoff
                    let_key = 'let_'+ char

                    #player_control_comp = self.gameworld.parent.ids['player_control']
                    game = self.gameworld.parent
                    create_dict = {'movement': {'vx':0,
                                                'vy':0},
                                   'position':(x,y),
                                    self.renderer: {'texture':let_key,
                                                     'model_key':let_key+'_mod'},
                                   'off_camera_comp':{'kill_off_camera':True},
                                   'attach_to': {'parent_id':game.player_id,
                                                 'lifespan':25,
                                                 'xoff':let_xoff,
                                                 'yoff':let_yoff}
                                   
                    }
                    ent = init_entity(create_dict,
                                      ['position',
                                       'movement',
                                       'attach_to',
                                       'off_camera_comp',
                                       self.renderer] )
                    
Factory.register('TextSystem',cls=TextSystem)




                    



class OffCameraSystem(DefaultGameSystem):
    """
    Does stuff when an object moves off camera
    One option (kill_off_camera) will delete entities which move off camera
    """
    
    gameview = 'camera1'
    #kill_off_camera = True
    #def __init__(self,**kwargs):
    #    super(OffScreenSystem,self).__init__(**kwargs)
    #    pass

    def update(self,dt):
        gview = self.gameworld.system_manager[self.gameview]
        #Lower left corner
        view_xmin =  -gview.camera_pos[0]
        view_ymin =  -gview.camera_pos[1]
        view_xmax = view_xmin + gview.size[0]
        view_ymax = view_ymin + gview.size[1]
        for component in self.components:
            if component is not None and component.kill_off_camera == True:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                
                if hasattr(entity,'position'):
                    pos = entity.position
                    if (pos.x < view_xmin - 64 or
                        pos.x > view_xmax + 256 or
                        pos.y > view_ymax + 256 or
                        pos.y < view_ymin - 64):
                        self.gameworld.remove_entity(entity_id)
                        
Factory.register('OffCameraSystem',cls=OffCameraSystem)




class HealthSystem(DefaultGameSystem):
    #Offset from x,y (lower left corner) of entity with
    #this shield system
    
    xoff = 0
    yoff = 0 

    default_args = {'health':100}
        
    def __init__(self,**kwargs):
        super(HealthSystem,self).__init__(**kwargs)

        
    '''
    def update(self,dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]
                if hasattr(entity,'position'):
                    pass
    '''
                
Factory.register('HealthSystem',cls=HealthSystem)



class PowerUpSystem(DefaultGameSystem):
    '''
    A powerup component contains data on new component parameters
	An entity with a powerup collision type and a powerup component 
	will transfer its component data to a target entity on collision.
	
	If the target entity has the components described in the 'new_comps'
	dict, these components will have their data overwritten. 
	
	
    
    Note that certain powerups such as health boosting powerups
    don't require this component as such powerups can have qualities
    like positive damage which adds health to the health bar of the target.

    This system adds or overrides components upon collision, and takes care
    of some of the associated SFX.

    powerup_dict is a create_dict for a component that will be created for whatever entity
    collides or triggers the powerup

    '''
    default_args = { 'new_comps':{} }


    def __init__(self,**kwargs):
        super(PowerUpSystem,self).__init__(**kwargs)
        #List of components to remove on each update

        self._phys_replace_stack = []


        
    def on_collision_powerup(self,space,arbiter):
        ent_id = arbiter.shapes[0].body.data
        powerup_id = arbiter.shapes[1].body.data
        #ent = self.gameworld.entities[gen_id]

        #print "Collision between",id1,id2
        self.apply_powerup(ent_id,powerup_id)
        return True

    def update(self,dt):
        self.replace_target_physics()


    def replace_target_physics(self):
        """
        Handle replacement of physics shapes
        
        Note: Removing and initializing components doesnt 
        seem to work for cymunk physics objects
        """
        
        game = self.gameworld.parent
        phys_sys = game.ids['cymunk_physics']
        while self._phys_replace_stack:
            #Pop off physics elements to be replaced
            old_comp_idx,ent_id,new_args = self._phys_replace_stack.pop()
            old_comp = phys_sys.components[old_comp_idx]
            if old_comp is not None:
                overwrite_utils.replace_cymunk_physics_shapes(old_comp,new_args,phys_sys.space)
             

    
    def apply_powerup(self,ent_id,powerup_id):
        ent = self.gameworld.entities[ent_id]
        powerup_ent = self.gameworld.entities[powerup_id]
        if hasattr(powerup_ent,'powerup_comp'):
            new_comps = powerup_ent.powerup_comp.new_comps

            if new_comps is not None and new_comps != {}:
                game = self.gameworld.parent

                for ncomp,new_args in new_comps.viewitems():

                    if hasattr(ent,ncomp):
                        """Replace an existing physics component"""
                        old_comp_idx = ent.get_component_index(ncomp)
                        if ncomp == 'cymunk_physics':
                            #Overwrite cymunk physics component
                            phys_sys = game.ids['cymunk_physics']
                            self._phys_replace_stack.append((old_comp_idx,ent_id,new_args))

                        if ncomp.endswith('renderer',-9,-1) or ncomp.endswith('renderer'):

                            """
                            Note: Overwriting exiting renderer component
                            models only works properly if new_args['copy'] 
                            is set to True. This may lead to memory 
                            overflow if too many power renderer components 
                            get new models initialized.

                            In the future, write a queue to track newly created models
                            and remove models from this queue if the queue grows too large
                            """
                        #if ncomp.endswith('rotate_renderer',-16,-1):
			    rsys = game.ids[ncomp]
                            old_comp = rsys.components[old_comp_idx]
                            new_model_key = new_args['texture']+'_mod'
                            old_comp.model = new_model_key
                            size = new_args['size']
                            old_comp.width = size[0]*params.scale
                            old_comp.height = size[1]*params.scale
                            old_comp.texture_key = new_args['texture']
                            old_comp.render = new_args['render']
                            

                            '''
                            model_manager = self.gameworld.model_manager
                            model_manager.register_entity_with_model(ent_id,
                            rsys.system_id,
                            new_model_key )
                            '''


Factory.register('PowerUpSystem',cls=PowerUpSystem)



class PlayerControlSystem(DefaultGameSystem):

    '''
    An input system listens for commands from a 
    PlayerControl System or an AiSystem

    It then relays these commands to a Thruster system
    or some other movement control type system.
    '''
    touch_down_state = 'up'

    default_args = {'weapon_key': 'weapon_comp',
                    'thruster_key':'thruster_comp',
                    'state': 'default',
                    'fire_weapon':False,


    }
    
    def __init__(self,**kwargs):
        super(PlayerControlSystem,self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
                
    '''
    def update(self,dt):
        for component in self.components:
            if component is not None:
                print component.state,component.prev_state
    '''

    def thrust(self,component):
        game = self.gameworld.parent
        ent_id = component.entity_id
        thruster_key = component.thruster_key
        thruster_sys = game.ids.get(thruster_key,game.ids['thruster_comp'])
        if component.state !='stop':
            thruster_sys.apply_delta_v(component)
        else:
            thruster_sys.stop(component)


    def fire_weapon(self,component):
        game = self.gameworld.parent
        ent_id = component.entity_id
        weapon_key = component.weapon_key
        weapon_sys = game.ids.get(weapon_key,game.ids['weapon_comp'])
        weapon_sys.fire_weapon(component)

 
    def on_touch_down(self,touch):
        """
        On touch down, change the state,
        and tell the thruster system to apply delta_v to the current entity
        """
        for component in self.components:
            if component is not None:
                component.state = self.touch_down_state
                self.thrust(component)
        
        
    def on_touch_up(self,touch):
        for component in self.components:
            if component is not None:
                component.state = 'default'
                self.thrust(component)
               
                
                
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

        
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #print "Key down",keycode
        for component in self.components:
            if component is not None:

                if keycode[1] == 'w':
                    component.state = 'up'
                    self.thrust(component)
                if keycode[1] == 's':
                    component.state = 'down'
                    self.thrust(component)
                if keycode[1] == 'up':
                    component.state = 'up'
                    self.thrust(component)
                if keycode[1] == 'down':
                    component.state = 'down'
                    self.thrust(component)
                                
                
                
                if keycode[1] == 'spacebar':
                    #print "Fire weapon"
                    component.fire_weapon = True
                    self.fire_weapon(component)
        return True
        
    def _on_keyboard_up(self,keyboard,keycode):
        #print "Key up",keycode
        for component in self.components:
            if component is not None:
                component.state = 'default'
                #self.thrust(component)
                component.fire_weapon = False
        return True


    
Factory.register('PlayerControlSystem',cls=PlayerControlSystem)                








class DamageSystem(DefaultGameSystem):
    #Note, an entity with negative damage will actually
    #Give health
    
    default_args = {'damage':0}
    def __init__(self,**kwargs):
        super(DamageSystem,self).__init__(**kwargs)

    def apply_damage(self,damage_entity,target_entity):
        if (hasattr(damage_entity,'damage_comp') and
            hasattr(target_entity,'health_comp') ):
            target_health = target_entity.health_comp.health
            damage = damage_entity.damage_comp.damage
            target_entity.health_comp.health = max(target_health+damage, 0)
            #print "Entity {} target_health {}".format(target_entity.entity_id,
            #                                          target_entity.health_comp.health)
             
        #else:
        #    print "Has damage",hasattr(damage_entity,'damage_comp')
    def on_collision_damage(self,space,arbiter):
        id1 = arbiter.shapes[0].body.data
        id2 = arbiter.shapes[1].body.data
        entity1 = self.gameworld.entities[id1]
        entity2 = self.gameworld.entities[id2]

        #print "Collision between",id1,id2
        self.apply_damage(entity1,entity2)
        self.apply_damage(entity2,entity1)
        

    def on_collision_separate_general(self,space,arbiter):
        self.on_collision_damage(space,arbiter)
        #Solve the collision
        return True

    def on_collision_begin_laser(self,space,arbiter):
        self.on_collision_damage(space,arbiter)
        #print "Applying laser damage"
        id1 = arbiter.shapes[0].body.data
        id2 = arbiter.shapes[1].body.data
        #print id1,id2
        #Don't solve the collision. Apply damage
        return False
    
Factory.register('DamageSystem',cls=DamageSystem)



class PinDownSystem(DefaultGameSystem):
    """
    Depends on cymunk physics
    
    Pins cymunk physics objects to have a fixed position, 
    angle, or velocity regardless of impacts
    """
    default_args = {'px':None,
                    'py':None,
                    'vx':None,
                    'vy':None,
                    'angle':None,
                    'angular_velocity':None
                    }
    
    def __init__(self,**kwargs):
        super(PinDownSystem,self).__init__(**kwargs)

    def update(self, dt):
        for component in self.components:
            if component is not None:
                
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                if hasattr(entity,'cymunk_physics'):
                    body = entity.cymunk_physics.body
                    new_pos = [body.position.x,body.position.y]
                    if component.px is not None:
                        new_pos[0] = component.px
                    if component.py is not None:
                        new_pos[1] = component.py
                    body.position = new_pos
                    #Need to replace body.position with list for some reason.
                    #Can't do body.position[0] = 233
                    if component.vx is not None:
                        body.velocity[0] = component.vx
                    if component.vy is not None:
                        body.velocity[1] = component.vy
                    if component.angle is not None:
                        body.angle = component.angle
                    if component.angular_velocity is not None:
                        body.angular_velocity = component.angular_velocity
                        
Factory.register('PinDownSystem',cls=PinDownSystem)



class ThrusterSystem(DefaultGameSystem):
    """
    A thruster component changes velocity (for both SimpleMovement and
    CymunkPhysics components) 

    Link a control system (player_control or ai_control) to this system
    and the control system will be able to change the Thruster systems velocity
    in the x and y directions
    
    """
    default_args = {'default':(0,0),
                    'stop':(0,0),
                    'up':(0,0),
                    'down':(0,0),
                    'left':(0,0),
                    'right':(0,0),
                    'do_tap':True,
    }

    def __init__(self,**kwargs):
        super(ThrusterSystem,self).__init__(**kwargs)
        
        
    def set_vel(self,control_component):
        """
        The input source will call this function
        """
        ent_id = control_component.entity_id
        state = control_component.state
        entity = self.gameworld.entities[ent_id]
        if hasattr(entity,self.system_id):
            ent_thruster = getattr(entity,self.system_id)
            delta_v = ent_thruster.__dict__.get(state,(0,0))
            if hasattr(entity,'cymunk_physics'):
                body = entity.cymunk_physics.body
                body.velocity = delta_v
            elif hasattr(entity,'movement'):
                movement.vx = delta_v[0]
                movement.vy = delta_v[1]

    def apply_delta_v(self,control_component):
        """
        The input source will call this function
        """
        ent_id = control_component.entity_id
        state = control_component.state
        entity = self.gameworld.entities[ent_id]
        if hasattr(entity,self.system_id):
            ent_thruster = getattr(entity,self.system_id)
            delta_v = ent_thruster.__dict__.get(state,(0,0))
            if hasattr(entity,'cymunk_physics'):
                body = entity.cymunk_physics.body
                body.velocity += delta_v
            elif hasattr(entity,'movement'):
                movement.vx += delta_v[0]
                movement.vy += delta_v[1]

                

    def stop(self,control_component):
        """
        The input source will call this function
        """
        ent_id = control_component.entity_id
        state = control_component.state
        entity = self.gameworld.entities[ent_id]
        if hasattr(entity,self.system_id):
            ent_thruster = getattr(entity,self.system_id)
            if hasattr(entity,'cymunk_physics'):
                body = entity.cymunk_physics.body
                body.velocity =(0,0)
            elif hasattr(entity,'movement'):
                movement.vx = 0
                movement.vy = 0

                
    def listen_input_state(self):
        """
        DEPRECATED
        Changes velocity by listening for changes in input state
        """
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                #Keep the player ship x position from changing on impacts
                if hasattr(entity,component.input_source) and hasattr(entity,'cymunk_physics'):
                    input_source = getattr(entity,component.input_source)

                    #Have read the curent keydown input.
                    #Set this to false to prevent multiple reads of the same key

                    body = entity.cymunk_physics.body
                    input_state = input_source.state
                    #prev_input_state = input_source.prev_state
                    #For the current input state, lookup component dict to get
                    #The change in velocity associated with that state
                    delta_v = component.__dict__[input_state]
                    body.velocity += delta_v

Factory.register('ThrusterSystem',cls=ThrusterSystem)



class ScrollEntGenSystem(DefaultGameSystem):
    renderer = 'bg_renderer1'
    gameview = 'camera1'
    models = ListProperty([('star1','star1a'),
                           ('star2','star2a'),
                           ('star3','star3a'),
                           ('star4','star4a')])

    gen_freq = 10
    gen_countdown = int(gen_freq)
    key = StringProperty(['asteroid1'])
    vx_range = ListProperty([-200,150])
    vy_range = ListProperty([0,0])
    ax_range = ListProperty([0,0])
    ay_range = ListProperty([0,0])
    collision_type = StringProperty('general')

    has_physics = False
    
    def update(self,dt):
        init_entity = self.gameworld.init_entity
        
        self.gen_countdown -= 1
        
        if self.gen_countdown <= 0:
            #After each countdown, make a new scrolling entity
            self.gen_countdown = self.gen_freq
            pos = (params.screen_width+64,randint(0,params.screen_height))
            rand_texture,rand_model_key = choice(self.models)


            if self.has_physics:
                pos = ( params.screen_width, randint(0,params.screen_height))
                vel = (randint(*self.vx_range),  randint(*self.vy_range))
                collision_type = self.gameworld.parent.collisions[self.collision_type]
                create_dict,init_order = self.create_bg_phys_ent( self.key,
                                                                  pos,
                                                                  vel,
                                                                  collision_type = collision_type,
                                                                  texture=rand_texture)
                init_entity(create_dict,init_order)
            else:
                render_dict =  { 'texture':rand_texture,
                                 'model_key':rand_model_key}
                create_dict = {
                    'position': pos,
                    'movement': {'vx':randint(*self.vx_range),
                                 'vy':randint(*self.vy_range)},
                    self.renderer: render_dict,
                    'off_camera_comp': {'kill_off_camera':True}
                }

                init_entity(create_dict,['position',
                                         'movement',
                                         self.renderer,
                                         'off_camera_comp'] )


    
    def create_bg_phys_ent(self,  entkey, pos, vel, collision_type, texture='asteroid1'):
        elib = self.gameworld.parent.entitylib
        create_dict, init_order = elib.get_template(entkey,
                                                    collision_type,
                                                    pos=pos,
                                                    vel=vel)
        if 'rotate_renderer1' in create_dict:
            create_dict['rotate_renderer1']['texture'] = texture
        return create_dict, init_order
                

Factory.register('ScrollEntGenSystem',cls=ScrollEntGenSystem)





class WeaponSystem(DefaultGameSystem):
    """
    Data: 
        - offsets from parent entity position for generating projectiles
        - num_projectile for this  

    """
    default_args = {'input_source':'player_control',
                    'xoff':0,
                    'yoff':0,
                    'projectile':'rocket1'}

    def __init__(self,**kwargs):
        super(WeaponSystem,self).__init__(**kwargs)
        self.projectiles = {
            'rocket1': self.create_rocket1_dict,
#            'laser1': self.create_laser1_dict
        }



    def create_rocket1_dict(self,xpos,ypos,collision_type=0):
        elib = self.gameworld.parent.entitylib
        create_dict,init_order = elib.get_template( 'rocket1',
                                                    pos=(xpos,ypos),
                                                    vel=None,
                                                    collision_type=collision_type)
        return create_dict, init_order
  
    


    def fire_weapon(self,control_comp):
        entity = self.gameworld.entities[control_comp.entity_id]

        if hasattr(entity,'position') and hasattr(entity,self.system_id):
            weapon_comp = getattr(entity,self.system_id)
            projectile_method = self.projectiles[weapon_comp.projectile]
            if hasattr(entity,'cymunk_physics'):
                if entity.cymunk_physics.shape_type == 'box':
                    box_info = entity.cymunk_physics.shapes[0]
                    weap_xpos = entity.position.x+box_info.width+weapon_comp.xoff
                    weap_ypos = entity.position.y+weapon_comp.yoff
                elif entity.cymunk_physics.shape_type == 'circle':
                    circ_info = entity.cymunk_physics.shapes[0]
                    weap_xpos = entity.position.x+circ_info.radius*2+weapon_comp.xoff
                    weap_ypos = entity.position.y+weapon_comp.yoff

            else:
                weap_xpos = entity.position.x+weapon_comp.xoff
                weap_ypos = entity.position.y

            collision_type = self.gameworld.parent.general_collision
            projectile_dict,init_order = projectile_method(weap_xpos,
                                                           weap_ypos,
                                                           collision_type)
            #Create the projectile entity
            projectile_ent = self.gameworld.init_entity(projectile_dict,init_order)
       
        
    """
    def update(self,dt):
       
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]
                
                if hasattr(entity,'position') and hasattr(entity,component.input_source):
                    input_source = getattr(entity,component.input_source)
                    fire_weapon = input_source.fire_weapon
                
                    if fire_weapon and not input_source.prev_fire_weapon:
                        projectile_method = self.projectiles[component.projectile]
                        weap_xpos = entity.position.x+60
                        print "Reminder: adapt weapon offset to parent body"
                        weap_ypos = entity.position.y
                        collision_type = self.gameworld.parent.general_collision
                        projectile_dict,init_order = projectile_method(weap_xpos,
                                                                       weap_ypos,
                                                                       collision_type)
                        #print "Fire away",entity_id
                                                
                        #Create the projectile entity
                        projectile_ent = self.gameworld.init_entity(projectile_dict,init_order)
                        '''
                        input_source.prev_fire_weapon = True
                    elif not fire_weapon and input_source.prev_fire_weapon:
                        input_source.prev_fire_weapon = False
                        '''

                        """
Factory.register('WeaponSystem',cls=WeaponSystem)




class RoboAiSystem(DefaultGameSystem):
    default_args = {'target_id': None}
    def __init__(self,**kwargs):
        super(RoboAiSystem,self).__init__(**kwargs)

Factory.register('RoboAiSystem',cls=RoboAiSystem)





class ShieldSystem(DefaultGameSystem):
    default_args = { 
                     'shield_type':'shield1',
                     'xoff':-16,
                     'yoff':-16,
    }
    
    def __init__(self,**kwargs):
        super(ShieldSystem,self).__init__(**kwargs)
        self.shields = {
            'shield1': self.create_shield1}
        
    def create_sys_entity(self,component_index,entity_id,zone,args):
        
        """ 
        Every times shield component is created, a shield entity is created as well
        #Note: Deprecated
        """
        pass
        '''
        parent_ent = self.gameworld.entities[entity_id]
        component = self.components[component_index]
        if (component is not None and hasattr(parent_ent,'position')
           and hasattr(parent_ent,'health_comp')):
            #Create shield
            vel = parent_ent.velocity
            xoff = component.xoff
            yoff = component.yoff
            pos = (parent_ent.position.x+xoff,parent_ent.position.y+yoff)
            outer_radius =component.outer_radius
            collision_type = self.gameworld.parent.general_collision
            #Ex: ShieldSystem.create_shield1()
            shield_dict,init_order = self.shields[component.shield_type](
                collision_type,
                pos,
                vel
            )
            
            shield_ent_id = self.gameworld.init_entity(shield_dict,init_order)
            component.shield_ent_id = shield_ent_id
           '''             

    def create_shield1(self,pos,vel,collision_type,xoff=0,yoff=0):
        elib = self.gameworld.parent.entitylib
        create_dict, init_order = elib.get_template('shield1',
                                                    collision_type,
                                                    pos=pos,
                                                    vel=vel)
        return create_dict,init_order

    
    
    def update(self,dt):
        for component in self.components:
            if component is not None and component.parent_ent is not None:
                pass
            #either ensure the shield entity stays on parent position,
            # OR render a shield around the target while replacing its renderering
                
        

Factory.register('ShieldSystem',cls=ShieldSystem)



class TimerSystem(DefaultGameSystem):
    """
    Updates roughly once every 60 frames
    """
    frame_count=60
    default_args = { 'countdown': 1,
                     'do_remove':False}
    def __init__(self,**kwargs):
        super(TimerSystem,self).__init__(**kwargs)
        
    def update(self,dt):
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                #entity = self.gameworld.entities[entity_id]
                component.countdown -= 1
                #Note: Consider moving this logic to destruct system
                if component.countdown <= 0 and component.do_remove:
                    self.gameworld.remove_entity(entity_id)
        
Factory.register('TimerSystem',cls=TimerSystem)


class TemplateSystem(DefaultGameSystem):
    default_args = {'target_id': None}
    def __init__(self,**kwargs):
        super(TemplateSystem,self).__init__(**kwargs)

Factory.register('TemplateSystem',cls=TemplateSystem)



#Note: Level might be set as a game or gameworld property
class LevelSystem(DefaultGameSystem):
    def __init__(self,**kwargs):
        super(LevelSystem,self).__init__(**kwargs)
        pass
Factory.register('LevelSystem',cls=LevelSystem)





#Refcode snippets
#print texutils.get_tex_region(texture_manager,'ship1',0)
    
#body.position.x = 255
#entity.position.x = 255

#body.movement += cymunk.Vec2d(0,100)
#body.movement = (0,300)
#print dir(body)
#print self.parent.parent.ids
        
    
#    
#if __name__ == '__main__':
#    ElectricNemoApp().run()
                            