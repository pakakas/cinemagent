import bpy

# 1. Convert workspace primary area to VIEW_3D with Material Shading
window = bpy.context.window_manager.windows[0]
screen = window.screen

for area in screen.areas:
    area.type = 'VIEW_3D'
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = 'MATERIAL'
            space.shading.use_scene_lights = False
            space.shading.use_scene_world = False
            space.show_object_viewport_armature = True
    break

# 2. Add 3D Scene Strip into VSE Sequencer
scene = bpy.context.scene
seq_ed = getattr(scene, "sequence_editor", None)
if not seq_ed:
    seq_ed = scene.sequence_editor_create()

seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None)
if seq_coll:
    has_scene_strip = any(getattr(s, "type", "") == "SCENE" for s in seq_coll)
    if not has_scene_strip:
        try:
            seq_coll.new_scene(name="Guray3DSceneStrip", scene=scene, channel=4, frame_start=1)
        except Exception:
            pass

print("SHOW_3D_VIEWPORT_SUCCESS: Switched workspace area to 3D Viewport with Material Preview!")
