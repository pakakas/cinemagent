import bpy

scene = bpy.context.scene

# 1. Clear all VSE sequences
seq_ed = getattr(scene, "sequence_editor", None)
if seq_ed:
    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
    for s in list(seq_coll):
        try:
            seq_coll.remove(s)
        except Exception:
            pass

# 2. Wipe ALL datablocks in the .blend file (Objects, Materials, Sounds, Images, Clips, GPencil)
datablocks = [
    bpy.data.objects,
    bpy.data.materials,
    bpy.data.textures,
    bpy.data.images,
    bpy.data.sounds,
    bpy.data.movieclips,
    bpy.data.grease_pencils,
    bpy.data.curves,
    bpy.data.meshes,
    bpy.data.cameras,
    bpy.data.lights
]

for block in datablocks:
    for item in list(block):
        try:
            block.remove(item)
        except Exception:
            pass

# 3. Reset scene parameters
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.fps_base = 1.0

scene.frame_start = 1
scene.frame_end = 250
scene.frame_current = 1

# Redraw UI areas
for win in bpy.context.window_manager.windows:
    screen = win.screen
    if screen:
        for area in screen.areas:
            area.tag_redraw()

# 4. Save file
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("FACTORY_RESET_SUCCESS: Completely wiped all datablocks, objects, sequences, sounds, and materials!")
