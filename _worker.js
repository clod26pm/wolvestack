// Cloudflare Pages Worker — Geo-based language redirect
// Free tier: 100,000 requests/day

const COUNTRY_TO_LANG = {
  // Spanish-speaking
  ES: 'es', MX: 'es', AR: 'es', CO: 'es', CL: 'es', PE: 'es', VE: 'es',
  EC: 'es', GT: 'es', CU: 'es', BO: 'es', DO: 'es', HN: 'es', PY: 'es',
  SV: 'es', NI: 'es', CR: 'es', PA: 'es', UY: 'es',
  // Chinese
  CN: 'zh', TW: 'zh', HK: 'zh', MO: 'zh', SG: 'zh',
  // Japanese
  JP: 'ja',
  // Portuguese
  BR: 'pt', PT: 'pt', AO: 'pt', MZ: 'pt',
  // Russian
  RU: 'ru', BY: 'ru', KZ: 'ru', KG: 'ru', UA: 'ru',
  // Italian
  IT: 'it', SM: 'it', VA: 'it',
  // Polish
  PL: 'pl',
  // French
  FR: 'fr', BE: 'fr', CH: 'fr', CA: 'fr', SN: 'fr', CI: 'fr',
  ML: 'fr', BF: 'fr', NE: 'fr', TG: 'fr', BJ: 'fr', CD: 'fr',
  // Indonesian
  ID: 'id', MY: 'id',
  // German
  DE: 'de', AT: 'de',
  // Dutch
  NL: 'nl',
  // Arabic
  SA: 'ar', AE: 'ar', EG: 'ar', IQ: 'ar', MA: 'ar', DZ: 'ar',
  TN: 'ar', LY: 'ar', JO: 'ar', LB: 'ar', KW: 'ar', QA: 'ar',
  BH: 'ar', OM: 'ar', YE: 'ar', SD: 'ar', SY: 'ar',
};

const VALID_LANGS = new Set(['en','es','zh','ja','pt','ru','it','pl','fr','id','de','nl','ar']);

// Known bot user-agents (Google, Bing, etc.)
function isBot(userAgent) {
  if (!userAgent) return false;
  return /googlebot|bingbot|yandex|baiduspider|duckduckbot|slurp|facebot|ia_archiver/i.test(userAgent);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Already has a language prefix — serve normally
    const langMatch = path.match(/^\/(en|es|zh|ja|pt|ru|it|pl|fr|id|de|nl|ar)\//);
    if (langMatch) {
      return env.ASSETS.fetch(request);
    }

    const userAgent = request.headers.get('User-Agent') || '';

    // For bots: serve the root HTML directly (no redirect) so they see hreflang tags
    // This prevents redirect loops and lets Google discover all language versions
    if (isBot(userAgent) && path.endsWith('.html')) {
      return env.ASSETS.fetch(request);
    }
    if (isBot(userAgent) && (path === '/' || path === '/index.html')) {
      return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
    }

    // Human visitors below this point —

    // Check for language preference cookie
    const cookies = request.headers.get('Cookie') || '';
    const langCookie = cookies.match(/wolvestack_lang=(\w{2})/);
    if (langCookie && VALID_LANGS.has(langCookie[1])) {
      return Response.redirect(`${url.origin}/${langCookie[1]}${path}`, 302);
    }

    // Geo-detect from Cloudflare headers
    const country = request.cf?.country || 'US';
    const detectedLang = COUNTRY_TO_LANG[country] || 'en';

    // Root page: redirect to detected language
    if (path === '/' || path === '/index.html') {
      return Response.redirect(`${url.origin}/${detectedLang}/index.html`, 302);
    }

    // HTML page without language prefix: redirect
    if (path.endsWith('.html')) {
      return Response.redirect(`${url.origin}/${detectedLang}${path}`, 302);
    }

    // Static assets (CSS, JS, images): serve from root
    return env.ASSETS.fetch(request);
  }
};
