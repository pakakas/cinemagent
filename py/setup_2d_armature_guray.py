import bpy, os

char_img_path = "C:/Users/ucing/.gemini/antigravity/brain/d1ecffbe-2710-45cb-b8ef-2f3490268b60/scratch/guray_transparent.png"
if not os.path.exists(char_img_path):
    char_img_path = "D:/videos/guray/Gemini_Generated_Image_wx163uwx163uwx16.png"

try:
    # 1. Clear objects cleanly
    for obj in list(bpy.data.objects):
        try:
            bpy.data.objects.remove(obj, do_unlink=True)
        except Exception:
            pass

    # 2. Load Texture & Material
    img = bpy.data.images.load(char_img_path)
    mat = bpy.data.materials.new(name="Guray2DMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    tex_node = nodes.new("ShaderNodeTexImage")
    tex_node.image = img
    
    if bsdf:
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        if "Alpha" in tex_node.outputs and "Alpha" in bsdf.inputs:
            links.new(tex_node.outputs["Alpha"], bsdf.inputs["Alpha"])
    mat.blend_method = 'BLEND'

    # 3. Pure PyData Mesh Creation (Instant & robust)
    verts = [(-0.72, -1.28, 0), (0.72, -1.28, 0), (0.72, 1.28, 0), (-0.72, 1.28, 0)]
    faces = [(0, 1, 2, 3)]
    
    mesh_data = bpy.data.meshes.new("Guray2DMeshData")
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()

    plane = bpy.data.objects.new("Guray2DMesh", mesh_data)
    bpy.context.scene.collection.objects.link(plane)
    plane.data.materials.append(mat)

    # 4. Save mainfile
    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()

    print("SETUP_2D_ARMATURE_SUCCESS: Built 2D Character Surface Mesh with Guray Texture!")
except Exception as e:
    print(f"SETUP_2D_ARMATURE_ERROR: {e}")
