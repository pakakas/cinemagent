#!/usr/bin/env bun

const SERVER_URL = "http://127.0.0.1:8080";

export async function hardSnapToZero() {
  const code = `
import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

for s in seq_list:
    s.frame_start = 1.0

bpy.context.scene.frame_start = 1

if seq_list:
    max_f = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_end = max_f

print("HARD_SNAP_SUCCESS: Set all strip frame_start to 1.0 (Second 0.0)!")
`;

  console.log("[Bun Native] Snapping all strips to exact Frame 1 (Second 0.0)...");
  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log("[Bun Native] Result:", res.output || res);
  return res;
}

if (import.meta.main) {
  await hardSnapToZero();
}
