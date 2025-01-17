from tusk.places.snow import PlaceInput
from tusk.places import InputObj
from tusk.places.constants import MouseTarget, InputModifier, InputEvent


@PlaceInput(InputObj(
    input_id = "use",
    script_id = "0:10",
    event = InputEvent.MOUSE_CLICK,
    target = MouseTarget.GAME_OBJECT,
    modifier = InputModifier.NONE,
    command = "use"
))
async def game_object_selected(p, object_id, x, y, obj_x, obj_y):
    object_id = int(object_id)
    object = p.objects.get_object(object_id)
    await object.callbacks['input'](p, object)