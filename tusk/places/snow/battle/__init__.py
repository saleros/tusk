from tusk.places.snow.models.card import Element
from tusk.places.snow.objects import RockTileTemplate, MoveTileTemplate, Template
from tusk.places.snow.models.window import CloseCjsnowRoomToRoomAction
from tusk.managers.object import Object
from dataclasses import dataclass, field
from tusk.client import MetaplaceServerProtocol
from typing import Dict
from .environments import *
from .ninjas import ninjas
from ..constants import BOARD_HEIGHT, BOARD_WIDTH, ROCKS_SPAWN_POINT
import random
import asyncio
import weakref

@dataclass
class SharedObject:
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
    penguin_objects: Dict = field(default_factory=dict)

    def add_penguin_obj(self, penguin_id, obj):
        self.penguin_objects[penguin_id] = obj

    def remove_penguin_obj(self, penguin_id):
        if penguin_id in self.penguin_objects:
            del self.penguin_objects[penguin_id]

    def get_penguin_obj(self, penguin_id):
        return self.penguin_objects.get(penguin_id)

    async def move(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z
        for game_object in self.penguin_objects.values():
            await game_object.move(x, y, z)

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
        self.obstacles = {}
        self.board = {}
        self.ninjas = []
        self.server = server
        self.fire_ninja = None
        self.water_ninja = None
        self.snow_ninja = None
        self.environment = random.choice([CragValley, Forest, MountainTop])
        self.ref = weakref.proxy(self)
    
    async def init(self):
        self.fire_ninja = await self.create_object(x=4.5, y=2.5)
        self.water_ninja = await self.create_object(x=4.5, y=2.5)
        self.snow_ninja = await self.create_object(x=4.5, y=2.5)

    async def start(self):
        # TODO: Check if the game autostarted; if it is autostarted, remove any unused penguins! if it exists.

        # This sets the spawn position of the ninjas:
        spawns = self.environment.PENGUIN_SPAWNS.copy()
        random.shuffle(spawns)
        await self.fire_ninja.move(*spawns.pop())
        await self.water_ninja.move(*spawns.pop())
        await self.snow_ninja.move(*spawns.pop())


        _background = await self.create_object(x=3.98869, y=-2.11106, art=self.environment.Background)
        _foreground = await self.create_object(x=4, y=5.1, art=self.environment.Foreground)
        for x in range(BOARD_WIDTH):
            self.board[x] = {}
            for y in range(BOARD_HEIGHT):
                tile = self.board[x][y] = await self.create_object(x=x, y=y, template=MoveTileTemplate)
                await tile.set_input_handler(self.tile_pressed)

        for x, y in ROCKS_SPAWN_POINT:
            self.obstacles[x] = self.obstacles.get(x, {})
            # We currently store the Obstacle into an object for future usages. 
            # will be used when writing the CPU players for snow minions.
            rock = self.obstacles[x][y] = await self.create_object(x=x, y=y, template=RockTileTemplate) 
            await rock.update_sprite(self.environment.Rock)

        for ninja in self.ninjas:
            await ninja.load(self.ref)

        await self.send_action(CloseCjsnowRoomToRoomAction())
        
    async def send_action(self, action):
        aws = []
        for ninja in self.ninjas:
            aws.append(ninja.penguin.window_manager.send_action(action))
        await asyncio.gather(*aws)

    async def tile_pressed(self, p, tile):
        # a tip to anyones reading this and want a quick implementation
        # here is a guide
        # when the ninja presses a tile get the tile's X and Y and store it to a temporary variable 
        # which then we would have to recover when moving the ninjas,
        # but before the timer expires make it so that it would put penguin "ghosts"
        # if a ghost of the penguin exists beforehand remove the existing ghost (by doing await ghost.remove())
        #  before adding another one.
        pass # TODO: Tile press handling.

    def get_ninja_by_element(self, element):
        if element == Element.FIRE:
            return self.fire_ninja
        elif element == Element.WATER:
            return self.water_ninja
        elif element == Element.SNOW:
            return self.snow_ninja
        #TODO: sensei (This is the last thing we do so we do not worry about this yet)

    def get_ninja_by_penguin(self, p):
        for ninja in self.ninjas:
            if ninja.penguin == p:
                return ninja

    async def join(self, p):
        if self.get_ninja_by_penguin(p) is not None:
            return self.get_ninja_by_penguin(p).object.get_penguin_obj(p.user.id)

        #init ninja object
        element = await p.server.redis.hget(p.server.name, p.user.id)
        element = int(element)
        ninja_obj = ninjas.get(element)
        self.ninjas.append(ninja_obj(p, self.get_ninja_by_element(element)))

        # sync objects
        for obj in self.objects.values():
            player_obj = await p.objects.copy_object(obj)
            obj.add_penguin_obj(p.user.id, player_obj)
        
        if len(self.ninjas) >= 3:
            await self.start()
        return self.get_ninja_by_penguin(p).object.get_penguin_obj(p.user.id)

        
    async def create_object(self, *args, **kwargs):
        self.object_id += 1
        self.objects[self.object_id] = object = SharedObject(self.object_id, *args, **kwargs)
        for ninja in self.ninjas:
            player_obj = await ninja.penguin.objects.copy_object(object)
            object.add_penguin_obj(ninja.penguin.user.id, player_obj)
        return object