from abc import ABC, abstractmethod, abstractproperty

class Entity(ABC):

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