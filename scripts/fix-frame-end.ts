#!/usr/bin/env bun

const SERVER_URL = "http://127.0.0.1:8080";

export async function setFullVideoDuration() {
  const code = `
import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

if seq_list:
    max_frame = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = max_frame
    fps = bpy.context.scene.render.fps
    seconds = max_frame / fps
    minutes = seconds / 60
    print(f"UPDATED: frame_end is now {max_frame} ({seconds:.1f}s / {minutes:.2f} mins)!")
else:
    print("No sequences found")
`;

  console.log("Setting scene frame_end to full video duration...");
  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log("Result:", res.output || res);
  return res;
}

if (import.meta.main) {
  await setFullVideoDuration();
}
