/* ============================================================
   BANTEX 粒子ロゴ アドオン (bantex.jp 本番用)
   ------------------------------------------------------------
   ヒーローの「BANTEX」の文字だけを粒子に置き換え、
   カーソルでなぞると散り、クリック(タップ)で弾け、
   自動でスルスルと元の文字に戻ります。

   導入方法:
     1. このファイルをサイトにアップロード (例: /js/bantex-particle-logo.js)
     2. index.html の </body> 直前に1行追加:
        <script src="js/bantex-particle-logo.js" defer></script>

   ・元のテキストはそのまま残す(透明化のみ)ため、SEO・
     アクセシビリティ・コピペへの影響はありません。
   ・prefers-reduced-motion 設定時やCanvas非対応環境では
     何もせず、従来の文字表示のままになります。
   ・依存ライブラリなし。
   ============================================================ */
(function () {
  "use strict";

  // ───── 設定 ─────
  var TARGET_SELECTOR = ".os-hero h1 > span:first-child"; // 「BANTEX」の要素
  var AREA_SELECTOR = ".os-hero";      // マウス反応を拾う範囲
  var ACCENT_COLORS = ["#39d58a", "#20a3ff"]; // サイトの緑/青を少量ミックス
  var ACCENT_RATIO = 0.14;             // アクセント色の割合
  var REPEL_RADIUS = 120;              // カーソルが押しのける半径(px)
  var BURST_RADIUS = 240;              // クリックで弾ける半径(px)
  var SPRING = 0.02;                   // 元の位置に戻る力
  var DAMPING = 0.88;                  // 減衰(小さいほど早く止まる)

  if (window.__bantexParticleLogo) return; // 二重読み込み防止
  window.__bantexParticleLogo = true;

  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var el = document.querySelector(TARGET_SELECTOR);
  if (!el || !el.textContent.trim()) return;

  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext && canvas.getContext("2d");
  if (!ctx) return;

  canvas.setAttribute("aria-hidden", "true");
  canvas.style.position = "absolute";
  canvas.style.pointerEvents = "none";

  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var particles = [];
  var W = 0, H = 0, PAD = 0;
  var mouse = { x: -99999, y: -99999 };
  var running = false;
  var built = false;

  function build() {
    var rect = el.getBoundingClientRect();
    if (rect.width < 10 || rect.height < 10) return; // レイアウト前

    var cs = getComputedStyle(el);
    var fontSize = parseFloat(cs.fontSize);
    PAD = Math.max(90, fontSize * 0.9); // 粒が飛び散る余白

    W = Math.ceil(rect.width + PAD * 2);
    H = Math.ceil(rect.height + PAD * 2);

    // 元テキストの上にキャンバスを重ねる
    if (getComputedStyle(el).position === "static") el.style.position = "relative";
    canvas.style.left = -PAD + "px";
    canvas.style.top = -PAD + "px";
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!canvas.parentNode) el.appendChild(canvas);

    // 元の文字は透明に(レイアウト・SEO・コピペはそのまま)
    el.style.color = "transparent";
    el.style.webkitTextFillColor = "transparent";
    el.style.textShadow = "none";

    // オフスクリーンに同じ書体で文字を描いてピクセルを拾う
    var off = document.createElement("canvas");
    off.width = W; off.height = H;
    var octx = off.getContext("2d");
    octx.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    if ("letterSpacing" in octx && cs.letterSpacing !== "normal") {
      octx.letterSpacing = cs.letterSpacing;
    }
    octx.textAlign = "left";
    octx.textBaseline = "middle";
    octx.fillStyle = "#fff";
    octx.fillText(el.textContent.trim(), PAD, PAD + rect.height / 2 + fontSize * 0.03);

    var baseColor = cs.color === "rgba(0, 0, 0, 0)" || !cs.color ? "#ffffff" : "#ffffff";
    var gap = Math.max(3, Math.round(fontSize / 26));
    var data = octx.getImageData(0, 0, W, H).data;
    particles = [];
    for (var y = 0; y < H; y += gap) {
      for (var x = 0; x < W; x += gap) {
        if (data[(y * W + x) * 4 + 3] > 128) {
          particles.push({
            hx: x, hy: y, x: x, y: y, vx: 0, vy: 0,
            r: gap * (0.34 + Math.random() * 0.2),
            c: Math.random() < ACCENT_RATIO
              ? ACCENT_COLORS[(Math.random() * ACCENT_COLORS.length) | 0]
              : baseColor,
          });
        }
      }
    }
    built = true;
    drawFrame(); // 静止1フレーム(初期表示)
  }

  function drawFrame() {
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      ctx.fillStyle = p.c;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, 6.2832);
      ctx.fill();
    }
  }

  function tick() {
    if (!running) return;
    ctx.clearRect(0, 0, W, H);
    var R = REPEL_RADIUS, R2 = R * R;
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      var dx = p.x - mouse.x, dy = p.y - mouse.y;
      var d2 = dx * dx + dy * dy;
      if (d2 < R2 && d2 > 0.01) {
        var d = Math.sqrt(d2);
        var f = ((R - d) / R) * 3.2;
        p.vx += (dx / d) * f;
        p.vy += (dy / d) * f;
      }
      p.vx += (p.hx - p.x) * SPRING;
      p.vy += (p.hy - p.y) * SPRING;
      p.vx *= DAMPING; p.vy *= DAMPING;
      p.x += p.vx; p.y += p.vy;
      ctx.fillStyle = p.c;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, 6.2832);
      ctx.fill();
    }
    requestAnimationFrame(tick);
  }

  function burst(cx, cy) {
    var R = BURST_RADIUS, R2 = R * R;
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      var dx = p.x - cx, dy = p.y - cy;
      var d2 = dx * dx + dy * dy;
      if (d2 < R2 && d2 > 0.01) {
        var d = Math.sqrt(d2);
        var f = ((R - d) / R) * 26;
        p.vx += (dx / d) * f * (0.5 + Math.random());
        p.vy += (dy / d) * f * (0.5 + Math.random());
      }
    }
  }

  function toCanvas(e) {
    var r = canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }

  function start() {
    build();
    var area = el.closest(AREA_SELECTOR) || el.parentNode;

    area.addEventListener("pointermove", function (e) {
      var p = toCanvas(e);
      mouse.x = p.x; mouse.y = p.y;
    }, { passive: true });

    area.addEventListener("pointerleave", function () {
      mouse.x = -99999; mouse.y = -99999;
    });

    area.addEventListener("pointerdown", function (e) {
      // ボタンやリンクのクリックでは弾けない
      if (e.target.closest("a, button, input, select, textarea")) return;
      var p = toCanvas(e);
      burst(p.x, p.y);
    });

    // 画面内にあるときだけ動かして省電力
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        var was = running;
        running = entries[0].isIntersecting && built;
        if (running && !was) requestAnimationFrame(tick);
      }).observe(area);
    } else {
      running = true;
      requestAnimationFrame(tick);
    }

    // レイアウト確定・ブレークポイント変化・リサイズで組み直し
    if ("ResizeObserver" in window) {
      var rt;
      new ResizeObserver(function () {
        clearTimeout(rt);
        rt = setTimeout(build, 180);
      }).observe(el);
    } else {
      window.addEventListener("resize", function () { build(); });
    }
  }

  // Webフォント(Inter 900)を待ってから粒子化
  function boot() {
    if (document.fonts && document.fonts.load) {
      Promise.race([
        document.fonts.load("900 100px Inter").then(function () { return document.fonts.ready; }),
        new Promise(function (r) { setTimeout(r, 1800); }),
      ]).then(start);
    } else {
      start();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
