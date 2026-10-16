// Render every tracked SVG with Chromium for visual review. Illustrations: one PNG. Animations (SMIL): frames at 10 time points.
// Usage: node render_svgs.js OUT_DIR   (PLAYWRIGHT_MODULE=/path/to/node_modules/playwright if it is not resolvable)
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'); const path = require('path'); const cp = require('child_process');
const REPO = process.env.AUDIT_REPO || path.resolve(__dirname, '..', '..');
const OUT = process.argv[2];
const manifest = JSON.parse(fs.readFileSync(path.join(REPO, 'figma-assets.json'), 'utf8'));
const anim = new Map();
for (const a of manifest.assets) if (a.kind === 'animation') anim.set(a.out.path, a);
const files = cp.execSync('git ls-files "*.svg"', { cwd: REPO }).toString().trim().split('\n');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  let i = 0;
  for (const f of files) {
    i++;
    const abs = path.join(REPO, f);
    const key = f.replace(/\//g, '__').replace(/\.svg$/, '');
    const svg = fs.readFileSync(abs, 'utf8');
    const m = svg.match(/<svg[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"/) || svg.match(/viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"/);
    let w = m ? parseFloat(m[1]) : 1200, h = m ? parseFloat(m[2]) : 800;
    const scale = Math.min(1, 1600 / w);
    const vw = Math.round(w * scale), vh = Math.round(h * scale);
    await page.setViewportSize({ width: vw, height: vh });
    // SVG markup is inlined (an <img src=file://> renders blank); inline also lets SMIL be paused and seeked
    if (anim.has(f)) {
      if (process.env.ONLY_ILLUS) continue;
      if (process.env.ONLY_ANIM && fs.existsSync(path.join(OUT, `${key}__t9.png`))) continue;
      await page.setContent(`<!doctype html><html><body style="margin:0;background:#fff"><div id="w" style="width:${vw}px;height:${vh}px">${svg.replace(/<svg /, `<svg style="width:${vw}px;height:${vh}px" `)}</div></body></html>`);
      const tr = anim.get(f).tracks ? JSON.parse(fs.readFileSync(path.join(REPO, anim.get(f).tracks), 'utf8')) : null;
      let dur = tr && tr.duration ? tr.duration : null;
      if (!dur) { const d = svg.match(/dur="([\d.]+)s"/); dur = d ? parseFloat(d[1]) : 10; }
      const ts = Array.from({length: 10}, (_, k) => k < 9 ? dur * k / 9 : Math.max(0, dur - 0.05));
      for (let k = 0; k < ts.length; k++) {
        await page.evaluate((t) => { const s = document.querySelector('svg'); s.pauseAnimations(); s.setCurrentTime(t); }, ts[k]);
        await page.waitForTimeout(60);
        await page.screenshot({ path: path.join(OUT, `${key}__t${k}.png`), clip: { x: 0, y: 0, width: vw, height: vh } });
      }
      fs.writeFileSync(path.join(OUT, `${key}__meta.txt`), `dur=${dur}\n`);
    } else {
      if (process.env.ONLY_ANIM) continue;
      if (process.env.ONLY_ILLUS && fs.existsSync(path.join(OUT, `${key}.png`)) && fs.statSync(path.join(OUT, `${key}.png`)).size > 20000) continue;
      await page.setContent(`<!doctype html><html><body style="margin:0;background:#fff"><div style="width:${vw}px;height:${vh}px">${svg.replace(/<svg /, `<svg style="width:${vw}px;height:${vh}px" `)}</div></body></html>`);
      await page.waitForTimeout(40);
      await page.screenshot({ path: path.join(OUT, `${key}.png`), clip: { x: 0, y: 0, width: vw, height: vh } });
    }
    if (i % 25 === 0) console.log(i, '/', files.length);
  }
  await browser.close();
  console.log('done', files.length);
})().catch(e => { console.error(e); process.exit(1); });
