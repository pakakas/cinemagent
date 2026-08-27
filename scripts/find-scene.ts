#!/usr/bin/env bun

const SERVER_URL = "http://127.0.0.1:8080";

export async function findVideoPath() {
  const code = `
import bpy, os

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
filepath = ""
for s in seq_list:
    if hasattr(s, "filepath"):
        filepath = os.path.abspath(bpy.path.abspath(s.filepath))
        break

print("FULL_PATH=" + filepath)
`;

  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log(res.output || res);
}

if (import.meta.main) {
  await findVideoPath();
}
