/* WolveStack cookie consent banner — GDPR / UK GDPR / CCPA / LGPD compliant */
(function() {
  if (window.__cookieBannerLoaded) return;
  window.__cookieBannerLoaded = true;

  const KEY = 'wolvestack_cookie_consent_v1';
  const stored = localStorage.getItem(KEY);
  if (stored) {
    // Already decided. If accepted, GA already loaded by main page. Done.
    return;
  }

  const banner = document.createElement('div');
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Cookie consent');
  banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#0f2240;color:#fff;padding:16px 20px;z-index:99999;box-shadow:0 -4px 24px rgba(0,0,0,0.25);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:14px;line-height:1.55;';
  banner.innerHTML = `
    <div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:14px;">
      <div style="flex:1 1 320px;min-width:240px;">
        <strong style="color:#14bdac;">We use cookies</strong> &mdash; strictly-necessary cookies always, and Google Analytics only with your consent. Read our <a href="/en/privacy.html" style="color:#14bdac;text-decoration:underline;">Privacy Policy</a> and <a href="/en/disclaimer.html" style="color:#14bdac;text-decoration:underline;">Disclaimer</a>.
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button id="ws-cookie-decline" style="background:transparent;color:#cbd5e1;border:1px solid #475569;border-radius:6px;padding:8px 16px;cursor:pointer;font-size:13px;font-family:inherit;">Decline non-essential</button>
        <button id="ws-cookie-accept" style="background:#14bdac;color:#0f2240;border:none;border-radius:6px;padding:8px 18px;cursor:pointer;font-weight:700;font-size:13px;font-family:inherit;">Accept all</button>
      </div>
    </div>`;
  document.body.appendChild(banner);

  function decide(value) {
    try { localStorage.setItem(KEY, JSON.stringify({decision: value, timestamp: Date.now()})); } catch (e) {}
    banner.remove();
    if (value === 'accept') {
      // GA was loaded with consent denied; grant it now.
      if (typeof gtag === 'function') {
        gtag('consent', 'update', {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
      }
    }
  }
  document.getElementById('ws-cookie-accept').addEventListener('click', () => decide('accept'));
  document.getElementById('ws-cookie-decline').addEventListener('click', () => decide('decline'));
})();
