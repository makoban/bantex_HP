import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {test} from 'node:test';

const html = fs.readFileSync(new URL('../boatsim.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x => x[1]);
const source = scripts.find(x => x.includes('const APP_URL'));
const paidURL = 'https://note.com/bnnmkt/n/n000000000001';
const resultURL = 'https://note.com/bnnmkt/n/n000000000002';
const phases = [
  {phase:'prelaunch',from:'20261013',to:'20261013',price:0,note:'free'},
  {phase:'free',from:'20261014',to:'20261014',price:0,note:'free'},
  {phase:'free',from:'20261015',to:'20261103',price:0,note:'free'},
  {phase:'sale',from:'20261104',to:'20270203',price:480,note:'paid'},
  {phase:'sale',from:'20270204',to:null,price:980,note:'paid'},
];
function fixture(time, patch = () => {}) {
  const date = time.slice(0,10).replaceAll('-','');
  const start = Date.parse(time.slice(0,10)+'T00:00:00+09:00');
  const iso = value => new Date(value).toISOString();
  const p = phases.find(p => p.from <= date && (p.to === null || date <= p.to));
  const paid = p.phase === 'sale';
  const ready = paid && Date.parse(time) >= start + 5*3600000;
  const status = {
    version:2, revision:'a'.repeat(40), date, now:time, enabled:true,
    schedule:{contract_version:'boatsim-20261015-v3',list_price:980,planned_price_from:'20270204',sales_stop_from:null,billing_unit:'day',tax_included:true,phases},
    campaign:{...p,note_kind:p.note,currency:'JPY',billing_unit:'day',tax_included:true,list_price:980,sales_stop_from:null},
    access:paid?'code':'open', premium:{ready:true,races:20,generated:time},
    code:{ready,digits:4,ready_from:iso(start+5*3600000),ready_at:ready?iso(start+5*3600000):null,valid_until:iso(start+86400000-1000)},
    note:{url:paid?paidURL:null,kind:paid?'paid':null}, results_note:{url:resultURL,kind:'free'},
    sale:{open:ready,note_url:ready?paidURL:null,price:p.price,currency:'JPY',valid_from:iso(start),valid_until:iso(start+86400000-1000)},
    entry_url:'https://boatsim-app.onrender.com/#daypass',lp_url:'https://bantex.jp/boatsim.html',
  };
  patch(status); return status;
}
async function render(time, patch, unavailable=false) {
  const bySelector = new Map();
  // Build the CTA elements from actual markup so a mislabeled destination is tested.
  for (const match of html.matchAll(/<(a|p|span|strong|small)\b([^>]*\bdata-[^>]*)>([\s\S]*?)<\/\1>/g)) {
    const [,tag,attrs,body] = match;
    const el = {tag, textContent:body.replace(/<[^>]+>/g,''), hidden:/\bhidden\b/.test(attrs),
      href:attrs.match(/href="([^"]+)"/)?.[1],dataset:{},setAttribute(k,v){this[k]=v;}};
    for (const attr of attrs.matchAll(/\b(data-[\w-]+)(?:="[^"]*")?/g)) {
      const selector = '['+attr[1]+']';
      bySelector.set(selector,[...(bySelector.get(selector)||[]),el]);
    }
  }
  const get = selector => {
    if (!bySelector.has(selector)) bySelector.set(selector,[{textContent:'',hidden:false,dataset:{},setAttribute(k,v){this[k]=v;}}]);
    return bySelector.get(selector);
  };
  const document = {body:{dataset:{salesApi:'/status'}},querySelector:s=>get(s)[0],querySelectorAll:get,addEventListener(){}};
  const now = Date.parse(time);
  class Clock extends Date {constructor(...a){super(...(a.length?a:[now]));} static now(){return now;}}
  const status = fixture(time,patch);
  vm.runInNewContext(source,{document,window:{addEventListener(){}},Date:Clock,Intl,URL,AbortController,
    setTimeout(){return 1;},clearTimeout(){},setInterval(){},fetch:async()=>({ok:!unavailable,json:async()=>status})});
  await new Promise(r=>setImmediate(r));
  return {get, state:document.body.dataset.passState};
}

test('static dates, reviewed result population, exclusions and sources stay consistent',()=>{
  const text = html.replace(/<script>[\s\S]*?<\/script>/g,'').replace(/<[^>]+>/g,'');
  assert.match(text,/10月15日〜11月3日の無料体験/);
  assert.doesNotMatch(text,/11月3日までは無料提供中|10月14日〜20日|10\/6〜10\/12|472レース|7,210円|69\.2%/);
  for (const expected of ['10/8〜10/14','489レース','25件的中（5.1%）','外れ464件','48,900円','23,500円','48.1%','532件','33件','予想なし1件','異常1件','567件','2,590円']) assert.ok(text.includes(expected),expected);
  for (const expected of ['github.com/makoban/boatsim-app','b261014.lzh','k261014.lzh','hd=20261014&amp;jcd=20&amp;rno=8']) assert.ok(html.includes(expected),expected);
  assert.equal((html.match(/data-results-cta href=/g)||[]).length,3);
  assert.ok(!html.includes('data-note-cta'));
});
for (const [label,time,price,canBuy] of [
  ['free start','2026-10-15T10:30:00+09:00',0,false],
  ['free last second','2026-11-03T23:59:59+09:00',0,false],
  ['paid before code','2026-11-04T00:00:00+09:00',480,false],
  ['debut ready','2026-11-04T06:10:00+09:00',480,true],
  ['debut last second','2027-02-03T23:59:59+09:00',480,true],
  ['standard ready','2027-02-04T06:10:00+09:00',980,true],
]) test(label+': free results and paid pass keep separate destinations',async()=>{
  const page=await render(time);
  assert.equal(page.state,price?'sale':'free');
  const results=page.get('[data-results-cta]');assert.equal(results.length,3);
  for (const el of results){assert.equal(el.href,resultURL);assert.match(el.textContent,/無料の結果記事/);}
  for (const el of page.get('[data-purchase-cta]')){assert.equal(!el.hidden,canBuy);if(canBuy){assert.equal(el.href,paidURL);assert.match(el.textContent,/1日パスを購入/);}}
  if(canBuy)assert.ok(page.get('[data-card-price]')[0].textContent.includes(String(price)));
});
for (const [label,patch,expectedBuy] of [
  ['no results article',s=>{s.results_note={url:null,kind:null};},true],
  ['wrong results kind',s=>{s.results_note.kind='paid';},true],
  ['same paid/results URL',s=>{s.results_note.url=paidURL;},false],
  ['no premium',s=>{s.premium={ready:false,races:0,generated:null};s.sale.open=false;},false],
  ['stale status',s=>{s.now='2026-11-04T06:00:00+09:00';},false],
  ['old schedule',s=>{s.schedule.list_price=1980;},false],
]) test(label+': no falsely free paid link; availability follows status',async()=>{
  const page=await render('2026-11-04T06:10:00+09:00',patch);
  assert.equal(page.get('[data-purchase-cta]').some(x=>!x.hidden),expectedBuy);
  for(const el of page.get('[data-results-cta]')){
    assert.notEqual(el.href,paidURL);
    if(label!=='no premium')assert.match(decodeURIComponent(el.href),/BoatSim 結果/);
  }
});
test('network failure hides purchase and preserves a free results search',async()=>{
  const page=await render('2026-11-04T06:10:00+09:00',()=>{},true);
  assert.equal(page.state,'unknown');
  assert.ok(page.get('[data-purchase-cta]').every(x=>x.hidden));
  assert.ok(page.get('[data-results-cta]').every(x=>decodeURIComponent(x.href).includes('BoatSim 結果')));
});

// Regression: public worker exposes the free result in its legacy note field too.
test('free results legacy alias remains a direct free link', async()=>{
 const page=await render('2026-10-15T13:46:00+09:00',s=>{s.note={url:resultURL,kind:'free'};});
 assert.equal(page.state,'free');
 for(const el of page.get('[data-results-cta]')) assert.equal(el.href,resultURL);
 assert.ok(page.get('[data-purchase-cta]').every(x=>x.hidden));
});
test('unknown alias kind still fails closed', async()=>{
 const page=await render('2026-10-15T13:46:00+09:00',s=>{s.note={url:resultURL,kind:null};});
 for(const el of page.get('[data-results-cta]')) assert.notEqual(el.href,resultURL);
});
test('verified free phase alias stays direct through the final free second', async()=>{
 const page=await render('2026-11-03T23:59:59+09:00',s=>{s.note={url:resultURL,kind:'free'};});
 assert.equal(page.state,'free');
 assert.equal(page.get('[data-results-cta]').length,3);
 for(const el of page.get('[data-results-cta]')) assert.equal(el.href,resultURL);
 assert.ok(page.get('[data-purchase-cta]').every(x=>x.hidden));
});
test('sale phase rejects a falsely free alias when sale note URL is null', async()=>{
 const page=await render('2026-11-04T06:10:00+09:00',s=>{
  s.note={url:paidURL,kind:'free'};
  s.results_note={url:paidURL,kind:'free'};
  s.sale.note_url=null;
 });
 assert.equal(page.state,'sale');
 assert.equal(page.get('[data-results-cta]').length,3);
 for(const el of page.get('[data-results-cta]')){
  assert.notEqual(el.href,paidURL);
  assert.match(decodeURIComponent(el.href),/BoatSim 結果/);
 }
 assert.ok(page.get('[data-purchase-cta]').every(x=>x.hidden));
});
