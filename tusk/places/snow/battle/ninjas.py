from tusk.places.snow.objects import *
from tusk.places.snow.models.card import Element

ninjas = {}

def Ninja(element):
    def decorate(cls):
        ninjas[int(element)] = cls
        return cls
    return decorate


@Ninja(Element.FIRE)
class FireNinja:
    pass #TODO: do ninjas and entities