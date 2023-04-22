from tusk.places.snow.models.card import Element
from tusk.places.snow.objects import MoveTileTemplate
from tusk.managers.object import Object
from dataclasses import dataclass, field
from tusk.client import MetaplaceServerProtocol

from .environments import *
from ..constants import BOARD_HEIGHT, BOARD_WIDTH
import random
import asyncio

@dataclass
class SharedObject(Object):
    penguin_objects: dict = field(default_factory=dict)

    def add_penguin_obj(self, penguin_id, obj):
        self.penguin_objects[penguin_id] = obj

    def remove_penguin_obj(self, penguin_id):
        if penguin_id in self.penguin_objects:
            del self.penguin_objects[penguin_id]

    def __getattr__(self, instance):
        async def handler(*args, **kwargs):
            for game_object in self.penguin_objects.values():
                try:
                    await getattr(game_object, instance)(*args, **kwargs)
                except:
                    pass

        return handler 

class BattleManager:

    def __init__(self, server):
        self.object_id = 0
        self.objects = {}
        self.board = {}
        self.server = server
        self.fire_ninja = None
        self.water_ninja = None
        self.snow_ninja = None
        self.environment = random.choice([CragValley, Forest, MountainTop])

        loop = asyncio.get_running_loop()
        self.timeout = loop.call_at(30, lambda: asyncio.ensure_future(self.start))
    
    async def init(self):
        loop = asyncio.get_running_loop()
        loop.call_at(16, lambda: asyncio.ensure_future(self.start))

    async def start(self):
        # TODO: Check if the game autostarted; if it is autostarted, remove any unused penguins! if it exists.
        for y in range(BOARD_HEIGHT):
            self.board[y] = {}
            for x in range(BOARD_WIDTH):
                tile = self.board[x] = await self.create_object(x=x, y=y, template=MoveTileTemplate)
                tile.set_input_handler(self.tile_pressed)

    async def tile_pressed(self, p, tile):
        # a tip to anyones reading this and want a quick implementation
        # here is a guide
        # when the ninja presses a tile get the tile's X and Y and store it to a temporary variable 
        # which then we would have to recover when moving the ninjas,
        # but before the timer expires make it so that it would put penguin "ghosts"
        # if a ghost of the penguin exists beforehand remove the existing ghost (by doing await ghost.remove())
        #  before adding another one.
        pass # TODO: Tile press handling.

    async def join(self, p):

        if p in self.ninjas:
            return

        element = await p.server.redis.get(f'{p.user.id}.element')
        self.ninjas.append(p)
        # sync objects
        for obj in self.objects.values():
            player_obj = await p.objects.copy_object(obj)
            obj.add_penguin_obj(p.user.id, player_obj)
        
        if len(self.ninjas) > 3:
            await self.start()

        
    async def create_object(self, *args, **kwargs):
        self.object_id += 1
        object = SharedObject(None, self.object_id, *args, **kwargs)
        for ninja in self.ninjas:
            player_obj = await ninja.objects.copy_object(object)
            object.add_penguin_obj(ninja.user.id, player_obj)
        return object