(function () {
  'use strict';

  var REFERRAL_STORAGE_KEY = 'bantex_referral_v1';
  var ATTRIBUTION_STORAGE_KEY = 'bantex_attribution_v1';
  var SESSION_STORAGE_KEY = 'bantex_session_v1';
  var VALID_REFERRAL = /^[A-Za-z0-9_-]{2,40}$/;
  var CAMPAIGN_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
  var THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;

  function safeValue(value, maxLength) {
    if (typeof value !== 'string') return '';
    var trimmed = value.trim();
    if (!trimmed || trimmed.length > maxLength || /[\u0000-\u001f\u007f]/.test(trimmed)) return '';
    return trimmed;
  }

  function readJson(storage, key) {
    try {
      return JSON.parse(storage.getItem(key) || 'null');
    } catch (error) {
      return null;
    }
  }

  function writeJson(storage, key, value) {
    try {
      storage.setItem(key, JSON.stringify(value));
    } catch (error) {
      return;
    }
  }

  function readReferral() {
    var stored = readJson(window.localStorage, REFERRAL_STORAGE_KEY);
    if (!stored || !VALID_REFERRAL.test(stored.code || '') || stored.expiresAt < Date.now()) {
      try { window.localStorage.removeItem(REFERRAL_STORAGE_KEY); } catch (error) { return ''; }
      return '';
    }
    return stored.code;
  }

  function saveReferral(code) {
    if (!VALID_REFERRAL.test(code)) return;
    writeJson(window.localStorage, REFERRAL_STORAGE_KEY, {
      code: code,
      expiresAt: Date.now() + THIRTY_DAYS
    });
  }

  function readAttribution() {
    var stored = readJson(window.localStorage, ATTRIBUTION_STORAGE_KEY);
    if (!stored || !stored.values || stored.expiresAt < Date.now()) {
      try { window.localStorage.removeItem(ATTRIBUTION_STORAGE_KEY); } catch (error) { return {}; }
      return {};
    }
    return stored.values;
  }

  function saveAttribution(values) {
    if (!Object.keys(values).length) return;
    writeJson(window.localStorage, ATTRIBUTION_STORAGE_KEY, {
      values: values,
      expiresAt: Date.now() + THIRTY_DAYS
    });
  }

  function sessionId() {
    try {
      var current = window.sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (current) return current;
      var generated = window.crypto && typeof window.crypto.randomUUID === 'function'
        ? window.crypto.randomUUID()
        : String(Date.now()) + '-' + Math.random().toString(36).slice(2, 12);
      window.sessionStorage.setItem(SESSION_STORAGE_KEY, generated);
      return generated;
    } catch (error) {
      return '';
    }
  }

  var params = new URLSearchParams(window.location.search);
  var incomingReferral = params.get('ref') || '';
  if (VALID_REFERRAL.test(incomingReferral)) saveReferral(incomingReferral);
  var referralCode = VALID_REFERRAL.test(incomingReferral) ? incomingReferral : readReferral();

  var attribution = readAttribution();
  CAMPAIGN_KEYS.forEach(function (key) {
    var incoming = safeValue(params.get(key) || '', 120);
    if (incoming) attribution[key] = incoming;
  });
  if (referralCode) attribution.ref = referralCode;
  saveAttribution(attribution);

  function isBantexHost(hostname) {
    return hostname === 'bantex.jp' || hostname.endsWith('.bantex.jp');
  }

  function shouldCarryAttribution(link, url) {
    return link.hasAttribute('data-carry-attribution') ||
      link.hasAttribute('data-bantex-service') ||
      isBantexHost(url.hostname);
  }

  if (Object.keys(attribution).length) {
    document.querySelectorAll('a[href]').forEach(function (link) {
      try {
        var url = new URL(link.href, window.location.href);
        if (!/^https?:$/.test(url.protocol) || !shouldCarryAttribution(link, url)) return;
        Object.keys(attribution).forEach(function (key) {
          if (!url.searchParams.has(key)) url.searchParams.set(key, attribution[key]);
        });
        if (referralCode && !url.searchParams.has('utm_source')) {
          url.searchParams.set('utm_source', 'bantex_partner');
          url.searchParams.set('utm_medium', 'referral');
        }
        link.href = url.toString();
      } catch (error) {
        return;
      }
    });
  }

  document.querySelectorAll('[data-ref-code]').forEach(function (element) {
    element.textContent = referralCode || 'なし';
  });

  document.querySelectorAll('a[data-referral-mail]').forEach(function (link) {
    var mailSubject = safeValue(link.getAttribute('data-mail-subject') || '', 100) || 'BANTEXサービス紹介のご相談';
    var subject = encodeURIComponent(mailSubject);
    var source = attribution.utm_source ? '\n流入元: ' + attribution.utm_source : '';
    var body = encodeURIComponent(
      '紹介コード: ' + (referralCode || 'なし') + source + '\n\n' +
      '希望サービス:\n' +
      '会社名・お名前:\n' +
      'ご相談内容:\n'
    );
    link.href = 'mailto:info@bantex.jp?subject=' + subject + '&body=' + body;
  });

  function eventEndpoint() {
    var meta = document.querySelector('meta[name="bantex-event-endpoint"]');
    var raw = safeValue(meta ? meta.content : '', 500);
    if (!raw) return '';
    try {
      var url = new URL(raw, window.location.href);
      return /^https?:$/.test(url.protocol) ? url.toString() : '';
    } catch (error) {
      return '';
    }
  }

  function sendToEndpoint(payload) {
    var endpoint = eventEndpoint();
    if (!endpoint) return;
    var data = JSON.stringify(payload);
    if (navigator.sendBeacon) {
      var sent = navigator.sendBeacon(endpoint, new Blob([data], { type: 'text/plain;charset=UTF-8' }));
      if (sent) return;
    }
    if (window.fetch) {
      window.fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
        body: data,
        keepalive: true,
        credentials: 'omit'
      }).catch(function () { return; });
    }
  }

  var contentId = safeValue(document.body.getAttribute('data-content-id') || '', 100);

  function emitEvent(name, details) {
    var payload = Object.assign({
      event: name,
      event_id: String(Date.now()) + '-' + Math.random().toString(36).slice(2, 9),
      session_id: sessionId(),
      content_id: contentId,
      page_path: window.location.pathname,
      page_title: document.title,
      ref: referralCode || '',
      utm_source: attribution.utm_source || '',
      utm_medium: attribution.utm_medium || '',
      utm_campaign: attribution.utm_campaign || '',
      utm_content: attribution.utm_content || ''
    }, details || {});

    if (typeof window.gtag === 'function') {
      var gtagPayload = Object.assign({}, payload);
      delete gtagPayload.event;
      window.gtag('event', name, gtagPayload);
    } else {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(payload);
    }
    sendToEndpoint(payload);
  }

  function eventNameFor(element, url) {
    var explicitName = safeValue(element.getAttribute('data-track-event') || '', 80);
    if (explicitName) return explicitName;
    var kind = element.getAttribute('data-link-kind') || '';
    if (kind === 'affiliate') return 'affiliate_click';
    if (element.hasAttribute('data-bantex-service') || kind === 'bantex-service') return 'bantex_cta_click';
    if (kind === 'contact') return 'contact_click';
    if (url.protocol === 'mailto:' || url.protocol === 'tel:') return 'contact_click';
    if (/^https?:$/.test(url.protocol) && url.origin !== window.location.origin) return 'outbound_click';
    return 'internal_content_click';
  }

  document.querySelectorAll('[data-track]').forEach(function (element) {
    element.addEventListener('click', function () {
      var url;
      try { url = new URL(element.href || window.location.href, window.location.href); } catch (error) { url = new URL(window.location.href); }
      emitEvent(eventNameFor(element, url), {
        link_label: safeValue(element.getAttribute('data-track') || '', 100),
        link_kind: safeValue(element.getAttribute('data-link-kind') || '', 40),
        program: safeValue(element.getAttribute('data-program') || '', 80),
        destination_host: safeValue(url.hostname || url.protocol.replace(':', ''), 120)
      });
    });
  });

  if (contentId) emitEvent('content_view', { link_label: contentId });

  var header = document.getElementById('site-header');
  function updateHeader() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  document.querySelectorAll('.mobile-nav a').forEach(function (link) {
    link.addEventListener('click', function () {
      var toggle = document.getElementById('nav-toggle');
      if (toggle) toggle.checked = false;
    });
  });
}());
