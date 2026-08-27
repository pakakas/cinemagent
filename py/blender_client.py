import os
import json
import urllib.request
import urllib.error

BLENDER_HTTP_URL = "http://127.0.0.1:8080/exec"

def send_bpy_code(code_str: str) -> dict:
    """Send arbitrary BPY code to live running Blender GUI on port 8080."""
    data = json.dumps({"code": code_str}).encode("utf-8")
    req = urllib.request.Request(
        BLENDER_HTTP_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as he:
        body = he.read().decode("utf-8")
        return {"success": False, "http_status": he.code, "body": body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_time_to_frame(time_val: str, fps: float = 25.0) -> int:
    """Parse time string like '1:18', '7.5', '44', '00:09.10', or frame count to integer frame."""
    time_str = str(time_val).strip()
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:
            mins = float(parts[0])
            sec_parts = parts[1].split(".")
            secs = float(sec_parts[0])
            frames = float(sec_parts[1]) if len(sec_parts) > 1 else 0.0
            return int((mins * 60 + secs) * fps + frames)
        elif len(parts) == 3:
            hrs = float(parts[0])
            mins = float(parts[1])
            secs = float(parts[2])
            return int((hrs * 3600 + mins * 60 + secs) * fps)
    try:
        val = float(time_str)
        return int(val * fps) if val < 200.0 else int(val)
    except ValueError:
        return 1
