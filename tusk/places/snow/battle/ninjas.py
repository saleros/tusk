from tusk.places.snow.objects import *
from tusk.places.snow.models.card import Element
from .entities import Entity
from abc import abstractmethod

ninjas = {}

def Ninja(element):
    def decorate(cls):
        ninjas[int(element)] = cls
        return cls
    return decorate


class BaseNinja(Entity):

    def __init__(self, penguin, object):
        self.penguin = penguin
        self._object = object

    health_bar = RegularHealthBar

    @property
    @abstractmethod
    def celebrate_intro_anim(self):
        """This gets played when the ninjas win the game, there are usually two animations, start and loop"""

    @property
    @abstractmethod
    def celebrate_loop_anim(self):
        """This gets played when the ninjas win the game, there are usually two animations, start and loop"""

    @property
    @abstractmethod
    def revive_other_intro_anim(self):
        """This gets played when a ninja revives another ninja"""

    @property
    @abstractmethod
    def revive_other_loop_anim(self):
        """This gets played when a ninja revives another ninja"""
    
    @property
    @abstractmethod
    def revived_anim(self):
        """This gets played when a ninja gets healed/revived"""


@Ninja(Element.FIRE)
class FireNinja(BaseNinja):
    max_health = 30
    idle_anim = FireNinjaIdleAnim
    move_anim = FireNinjaMoveAnim
    hit_anim = FireNinjaHitAnim
    knockout_intro_anim = FireNinjaKnockoutStartAnim
    knockout_anim = FireNinjaKnockoutStartAnim
    celebrate_intro_anim = FireNinjaCelebrateStartAnim
    celebrate_loop_anim = FireNinjaCelebrateLoopAnim
    revive_other_intro_anim = FireNinjaIdleAnim
    revive_other_loop_anim = FireNinjaIdleAnim
    revived_anim = FireNinjaIdleAnim

@Ninja(Element.SNOW)
class SnowNinja(BaseNinja):
    max_health = 28
    idle_anim = FireNinjaIdleAnim
    move_anim = FireNinjaMoveAnim
    hit_anim = FireNinjaHitAnim
    knockout_intro_anim = FireNinjaKnockoutStartAnim
    knockout_anim = FireNinjaKnockoutStartAnim
    celebrate_intro_anim = FireNinjaCelebrateStartAnim
    celebrate_loop_anim = FireNinjaCelebrateLoopAnim
    revive_other_intro_anim = FireNinjaIdleAnim
    revive_other_loop_anim = FireNinjaIdleAnim
    revived_anim = FireNinjaIdleAnim

@Ninja(Element.WATER)
class WaterNinja(BaseNinja):
    max_health = 38
    idle_anim = FireNinjaIdleAnim
    move_anim = FireNinjaMoveAnim
    hit_anim = FireNinjaHitAnim
    knockout_intro_anim = FireNinjaKnockoutStartAnim
    knockout_anim = FireNinjaKnockoutStartAnim
    celebrate_intro_anim = FireNinjaCelebrateStartAnim
    celebrate_loop_anim = FireNinjaCelebrateLoopAnim
    revive_other_intro_anim = FireNinjaIdleAnim
    revive_other_loop_anim = FireNinjaIdleAnim
    revived_anim = FireNinjaIdleAnim
