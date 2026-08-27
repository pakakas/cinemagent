import sys, bpy

addon_dir = r"C:\Users\ucing\AppData\Roaming\Blender Foundation\Blender\5.2\scripts\addons"
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

try:
    import blender_mcp_vse
    blender_mcp_vse.register()
except Exception:
    pass

try:
    import blender_mcp_vse
    srv = blender_mcp_vse.BlenderMCPServer(host='localhost', port=9876)
    srv.start()
    print("MCP_SOCKET_SERVER_STARTED_ON_PORT_9876")
except Exception as e:
    print(f"MCP_SOCKET_SERVER_ERROR: {e}")
