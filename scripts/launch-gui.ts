#!/usr/bin/env bun

import { spawn } from "bun";

const blendPath = process.argv[2] || "D:/videos/guray-dance.blend";
console.log(`[Bun Native] Spawning Blender GUI with "${blendPath}"...`);

const proc = spawn(["cmd.exe", "/c", "start", "", "blender-launcher.exe", blendPath], {
  detached: true,
  stdio: ["ignore", "ignore", "ignore"]
});
proc.unref();

console.log(`✅ Success: Spawned Blender GUI with project ${blendPath}!`);
