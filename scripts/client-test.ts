#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

export async function checkStatus() {
  const resp = await fetch(`${SERVER_URL}/status`);
  const data = await resp.json();
  console.log("Server Status:", data);
  return data;
}

export async function sendPyFile(scriptName: string, replacements: Record<string, string> = {}) {
  const pyPath = join(PY_DIR, scriptName);
  let code = await Bun.file(pyPath).text();
  
  for (const [key, value] of Object.entries(replacements)) {
    code = code.replaceAll(`{${key}}`, value);
  }

  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  const data = await resp.json();
  console.log("Execution Result:", data);
  return data;
}

if (import.meta.main) {
  console.log("1. Checking Blender agent server status...");
  try {
    await checkStatus();
    console.log("\n2. Executing create_cube.py from disk...");
    await sendPyFile("create_cube.py");
  } catch (err) {
    console.error("Failed to communicate with Blender Server:", err);
  }
}
