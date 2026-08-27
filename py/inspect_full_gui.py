import bpy, json

screen = getattr(bpy.context, "screen", None) or getattr(bpy.context.window, "screen", None)
area_types = [a.type for a in screen.areas] if screen else []

info = {
    "file": bpy.data.filepath,
    "workspace": getattr(bpy.context.workspace, "name", ""),
    "screen_areas": area_types,
    "objects_in_scene": [o.name for o in bpy.data.objects],
    "active_object": getattr(bpy.context.active_object, "name", None),
    "camera": getattr(bpy.context.scene.camera, "name", None),
    "vse_sequences": [s.name for s in getattr(getattr(bpy.context.scene, "sequence_editor", None), "sequences", [])],
    "resolution": f"{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y} @ {bpy.context.scene.render.fps}FPS"
}

print("FULL_GUI_INSPECT=" + json.dumps(info, indent=2))
