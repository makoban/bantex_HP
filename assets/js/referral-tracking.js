(function () {
  'use strict';

  var STORAGE_KEY = 'bantex_referral_v1';
  var VALID_CODE = /^[A-Za-z0-9_-]{2,40}$/;
  var THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;

  function readReferral() {
    try {
      var stored = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || 'null');
      if (!stored || !VALID_CODE.test(stored.code || '') || stored.expiresAt < Date.now()) {
        window.localStorage.removeItem(STORAGE_KEY);
        return '';
      }
      return stored.code;
    } catch (error) {
      return '';
    }
  }

  function saveReferral(code) {
    if (!VALID_CODE.test(code)) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify({
        code: code,
        expiresAt: Date.now() + THIRTY_DAYS
      }));
    } catch (error) {
      return;
    }
  }

  function emitEvent(name, label) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: name,
      link_label: label || '',
      page_path: window.location.pathname
    });
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, {
        link_label: label || '',
        page_path: window.location.pathname
      });
    }
  }

  var params = new URLSearchParams(window.location.search);
  var incomingCode = params.get('ref') || '';
  if (VALID_CODE.test(incomingCode)) saveReferral(incomingCode);
  var referralCode = VALID_CODE.test(incomingCode) ? incomingCode : readReferral();

  if (referralCode) {
    document.querySelectorAll('a[href]').forEach(function (link) {
      try {
        var url = new URL(link.href, window.location.href);
        var isBantexService = link.hasAttribute('data-bantex-service') || url.hostname.endsWith('.bantex.jp');
        if (!isBantexService) return;
        url.searchParams.set('ref', referralCode);
        url.searchParams.set('utm_source', 'bantex_partner');
        url.searchParams.set('utm_medium', 'referral');
        link.href = url.toString();
      } catch (error) {
        return;
      }
    });

    document.querySelectorAll('[data-ref-code]').forEach(function (element) {
      element.textContent = referralCode;
    });

    document.querySelectorAll('a[data-referral-mail]').forEach(function (link) {
      var subject = encodeURIComponent('BANTEXサービス紹介のご相談');
      var body = encodeURIComponent(
        '紹介コード: ' + referralCode + '\n\n' +
        '希望サービス:\n' +
        '会社名・お名前:\n' +
        'ご相談内容:\n'
      );
      link.href = 'mailto:info@bantex.jp?subject=' + subject + '&body=' + body;
    });
  }

  document.querySelectorAll('[data-track]').forEach(function (element) {
    element.addEventListener('click', function () {
      emitEvent('bantex_outbound_click', element.getAttribute('data-track'));
    });
  });

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
