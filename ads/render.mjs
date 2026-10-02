#!/usr/bin/env node
/* Frame-steps an ad page and encodes it to MP4.
 * Deterministic: the page's timeline is a pure function of time, so every
 * run of the same input produces the same frames.
 *
 *   node ads/render.mjs --in ads/video/vpn-uk-2026.html --out ads/out/vpn-9x16.mp4
 *   node ads/render.mjs --in ... --out ... --w 1080 --h 1080   # 1:1 variant
 */
import { createRequire } from 'node:module';

// Playwright may be installed globally rather than in this repo; try both.
const require_ = createRequire(import.meta.url);
let chromium;
for (const candidate of [
  'playwright',
  '/opt/node-tools/node_modules/playwright',
  '/opt/node22/lib/node_modules/playwright'
]) {
  try { ({ chromium } = require_(candidate)); break; } catch { /* next */ }
}
if (!chromium) {
  console.error('playwright not found — install it with: npm i -D playwright');
  process.exit(1);
}
import { spawn } from 'node:child_process';
import { mkdtemp, rm, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const arg = (k, d) => {
  const i = argv.indexOf(`--${k}`);
  return i === -1 ? d : argv[i + 1];
};

const input = arg('in');
const output = arg('out');
if (!input || !output) {
  console.error('usage: render.mjs --in <ad.html> --out <out.mp4> [--w 1080] [--h 1920] [--fps 30] [--dur auto] [--quality 92] [--keep-frames]');
  process.exit(1);
}
const W = +arg('w', 1080);
const H = +arg('h', 1920);
const FPS = +arg('fps', 30);
const QUALITY = +arg('quality', 92);
const keepFrames = argv.includes('--keep-frames');

const run = (cmd, args) =>
  new Promise((res, rej) => {
    const p = spawn(cmd, args, { stdio: ['ignore', 'inherit', 'inherit'] });
    p.on('error', rej);
    p.on('close', (code) => (code === 0 ? res() : rej(new Error(`${cmd} exited ${code}`))));
  });

const frameDir = await mkdtemp(path.join(tmpdir(), 'adframes-'));
await mkdir(path.dirname(path.resolve(output)), { recursive: true });

// Offline on purpose: fonts are on disk, so nothing is fetched mid-render.
const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.route(/^https?:\/\//, (route) => route.abort());  // local files only; never fetch mid-render

const url = `${pathToFileURL(path.resolve(input)).href}?render=1&w=${W}&h=${H}`;
await page.goto(url, { waitUntil: 'load' });
await page.waitForFunction(() => document.documentElement.dataset.adReady === '1', null, { timeout: 15000 });

const duration = arg('dur') ? +arg('dur') : await page.evaluate(() => window.AD.duration);
const total = Math.round(duration * FPS);
console.log(`→ ${path.basename(input)}  ${W}x${H} @${FPS}fps  ${duration}s  (${total} frames)`);

for (let i = 0; i < total; i++) {
  const t = i / FPS;
  await page.evaluate((tt) => window.AD.seek(tt), t);
  await page.screenshot({
    path: path.join(frameDir, `f${String(i).padStart(5, '0')}.jpg`),
    type: 'jpeg',
    quality: QUALITY
  });
  if (i % 60 === 0) process.stdout.write(`  ${i}/${total}\r`);
}
await browser.close();

await run('ffmpeg', [
  '-y', '-loglevel', 'error',
  '-framerate', String(FPS),
  '-i', path.join(frameDir, 'f%05d.jpg'),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '20',
  '-pix_fmt', 'yuv420p',
  '-movflags', '+faststart',
  '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
  path.resolve(output)
]);

if (!keepFrames) await rm(frameDir, { recursive: true, force: true });
else console.log(`frames kept in ${frameDir}`);
console.log(`✓ ${output}`);
