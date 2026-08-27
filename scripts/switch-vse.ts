#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

export async function switchVideoEditing() {
  const code = await Bun.file(join(PY_DIR, "switch_vse.py")).text();
  console.log("Switching layout to Video Editing VSE...");
  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log("Result:", res);
  return res;
}

if (import.meta.main) {
  await switchVideoEditing();
}
