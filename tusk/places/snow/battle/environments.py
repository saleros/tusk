from tusk.places.objects import Sprite

class CragValley:
    PENGUIN_SPAWNS = [
        (0, 0),
        (0, 2),
        (0, 4)
    ]

    class Background(Sprite):
        art_index: str = "0:6740003"

    class Foreground(Sprite):
        art_index: str = "0:6740004"

    class Rock(Sprite):
        art_index: str = "0:6740008"

class Forest(CragValley):
    class Background(Sprite):
        art_index: str = "0:6740006"

    class Foreground(Sprite):
        art_index: str = "0:6740007"

    class Rock(Sprite):
        art_index: str = "0:100394"

class MountainTop(CragValley):
    class Background(Sprite):
        art_index: str = "0:100380"

    class Foreground(Sprite):
        pass

    class Rock(Sprite):
        art_index: str = "0:100394"