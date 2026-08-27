import bpy

try:
    scene = bpy.context.scene
    if hasattr(scene, "blender_mcp_use_vse"):
        scene.blender_mcp_use_vse = True

    if hasattr(bpy.ops.wm, "blender_mcp_start_server"):
        bpy.ops.wm.blender_mcp_start_server()
        print("BLENDER_MCP_OPERATOR_STARTED_SUCCESS")
    else:
        print("BLENDER_MCP_OPERATOR_NOT_FOUND")
except Exception as e:
    print(f"BLENDER_MCP_OPERATOR_ERROR: {e}")
