from tusk.handlers import slash_command

# Technically counts as a sound but putting it here anyways since they're closely related.
@slash_command('sound_done')
async def sound_done(p, sound_id, handle_id):
    sound = p.sounds.get_sound(int(sound_id))
    if sound is None:
        return
    callback = sound.callbacks.get(int(handle_id))
    if callback is not None:
        await callback(p)

@slash_command('anim_done')
async def object_animation_done(p, obj_id, handle_id):
    object = p.objects.get_object(int(obj_id))
    if object is None:
        return
    callback = object.callbacks.get(int(handle_id))
    if callback is not None:
        await callback(p)