// WolveStack Email Capture Popup
// Inject before </body> in all pages
(function() {
  // Don't show if already dismissed or subscribed
  if (localStorage.getItem('ws_popup_dismissed')) return;

  // Wait 30 seconds or 50% scroll before showing
  var shown = false;
  function showPopup() {
    if (shown) return;
    shown = true;
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  // Create overlay
  var overlay = document.createElement('div');
  overlay.id = 'ws-email-overlay';
  overlay.innerHTML = 
    '<div id="ws-email-popup">' +
      '<button id="ws-popup-close" aria-label="Close">&times;</button>' +
      '<div id="ws-popup-icon">🧬</div>' +
      '<h2>Get the Weekly Peptide Research Digest</h2>' +
      '<p>Join 2,000+ researchers and biohackers getting our free weekly breakdown of new peptide studies, protocol updates, and sourcing alerts.</p>' +
      '<form id="ws-email-form">' +
        '<input type="email" id="ws-email-input" placeholder="Your email address" required />' +
        '<button type="submit" id="ws-email-submit" disabled>Subscribe Free</button>' +
      '</form>' +
      '<div id="ws-consent-wrapper">' +
        '<label id="ws-consent-label">' +
          '<input type="checkbox" id="ws-consent-checkbox" />' +
          '<span>I agree to receive emails from WolveStack. No spam, unsubscribe anytime.</span>' +
        '</label>' +
        '<p id="ws-privacy-link"><a href="/en/privacy.html" target="_blank">View our Privacy Policy</a></p>' +
      '</div>' +
      '<p id="ws-email-note">We respect your privacy.</p>' +
      '<div id="ws-popup-success" style="display:none;">' +
        '<div style="font-size:2rem;margin-bottom:12px;">✅</div>' +
        '<h3>You\'re in!</h3>' +
        '<p>Check your inbox for a confirmation. Welcome to the WolveStack community.</p>' +
      '</div>' +
    '</div>';

  // Styles
  var style = document.createElement('style');
  style.textContent = 
    '#ws-email-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;' +
    'background:rgba(0,0,0,0.6);z-index:10000;justify-content:center;align-items:center;' +
    'padding:20px;box-sizing:border-box;backdrop-filter:blur(4px)}' +
    '#ws-email-popup{background:#fff;border-radius:16px;max-width:480px;width:100%;' +
    'padding:40px 32px;text-align:center;position:relative;box-shadow:0 20px 60px rgba(0,0,0,0.3);' +
    'animation:ws-slide-up 0.4s ease}' +
    '@keyframes ws-slide-up{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}' +
    '#ws-popup-close{position:absolute;top:12px;right:16px;background:none;border:none;' +
    'font-size:28px;cursor:pointer;color:#999;line-height:1;padding:4px 8px}' +
    '#ws-popup-close:hover{color:#333}' +
    '#ws-popup-icon{font-size:3rem;margin-bottom:8px}' +
    '#ws-email-popup h2{font-size:1.5rem;margin:0 0 12px;color:#1a1a2e;font-family:system-ui,sans-serif}' +
    '#ws-email-popup p{font-size:0.95rem;color:#555;line-height:1.5;margin:0 0 20px}' +
    '#ws-email-form{display:flex;gap:8px;margin-bottom:12px}' +
    '#ws-email-input{flex:1;padding:14px 16px;border:2px solid #ddd;border-radius:10px;' +
    'font-size:1rem;outline:none;transition:border-color 0.2s}' +
    '#ws-email-input:focus{border-color:#c0392b}' +
    '#ws-email-submit{background:#c0392b;color:#fff;border:none;padding:14px 24px;' +
    'border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer;white-space:nowrap;' +
    'transition:background 0.2s}' +
    '#ws-email-submit:hover:not(:disabled){background:#a93226}' +
    '#ws-email-submit:disabled{background:#ccc;cursor:not-allowed;opacity:0.6}' +
    '#ws-consent-wrapper{margin:16px 0;text-align:left;padding:12px;background:#f9f9f9;border-radius:8px}' +
    '#ws-consent-label{display:flex;align-items:flex-start;gap:8px;font-size:0.9rem;color:#555;cursor:pointer;margin:0}' +
    '#ws-consent-label input[type=checkbox]{margin-top:2px;cursor:pointer;flex-shrink:0}' +
    '#ws-privacy-link{font-size:0.8rem;color:#999;margin:8px 0 0;text-align:center}' +
    '#ws-privacy-link a{color:#c0392b;text-decoration:none}' +
    '#ws-privacy-link a:hover{text-decoration:underline}' +
    '#ws-email-note{font-size:0.8rem;color:#999;margin:0}' +
    '#ws-popup-success h3{color:#1a1a2e;margin:0 0 8px}' +
    '@media(max-width:500px){#ws-email-form{flex-direction:column}' +
    '#ws-email-submit{width:100%}#ws-email-popup{padding:32px 20px}}';

  document.head.appendChild(style);
  document.body.appendChild(overlay);

  // Close handlers
  document.getElementById('ws-popup-close').onclick = function() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
    localStorage.setItem('ws_popup_dismissed', Date.now());
  };
  overlay.onclick = function(e) {
    if (e.target === overlay) {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
      localStorage.setItem('ws_popup_dismissed', Date.now());
    }
  };

  // Checkbox validation — enable/disable submit button
  document.getElementById('ws-consent-checkbox').onchange = function() {
    document.getElementById('ws-email-submit').disabled = !this.checked;
  };

  // Form submission — stores email in localStorage and sends to endpoint if configured
  document.getElementById('ws-email-form').onsubmit = function(e) {
    e.preventDefault();

    // Verify consent checkbox is checked
    if (!document.getElementById('ws-consent-checkbox').checked) {
      alert('Please agree to receive emails before subscribing.');
      return;
    }

    var email = document.getElementById('ws-email-input').value;
    
    // Store locally
    var subs = JSON.parse(localStorage.getItem('ws_subscribers') || '[]');
    subs.push({email: email, date: new Date().toISOString(), page: location.pathname});
    localStorage.setItem('ws_subscribers', JSON.stringify(subs));
    localStorage.setItem('ws_popup_dismissed', 'subscribed');

    // Send to Cloudflare Worker → Resend email with PDF
    // REPLACE YOUR_SUBDOMAIN with your actual Cloudflare Workers subdomain
    var WORKER_URL = 'https://wolvestack-email.clod26.workers.dev';
    fetch(WORKER_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: email, source: 'wolvestack-popup', page: location.pathname})
    }).catch(function(err){ console.error('Email worker error:', err); });

    // Show success
    document.getElementById('ws-email-form').style.display = 'none';
    document.getElementById('ws-email-note').style.display = 'none';
    document.getElementById('ws-popup-success').style.display = 'block';

    setTimeout(function() {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
    }, 3000);
  };

  // Trigger: 30s delay OR 50% scroll
  setTimeout(showPopup, 30000);
  window.addEventListener('scroll', function() {
    var scrollPct = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
    if (scrollPct > 0.5) showPopup();
  });
})();
