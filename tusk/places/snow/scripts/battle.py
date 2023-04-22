from tusk.handlers import slash_command, authenticated, server_command
from tusk.places.snow import OnPlaceId
from tusk.places.snow.windowmanager import window_event
from tusk.places.snow.battle import BattleManager

@slash_command('place_ready')
@OnPlaceId('0:10001')
@authenticated
async def place_ready(p):
    player_object = await p.objects.create_object(x=5, y=2.5)
    await p.send_tag('P_CAMERA', 4.5, 2.5, 0, 0, 1)
    await p.send_tag('P_ZOOM', 1)
    await p.send_tag('P_LOCKZOOM', 1)
    await p.send_tag('P_LOCKCAMERA', 1)
    await player_object.set_as_camera_target()


@window_event("roomToRoomMinTime")
@OnPlaceId('0:10001')
@authenticated
async def handle_room_loaded(p, **_):
    await p.server.battle_manager.join(p)

@window_event("roomToRoomComplete")
@OnPlaceId('0:10001')
@authenticated
async def handle_room_loaded(p, **_):
    await p.server.battle_manager.join(p)

@server_command('boot')
@OnPlaceId('0:10001')
async def setup_battle(server):
    server.battle_manager = BattleManager(server)