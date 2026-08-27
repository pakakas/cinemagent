import bpy
import json
import sys
import io
import traceback
import threading
import queue
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 8080

task_queue = queue.Queue()

def main_thread_executor():
    """Runs on Blender's main loop to safely execute BPY operators."""
    try:
        while not task_queue.empty():
            try:
                code, event, result_holder = task_queue.get_nowait()
            except queue.Empty:
                break

            old_stdout, old_stderr = sys.stdout, sys.stderr
            captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                
                exec_globals = {
                    "bpy": bpy,
                    "json": json,
                    "sys": sys
                }
                exec(code, exec_globals)
                
                result_holder["success"] = True
                result_holder["output"] = captured_stdout.getvalue()
                result_holder["error"] = captured_stderr.getvalue()
            except Exception as e:
                result_holder["success"] = False
                result_holder["error"] = str(e)
                result_holder["traceback"] = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                event.set()
    except Exception as outer_e:
        print(f"[BlenderServer Timer Exception]: {outer_e}")
    return 0.05

class BlenderAgentHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path in ('/status', '/'):
            self._send_response(200, {
                "status": "ok",
                "blender_version": bpy.app.version_string,
                "file": bpy.data.filepath or "Untitled"
            })
        else:
            self._send_response(404, {"error": "Not Found"})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            payload = json.loads(body) if body else {}
        except Exception as e:
            self._send_response(400, {"error": f"Invalid JSON: {str(e)}"})
            return

        if self.path == '/exec':
            code = payload.get('code', '')
            if not code:
                self._send_response(400, {"error": "Missing 'code' parameter"})
                return
            
            event = threading.Event()
            result_holder = {}
            task_queue.put((code, event, result_holder))
            
            completed = event.wait(timeout=10.0)
            if not completed:
                self._send_response(504, {"error": "Execution timed out (10s)"})
                return

            if result_holder.get("success"):
                self._send_response(200, result_holder)
            else:
                self._send_response(500, result_holder)

        elif self.path == '/eval':
            expr = payload.get('expression', '')
            event = threading.Event()
            result_holder = {}
            
            eval_code = f"__result = ({expr})"
            task_queue.put((eval_code, event, result_holder))
            
            completed = event.wait(timeout=5.0)
            if completed and result_holder.get("success"):
                self._send_response(200, {"success": True, "result": result_holder.get("output")})
            else:
                self._send_response(500, result_holder)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def log_message(self, format, *args):
        print(f"[BlenderServer] {self.address_string()} - {format % args}")

def run_server():
    server = HTTPServer((HOST, PORT), BlenderAgentHandler)
    print(f"==================================================")
    print(f"🚀 Blender Agent Server running at http://{HOST}:{PORT}")
    print(f"   Blender Version: {bpy.app.version_string}")
    print(f"==================================================")
    server.serve_forever()

if __name__ == "__main__":
    if not bpy.app.timers.is_registered(main_thread_executor):
        bpy.app.timers.register(main_thread_executor)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
