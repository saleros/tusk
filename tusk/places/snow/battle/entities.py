from abc import ABC, abstractmethod
from tusk.places.snow.objects import HealthBarTemplate
import math

class HPObject:
    HEALTH_BAR_FRAMES = 60

    def __init__(self, session, entity):
        self.session = session
        self.entity = entity
        self.max_health = self.entity.max_health
        self.health = self.max_health
    
    async def load(self):
        self.hp_object = await self.session.create_object(x=self.entity.object.x, y=self.entity.object.y, template=HealthBarTemplate)
        await self.hp_object.update_sprite(self.entity.health_bar)
        await self.update()
    
    async def update(self, decrease=0):
        start_frame = self.frame
        self.health -= decrease
        end_frame = self.frame
        await self.hp_object.animate_sprite(start_frame, end_frame, duration=0 if decrease <= 0 else 500)
    
    @property
    def frame(self):
        return (HPObject.HEALTH_BAR_FRAMES + 1) - math.floor(HPObject.HEALTH_BAR_FRAMES / self.max_health * self.health)

    @property
    def alive(self):
        return self.health > 0

class Entity(ABC):

    @property
    def object(self):
        """The `Room Object` instance for the entity"""
        return self._object

    @property
    def hp_object(self):
        """The `HPObject` instance for the entity's Health Bar"""
        return self._hp_object

    @property
    @abstractmethod
    def max_health(self):
        """The entity's Max Hit Points."""

    @property
    @abstractmethod
    def health_bar(self):
        """The Health bar used for the entity."""

    @property
    @abstractmethod
    def idle_anim(self):
        """This animation will play on default"""

    @property
    @abstractmethod
    def move_anim(self):
        """This animation will play when the entity moves"""

    @property
    @abstractmethod     
    def hit_anim(self):
        """This animation will play if the entity gets hit"""

    @property
    @abstractmethod
    def knockout_intro_anim(self):
        """This animation will play before (knockout_anim) if it exists"""

    @property
    @abstractmethod
    def knockout_anim(self):
       """This animation loops when the entity dies"""
    
    async def load(self, session):
        await self.object.update_sprite(self.idle_anim)
        self._hp_object = HPObject(session, self)
        await self.hp_object.load()