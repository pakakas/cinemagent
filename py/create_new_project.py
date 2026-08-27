import bpy

target_path = "{FILEPATH}"

try:
    # 1. Reset to clean empty file
    bpy.ops.wm.read_homefile(use_empty=True)
    
    # 2. Embed Agent autostart script
    autostart_code = """import bpy, queue, threading, http.server, json

HOST = '127.0.0.1'
PORT = 8080
cmd_queue = queue.Queue()

class AgentHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def _send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path == '/status':
            self._send_json({"status": "running", "file": bpy.data.filepath})
        else: self._send_json({"error": "not found"}, 404)
    def do_POST(self):
        if self.path == '/exec':
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length).decode())
            res_q = queue.Queue()
            cmd_queue.put((payload.get('code', ''), res_q))
            res = res_q.get(timeout=30)
            self._send_json(res)
        else: self._send_json({"error": "not found"}, 404)

def main_thread_executor():
    while not cmd_queue.empty():
        code, res_q = cmd_queue.get_nowait()
        try:
            import io, sys
            out = io.StringIO()
            sys.stdout = out
            exec(code, globals())
            sys.stdout = sys.__stdout__
            res_q.put({"success": True, "output": out.getvalue()})
        except Exception as e:
            import traceback
            res_q.put({"success": False, "error": str(e), "traceback": traceback.format_exc()})
    return 0.1

if not getattr(bpy.app, '_agent_server_started', False):
    server = http.server.HTTPServer((HOST, PORT), AgentHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    bpy.app.timers.register(main_thread_executor)
    bpy.app._agent_server_started = True
    print(f"[Agent Server] Running on http://{HOST}:{PORT}")
"""
    
    text_block = bpy.data.texts.new("agent_autostart.py")
    text_block.write(autostart_code)
    text_block.use_register = True
    
    # 3. Save as new project file
    bpy.ops.wm.save_as_mainfile(filepath=target_path)
    print(f"CREATE_PROJECT_SUCCESS: Created new Blender project at '{target_path}'!")
except Exception as e:
    print(f"CREATE_PROJECT_ERROR: {e}")
