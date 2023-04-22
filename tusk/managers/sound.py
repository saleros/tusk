from dataclasses import dataclass, field
from tusk.places.objects import Sprite
from typing import Any, Callable, Dict
import weakref

@dataclass
class Sound:
    manager: Any
    id: int
    art: str = '0:1'
    x: int = 0
    y: int = 0
    z: int = 0
    name: str = ''
    template: str = '0:1'
    block: bool = False
    pickable: bool = False
    scale_by_depth: bool = False
    callbacks: Dict = field(default_factory=dict)

    async def play(self, loop=False, volume=100):
        handle_id = self.manager.handle_id
        #I was going to implement the game object element of this but i decided not to as it is not used by CJSnow.
        await self.manager.penguin.send_tag('FX_PLAYSOUND', self.art_index, handle_id, int(loop), volume, -1, 0, -1)

class SoundManager:

    def __init__(self, penguin):
        self.penguin = penguin
        self._handle_id = 0
        self._game_object_id = 0
        self.sounds = {}
        self.ref = weakref.proxy(self)
    
    @property
    def game_object_id(self):
        self._game_object_id += 1
        return self._game_object_id
    
    @property
    def handle_id(self):
        self._handle_id += 1
        return self._handle_id
    
    def get_sound(self, obj_id):
        return self.sounds.get(obj_id)

