from dataclasses import dataclass, field
from tusk.places.objects import Sprite, Template
from typing import Any, Callable, Dict
import weakref

@dataclass
class Object:
    manager: Any
    id: int
    art: Sprite = Sprite
    x: int = 0
    y: int = 0
    z: int = 0
    name: str = ''
    template: Template = Template
    terrain: bool = True
    pickable: bool = False
    scale_by_depth: bool = False
    callbacks: Dict = field(default_factory=dict)

    def get_nearby_tiles(self, max_x, max_y, range_limit=1):
        return ((i, j-1) for i in range(max(self.x-range_limit, 0), min(self.x+1+range_limit, max_x+1)) 
                for j in range(max(self.y-range_limit, 0), min(self.y+1+range_limit, max_y+1)) 
                if abs(self.x-i) + abs(self.y-j) <= range_limit)

    @property
    def coords(self):
        return self.x + self.template.x_offset, self.y + self.template.y_offset

    async def init(self):
        await self.manager.penguin.send_tag('O_HERE', self.id, self.art.art_index, 
                                            *self.coords, self.z, int(not self.z),
                                            0, 0, 0, self.name, self.template, int(self.pickable), int(self.terrain), int(self.scale_by_depth))

    async def move(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z
        await self.manager.penguin.send_tag('O_MOVE', self.id, *self.coords, z)

    async def animate(self, sprite: Sprite, play_style='play_once', time_scale: int = 1, no_reset: bool = False, callback: Callable = None):
        handle_id = self.manager.handle_id
        if callback is not None:
            self.callbacks[handle_id] = callback
        await self.manager.penguin.send_tag('O_ANIM', self.id, sprite.art_index, play_style, 
                                            sprite.duration, time_scale, int(no_reset), self.id, handle_id)

    async def animate_sprite(self, start_frame=0, end_frame=0, backwards=False, play_style='play_once', duration=None):
        await self.manager.penguin.send_tag('O_SPRITEANIM', self.id, start_frame, end_frame, int(backwards), play_style, duration or '')

    async def update_sprite(self, sprite: Sprite, frame: int = 0, relative_path: str = ''):
        await self.manager.penguin.send_tag('O_SPRITE', self.id, sprite.art_index, frame, relative_path)

    async def set_as_camera_target(self):
        await self.manager.penguin.send_tag('O_PLAYER', self.id)

    async def delete(self):
        self.remove_input_handler()
        await self.manager.penguin.send_tag('O_GONE', self.id)

    def set_input_handler(self, callback):
        self.callbacks['input'] = callback
    
    def remove_input_handler(self):
        if 'input' in self.callbacks:
            del self.callbacks['input']

class ObjectManager:

    def __init__(self, penguin):
        self.penguin = penguin
        self._handle_id = 0
        self._game_object_id = 0
        self.objects = {}
        self.ref = weakref.proxy(self)
    
    @property
    def game_object_id(self):
        self._game_object_id += 1
        return self._game_object_id
    
    @property
    def handle_id(self):
        self._handle_id += 1
        return self._handle_id
    
    def get_object(self, obj_id):
        return self.objects.get(obj_id)

    async def create_object(self, art: Sprite = Sprite, x: int = 0, y: int = 0 , z: int = 0, 
                            name: str = '', template: Template = Template, terrain: bool = True, pickable: bool = False,
                            scale_by_depth: bool = False
                            ):
        obj_id = self.game_object_id
        obj = self.objects[obj_id] = Object(self.ref, obj_id, art, x, y, z, name, template, terrain, pickable, scale_by_depth)
        await obj.init()
        return obj

    async def copy_object(self, object):
        return await self.create_object(object.art, object.x, object.y, object.z, object.name, object.template, object.block, object.pickable, object.scale_by_depth)