#!/usr/bin/env bun

import { join } from "path";

const SERVER_URL = "http://127.0.0.1:8080";
const PY_DIR = join(import.meta.dir, "..", "py");

// Natural durations for each highlight moment
const highlights = [
  {
    title: "Momen 1: Penyerahan & Guray Naik Kuda Kecil",
    startTime: "00:19",
    startFrame: 475,
    endFrame: 1475,
    durationSec: 40, // Natural duration: 40 seconds
  },
  {
    title: "Momen 2: Orang Lari Mutering Guray & Chat Ngasummon Admin",
    startTime: "01:34",
    startFrame: 2350,
    endFrame: 3225,
    durationSec: 35, // Natural duration: 35 seconds
  },
  {
    title: "Momen 3: Kuda Kecil Sprint Lari Kencang di Kegelapan",
    startTime: "02:40",
    startFrame: 4000,
    endFrame: 5000,
    durationSec: 40, // Natural duration: 40 seconds
  }
];

async function sendCode(code: string) {
  const resp = await fetch(`${SERVER_URL}/exec`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  return await resp.json();
}

export async function playFunnyTour() {
  console.log("==================================================");
  console.log("🎬 MEMULAI PLAYBACK DENGAN DURASI ALAMI SPESIFIK...");
  console.log("==================================================\n");

  const playCodeTpl = await Bun.file(join(PY_DIR, "play_range.py")).text();
  const stopCode = await Bun.file(join(PY_DIR, "stop_playback.py")).text();

  for (let i = 0; i < highlights.length; i++) {
    const h = highlights[i];
    console.log(`▶️ [MOMEN ${i + 1}/${highlights.length}] ${h.title}`);
    console.log(`   Start: ${h.startTime} (Frame ${h.startFrame}) | Durasi Alami: ${h.durationSec} detik`);

    const code = playCodeTpl.replace("{START_FRAME}", h.startFrame.toString());
    await sendCode(code);

    await new Promise((r) => setTimeout(r, h.durationSec * 1000));

    await sendCode(stopCode);

    if (i < highlights.length - 1) {
      console.log(`⏸️ JEDA 5 DETIK (Menunggu momen berikutnya...)...\n`);
      await new Promise((r) => setTimeout(r, 5000));
    }
  }

  console.log("\n✨ TOUR SELESAI! Seluruh momen lucu telah diputar sesuai durasi alaminya.");
}

if (import.meta.main) {
  await playFunnyTour();
}
