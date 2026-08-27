#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

export async function hardSnapToZero() {
  const code = await Bun.file(join(PY_DIR, "snap_zero.py")).text();
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
