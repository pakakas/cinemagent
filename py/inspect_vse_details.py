import bpy, json

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

res = []
for s in seq_list:
    mods = [m.name for m in getattr(s, "modifiers", [])]
    res.append({
        "name": s.name,
        "type": s.type,
        "channel": s.channel,
        "modifiers": mods,
        "use_proxy": getattr(s, "use_proxy", False),
        "mute": getattr(s, "mute", False)
    })

print("VSE_DETAILS=" + json.dumps(res, indent=2))
