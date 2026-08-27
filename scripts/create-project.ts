#!/usr/bin/env bun

import { copyFileSync, existsSync } from "fs";
import { dirname, join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";

export async function createProject(projectNameArg?: string) {
  const inputName = projectNameArg || process.argv[2] || "guray-dance";
  
  // 1. Query active blend file path dynamically from server
  let currentFile = "D:/videos/guray.blend";
  try {
    const sResp = await fetch(`${SERVER_URL}/status`);
    const sData = await sResp.json();
    if (sData.file && sData.file !== "Untitled" && existsSync(sData.file)) {
      currentFile = sData.file.replace(/\\/g, "/");
    }
  } catch (e) {}

  const baseDir = dirname(currentFile);
  let targetPath = inputName.replace(/\\/g, "/");
  
  if (!targetPath.endsWith(".blend")) {
    targetPath += ".blend";
  }
  if (!targetPath.includes("/")) {
    targetPath = join(baseDir, targetPath).replace(/\\/g, "/");
  }

  console.log(`[Bun Native] Dynamic Project Creation:`);
  console.log(`   Source Template: ${currentFile}`);
  console.log(`   Target Project:  ${targetPath}`);

  if (existsSync(currentFile)) {
    copyFileSync(currentFile, targetPath);
    console.log(`✅ Success: Created new project file on disk at ${targetPath}`);
  } else {
    console.error(`❌ Error: Source template ${currentFile} not found.`);
    return;
  }

  // 2. Instruct Blender to open the newly created project file
  const safeTarget = targetPath.replace(/\\/g, "/");
  const code = `
import bpy
try:
    bpy.ops.wm.open_mainfile(filepath="${safeTarget}")
    print(f"OPEN_NEW_PROJECT_SUCCESS: Opened {safeTarget}")
except Exception as e:
    print(f"OPEN_NEW_PROJECT_ERROR: {e}")
`;

  try {
    const resp = await fetch(`${SERVER_URL}/exec`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const res = await resp.json();
    console.log("[Bun Native] Result:", res.output || res);
  } catch (err: any) {
    console.log("[Bun Native] Server will open file upon autostart.");
  }
}

if (import.meta.main) {
  await createProject();
}
