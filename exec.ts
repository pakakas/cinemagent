#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "py");

async function runExec() {
  const rawTarget = process.argv[2];
  if (!rawTarget) {
    console.log(`
🚀 Blender Agent CLI Executor (exec.ts)

Usage:
  bun .inbox/blender-server/exec.ts <script-name> [args...]
`);
    process.exit(0);
  }

  let scriptBaseName = rawTarget.replace(/-/g, "_");
  if (!scriptBaseName.endsWith(".py")) {
    scriptBaseName += ".py";
  }

  const pyPath = join(PY_DIR, scriptBaseName);
  const fileExists = await Bun.file(pyPath).exists();

  if (!fileExists) {
    console.error(`❌ Error: Python script "${scriptBaseName}" not found in ${PY_DIR}`);
    process.exit(1);
  }

  let code = await Bun.file(pyPath).text();

  const arg1 = process.argv[3];
  const arg2 = process.argv[4];
  const arg3 = process.argv[5];
  const arg4 = process.argv[6];
  const arg5 = process.argv[7];

  if (scriptBaseName.includes("add_video_strip")) {
    if (!arg1) {
      console.error(`❌ Error: Missing required argument <filepath> for ${scriptBaseName}`);
      console.error(`Usage: bun .inbox/blender-server/exec.ts add-video-strip <filepath> [strip-name] [res-x] [res-y] [fps]`);
      process.exit(1);
    }
    const filePath = arg1.replace(/\\/g, "/");
    const stripName = arg2 || "";
    const resX = arg3 || "";
    const resY = arg4 || "";
    const fpsVal = arg5 || "";

    code = code
      .replaceAll("{FILEPATH}", filePath)
      .replaceAll("{STRIP_NAME}", stripName)
      .replaceAll("{RES_X}", resX)
      .replaceAll("{RES_Y}", resY)
      .replaceAll("{FPS}", fpsVal);
  } else if (scriptBaseName.includes("trim_video")) {
    if (!arg1) {
      console.error(`❌ Error: Missing required argument <seconds> for ${scriptBaseName}`);
      process.exit(1);
    }
    code = code.replaceAll("{START_SECONDS}", arg1);
  } else if (scriptBaseName.includes("trim_after_sec")) {
    if (!arg1) {
      console.error(`❌ Error: Missing required argument <seconds> for ${scriptBaseName}`);
      process.exit(1);
    }
    code = code.replaceAll("{TARGET_SECONDS}", arg1);
  } else if (scriptBaseName.includes("open_blend") || scriptBaseName.includes("create_new_project") || scriptBaseName.includes("save_as")) {
    if (!arg1) {
      console.error(`❌ Error: Missing required argument <filepath> for ${scriptBaseName}`);
      process.exit(1);
    }
    let filePath = arg1.replace(/\\/g, "/");
    if (!filePath.endsWith(".blend")) filePath += ".blend";
    code = code.replaceAll("{FILEPATH}", filePath);
  }

  console.log(`[Bun Exec] Running "${scriptBaseName}" on Blender Agent Server...`);

  try {
    const resp = await fetch(`${SERVER_URL}/exec`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });

    const res = await resp.json();
    if (res.success) {
      console.log(`✅ Success:\n${res.output}`);
    } else {
      console.error(`❌ Server Error:\n${res.error || res.traceback}`);
    }
  } catch (err: any) {
    console.error(`❌ HTTP Error: Could not connect to Blender Server on ${SERVER_URL}`);
  }
}

if (import.meta.main) {
  await runExec();
}
