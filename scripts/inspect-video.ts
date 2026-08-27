#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

export async function inspectVideoSequences() {
  const code = await Bun.file(join(PY_DIR, "inspect_video.py")).text();
  try {
    const resp = await fetch(`${SERVER_URL}/exec`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const res = await resp.json();
    return res;
  } catch (err) {
    return null;
  }
}

if (import.meta.main) {
  const res = await inspectVideoSequences();
  if (res) {
    console.log(res.output || JSON.stringify(res, null, 2));
  } else {
    console.log("Server not reachable on port 8080.");
  }
}
