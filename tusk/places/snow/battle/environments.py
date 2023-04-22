from tusk.places.objects import Sprite

class CragValley:
    class Background(Sprite):
        art_index: str = "0:6740003"

    class Foreground(Sprite):
        art_index: str = "0:6740004"

    class Rock(Sprite):
        art_index: str = "0:6740008"

class Forest:
    class Background(Sprite):
        art_index: str = "0:6740006"

    class Foreground(Sprite):
        art_index: str = "0:6740007"

    class Rock(Sprite):
        art_index: str = "0:100394"

class MountainTop:
    class Background(Sprite):
        art_index: str = "0:100380"

    class Foreground(Sprite):
        art_index: str = "0:6740004"

    class Rock(Sprite):
        art_index: str = "0:100394"