import bpy, json

info = {
    "timeline_markers": [m.name for m in bpy.context.scene.timeline_markers],
    "texts": [t.name for t in bpy.data.texts],
    "grease_pencils": [g.name for g in bpy.data.grease_pencils],
    "objects": [o.name for o in bpy.data.objects],
    "workspaces": [w.name for w in bpy.data.workspaces]
}

print("DEBUG_SCENE=" + json.dumps(info, indent=2))
