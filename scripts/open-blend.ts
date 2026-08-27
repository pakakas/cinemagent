#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

export async function openBlendFile(filepath: string) {
  const safePath = filepath.replace(/\\/g, "/");
  let code = await Bun.file(join(PY_DIR, "open_blend.py")).text();
  code = code.replace("{FILEPATH}", safePath);

  console.log(`[Bun Native] Opening blend file: ${safePath}...`);
  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const res = await resp.json();
  console.log("[Bun Native] Result:", res);
  return res;
}

if (import.meta.main) {
  const fileArg = process.argv[2] || "D:/videos/guray.blend";
  await openBlendFile(fileArg);
}
