// 跨源无感续传示例：A 源下到一半，切 B 源继续，客户端不重取已校验块
//
// ★ 为什么这不需要改协议（2026-11-01 实测结论）：
//   契约 V5/V6 要求「每块独立压缩、独立解码」（fzstd backreference 上限 2^25 逼出来的），
//   于是每块都有自己的 sha256、都能单独校验 —— 跨源续传只是把第 N 块换个 base 去取，
//   协议层面零新增字段、零新增判据。
//
// ★ 唯一前提：两个源的 manifest.json **逐字相同**（否则 file 名与 sha 可能对不上）。
//   本脚本第一件事就是断言这条，并把它打出来。
//
// 用法：node tools/multi-source.mjs http://源A http://源B
// 依赖：playwright（chromium）。两个源需允许 CORS（跨源 fetch）。
import { chromium } from 'playwright';
const [,, A, B] = process.argv;
if (!A || !B) { console.error('用法: node multi-source.mjs <源A> <源B>'); process.exit(2); }
const b = await chromium.launch({ executablePath:'/usr/bin/chromium',
  args:['--no-proxy-server','--no-sandbox','--disable-dev-shm-usage'] });
const p = await (await b.newContext()).newPage();
const reqLog = [];
p.on('request', r => reqLog.push(r.url()));

await p.goto(A + '/manifest.json');   // 先建立页面上下文（crypto.subtle 需要 secure context）
const out = await p.evaluate(async ({A, B}) => {
  const log = [];
  const manA = await (await fetch(`${A}/manifest.json`)).json();
  const manB = await (await fetch(`${B}/manifest.json`)).json();
  const sameManifest = JSON.stringify(manA) === JSON.stringify(manB);
  log.push(`manifest A==B: ${sameManifest}`);

  const fz = await import(`${A}/fzstd.mjs`);
  const results = [];

  for (const e of manA.entries) {
    const v = e.variants.find(x => x.codec === 'zstd');
    if (!v) continue;
    const names = v.chunks.map(c => c.file);
    const held = new Array(names.length);        // 已校验块
    const got = new Array(names.length);         // 每块来源

    // ── 阶段 1：只从 A 取前一半（模拟"下到一半"）──
    const half = Math.ceil(names.length / 2);
    for (let i = 0; i < half; i++) {
      const c = v.chunks[i];
      const r = await fetch(`${A}/${c.file}`);    // 普通 GET
      const buf = new Uint8Array(await r.arrayBuffer());
      const h = [...new Uint8Array(await crypto.subtle.digest('SHA-256', buf))]
        .map(x => x.toString(16).padStart(2, '0')).join('');
      if (h !== c.sha256) throw new Error(`A chunk ${i} sha`);
      held[i] = buf; got[i] = 'A';
    }

    // ── 阶段 2：A 断了，切 B 继续；已持有的块不重取 ──
    for (let i = half; i < names.length; i++) {
      const c = v.chunks[i];
      const r = await fetch(`${B}/${c.file}`);    // 同一份 manifest 的同一个 file 名
      const buf = new Uint8Array(await r.arrayBuffer());
      const h = [...new Uint8Array(await crypto.subtle.digest('SHA-256', buf))]
        .map(x => x.toString(16).padStart(2, '0')).join('');
      if (h !== c.sha256) throw new Error(`B chunk ${i} sha`);
      held[i] = buf; got[i] = 'B';
    }

    // ── 阶段 3：解码 + 拼接 + 验 entry.sha256 ──
    const parts = held.map(x => fz.decompress(x));
    const total = parts.reduce((n, x) => n + x.length, 0);
    const all = new Uint8Array(total); let off = 0;
    for (const q of parts) { all.set(q, off); off += q.length; }
    const h = [...new Uint8Array(await crypto.subtle.digest('SHA-256', all))]
      .map(x => x.toString(16).padStart(2, '0')).join('');

    results.push({ name: e.name, ok: h === e.sha256 && total === e.bytes,
                   chunks: names.length, srcA: got.filter(x=>x==='A').length,
                   srcB: got.filter(x=>x==='B').length });
  }
  return { sameManifest, results };
}, {A, B});

console.log(`manifest A==B: ${out.sameManifest}`);
let pass = 0, fail = 0;
for (const r of out.results) {
  if (r.ok) { pass++; console.log(`PASS ${r.name.padEnd(30)} ${String(r.chunks).padStart(2)}块  A取${r.srcA} + B取${r.srcB}`); }
  else { fail++; console.log(`FAIL ${r.name}`); }
}
const fromA = reqLog.filter(u => u.startsWith(A)).length;
const fromB = reqLog.filter(u => u.startsWith(B)).length;
console.log(`\n=== ${pass} PASS / ${fail} FAIL ===`);
console.log(`实际请求：A=${fromA}  B=${fromB}（总计 ${reqLog.length}）`);
await b.close();
process.exit(fail ? 1 : 0);
