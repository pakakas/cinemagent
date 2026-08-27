#!/usr/bin/env bun

const SERVER_URL = "http://127.0.0.1:8080";

export async function inspectStrips() {
  const code = `
import bpy, json

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

res = []
for s in seq_list:
    res.append({
        "name": s.name,
        "type": s.type,
        "channel": s.channel,
        "frame_start": s.frame_start,
        "frame_offset_start": getattr(s, "frame_offset_start", 0),
        "frame_final_duration": getattr(s, "frame_final_duration", 0),
        "frame_offset_end": getattr(s, "frame_offset_end", 0)
    })

print("STRIP_DATA=" + json.dumps(res, indent=2))
`;

  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log(res.output || res);
  return res;
}

if (import.meta.main) {
  await inspectStrips();
}
