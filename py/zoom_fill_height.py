import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

render_w = bpy.context.scene.render.resolution_x # 1080
render_h = bpy.context.scene.render.resolution_y # 1920

# Calculate exact scale factor so height touches top & bottom of 9:16 canvas (1920px)
# Base VSE height for 16:9 video fitted to 1080w is (1080 * 9 / 16) = 607.5px
# Target height 1920 / 607.5 = 3.1604938271604937
base_vse_h = render_w * (9.0 / 16.0)
scale_factor = render_h / base_vse_h # 3.1604938271604937

scaled_count = 0
for seq in seq_list:
    if seq.type == 'MOVIE' and hasattr(seq, "transform"):
        t = seq.transform
        t.scale_x = scale_factor
        t.scale_y = scale_factor
        t.offset_x = 0.0
        t.offset_y = 0.0
        scaled_count += 1

print(f"ZOOM_FILL_HEIGHT_SUCCESS: Scaled {scaled_count} strips by factor {scale_factor:.4f} so height touches top and bottom borders!")
