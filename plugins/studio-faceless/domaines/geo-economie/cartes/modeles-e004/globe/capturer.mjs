// Captures du globe de l'épisode 004 par le Chrome sans fenêtre de HyperFrames (puppeteer-core du projet).
// Repris de episodes/episode-003-german-gold/kit/cartes/capturer.mjs (relu le 26/10/2026) : états de la page 004 (alberta au lieu de
// nuit et arcs), aucun crédit à masquer ; le reste est inchangé (attente bornée, 404 comptés, MP4 direct, ancres).
// serve.py doit tourner sur 127.0.0.1:PORT. Node 22 (Git Bash).
//   node capturer.mjs PORT vues SORTIE "v=europe&traces=rideau-de-fer:1&calques=rfa" …   → SORTIE/<n>.png et <n>.json (positions)
//   node capturer.mjs PORT vol VOL.json SORTIE                                          → SORTIE/f0001.png… et ancres.json
//   node capturer.mjs PORT vol VOL.json SORTIE.mp4                                      → MP4 direct (FFmpeg : $FF ou ffmpeg ; H.264 CRF 16, -g 15)
//                                                                                         et SORTIE-ancres.json, sans images sur le disque
// VOL.json : {"vue": "alaska", "fps": 30, "duree": 8,
//             "cles": [{"t": 0, "camera": {center, zoom, pitch, bearing},
//             "traces": {"oleoduc": 0}, "calques": ["alberta"], "points": ["valdez"], "alberta": 0, "voile": 0, "ease": "lineaire"}, …]}
//             (vols.py écrit une clé par image, en « lineaire » : le mouvement est calculé là, d'un seul tenant)
// Entre deux clés : zoom linéaire, centre en Mercator à vitesse d'échelle (la cible reste dans le cadre en zoomant),
// inclinaison, cap, traces et voile interpolés ; adoucissement en cosinus sauf "ease": "lineaire" sur la clé d'arrivée.
import puppeteer from 'puppeteer-core';
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {homedir} from 'node:os';
import {spawn} from 'node:child_process';
import {resolve} from 'node:path';

const [PORT, MODE, ...RESTE] = process.argv.slice(2);
const CHROME = `${homedir()}/.cache/hyperframes/chrome/chrome-headless-shell/win64-152.0.7977.30/chrome-headless-shell-win64/chrome-headless-shell.exe`;
const URL0 = `http://127.0.0.1:${PORT}/carte.html`;

const merc = ([lo, la]) => [(lo + 180) / 360, (1 - Math.log(Math.tan(Math.PI / 4 + la * Math.PI / 360)) / Math.PI) / 2];
const lonlat = ([x, y]) => [x * 360 - 180, (360 / Math.PI) * Math.atan(Math.exp(Math.PI * (1 - 2 * y))) - 90];
const doux = u => (1 - Math.cos(Math.PI * u)) / 2;
function camera(a, b, u) {
  const z = a.zoom + (b.zoom - a.zoom) * u;
  const s = Math.abs(b.zoom - a.zoom) > 0.5 ? (2 ** -z - 2 ** -a.zoom) / (2 ** -b.zoom - 2 ** -a.zoom) : u;
  const [ax, ay] = merc(a.center), [bx, by] = merc(b.center);
  let db = ((b.bearing - a.bearing + 540) % 360) - 180;
  return {center: lonlat([ax + (bx - ax) * s, ay + (by - ay) * s]), zoom: z, pitch: a.pitch + (b.pitch - a.pitch) * u, bearing: a.bearing + db * u};
}
function etatA(vol, t) {
  const C = vol.cles;
  let i = C.findIndex(c => c.t > t); if (i === -1) i = C.length; const a = C[Math.max(0, i - 1)], b = C[Math.min(C.length - 1, i)];
  const u0 = b.t > a.t ? Math.min(1, Math.max(0, (t - a.t) / (b.t - a.t))) : 0, u = b.ease === 'lineaire' ? u0 : doux(u0);
  const traces = {};
  for (const id of new Set([...Object.keys(a.traces || {}), ...Object.keys(b.traces || {})]))
    traces[id] = (a.traces?.[id] ?? 0) + ((b.traces?.[id] ?? a.traces?.[id] ?? 0) - (a.traces?.[id] ?? 0)) * u;
  return {camera: camera(a.camera, b.camera, u), traces, calques: a.calques || [], points: a.points || [],
          voile: (a.voile ?? 0) + ((b.voile ?? a.voile ?? 0) - (a.voile ?? 0)) * u,
          alberta: (a.alberta ?? 0) + ((b.alberta ?? a.alberta ?? 0) - (a.alberta ?? 0)) * u};
}

const browser = await puppeteer.launch({executablePath: CHROME, headless: 'shell', protocolTimeout: 300000,
  args: ['--use-angle=d3d11', '--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--window-size=1920,1080']});
const manquants = new Set();   // tuiles absentes (404) : comptées, listées à la fin, pas une ligne chacune
try {
  const page = await browser.newPage();
  await page.setViewport({width: 1920, height: 1080, deviceScaleFactor: 1});
  page.on('console', m => { if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) console.log('  console:', m.text()); });
  page.on('response', r => { if (r.status() >= 400) manquants.add(new URL(r.url()).pathname); });
  page.on('pageerror', e => console.log('  erreur de page :', e.message));
  const ouvrir = async q => {
    await page.goto(`${URL0}?${q}`, {waitUntil: 'load'});
    await page.waitForFunction('window.__pret === true', {timeout: 180000});
  };
  if (MODE === 'vues') {
    const [SORTIE, ...requetes] = RESTE; mkdirSync(SORTIE, {recursive: true});
    for (const q of requetes) {
      const t0 = Date.now(), nom = new URLSearchParams(q).get('nom') || new URLSearchParams(q).get('v');
      await ouvrir(q); await new Promise(r => setTimeout(r, 300));
      await page.screenshot({path: resolve(SORTIE, `${nom}.png`)});
      writeFileSync(resolve(SORTIE, `${nom}.json`), JSON.stringify(await page.evaluate(() => window.__ancres()), null, 1));
      console.log(`${nom} : ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    }
  } else if (MODE === 'vol') {
    const [FICHIER, SORTIE] = RESTE, vol = JSON.parse(readFileSync(FICHIER, 'utf8'));
    const fps = vol.fps || 30, n = Math.round(vol.duree * fps), ancres = [], mp4 = SORTIE.endsWith('.mp4');
    let ff = null, fin = null;
    if (mp4) {
      ff = spawn(process.env.FF || 'ffmpeg', ['-v', 'error', '-n', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
        '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-g', '15', '-movflags', '+faststart', SORTIE],
        {stdio: ['pipe', 'inherit', 'inherit']});
      fin = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));
    } else mkdirSync(SORTIE, {recursive: true});
    await ouvrir(`v=${vol.vue}`);
    const t0 = Date.now(), instables = [];
    for (let f = 0; f < n; f++) {
      // attente bornée (20 s) : une image dont la carte n'est pas stable est relancée une fois, puis notée et capturée telle quelle
      let stable = await page.evaluate(e => window.__appliquer(e), etatA(vol, f / fps));
      if (!stable) stable = await page.evaluate(() => window.__appliquer({}));
      if (!stable) {
        instables.push(f + 1);
        console.log(`  image ${f + 1} : carte pas stable après 2 × 20 s`, JSON.stringify(await page.evaluate(() => window.__etat())));
        if (instables.length >= 5 && instables.slice(-5)[0] === f - 3) throw new Error('5 images instables de suite : arrêt');
      }
      if (mp4) { const img = await page.screenshot({type: 'png'}); if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once('drain', r)); }
      else await page.screenshot({path: resolve(SORTIE, `f${String(f + 1).padStart(4, '0')}.png`)});
      ancres.push(await page.evaluate(() => window.__ancres()));
      if (f % 30 === 0) console.log(`  image ${f + 1}/${n} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
    if (mp4) { ff.stdin.end(); await fin; }
    writeFileSync(mp4 ? SORTIE.replace(/\.mp4$/, '-ancres.json') : resolve(SORTIE, 'ancres.json'), JSON.stringify({fps, instables, images: ancres}));
    console.log(`${n} images en ${((Date.now() - t0) / 1000).toFixed(0)} s ; instables : ${instables.length ? instables.join(', ') : 'aucune'}`);
  } else console.log('mode : vues ou vol');
} finally {
  if (manquants.size) console.log(`  ${manquants.size} fichiers absents (404), par exemple : ${[...manquants].slice(0, 6).join(' ')}`);
  await browser.close();
}
