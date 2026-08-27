#!/usr/bin/env bun

import { join } from "path";
import { execSync } from "child_process";

export function bringToForeground() {
  const psPath = join(import.meta.dir, "pop-foreground.ps1");
  const sysPowerShell = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";
  
  try {
    console.log("[Bun Native] Popping Blender GUI window to FOREGROUND (Tampil Paling Depan)...");
    const out = execSync(`"${sysPowerShell}" -NoProfile -ExecutionPolicy Bypass -File "${psPath}"`, { encoding: "utf8" });
    console.log("✅ " + (out.trim() || "Brought Blender window to foreground!"));
  } catch (e: any) {
    console.error("Error bringing to foreground:", e.message || e);
  }
}

if (import.meta.main) {
  bringToForeground();
}
