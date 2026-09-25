import json, os
H = os.path.dirname(os.path.abspath(__file__))
m = json.load(open('/tmp/parismap.json'))
pins = json.load(open('/tmp/pins.json'))
UNION = m['union']
BLUE, YEL = '#1F6BED', '#F4FF1E'

PIN = '<svg class="pin" viewBox="0 0 48 60" style="left:%.1f%%;top:%.1f%%;width:%.1f%%;transform:translate(-50%%,-100%%) rotate(%ddeg)"><path d="M24 58 C24 58 4 34 4 22 A20 20 0 0 1 44 22 C44 34 24 58 24 58 Z" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/><path d="M16 14 L32 30 M32 14 L16 30" stroke="#000" stroke-width="5" stroke-linecap="round"/></svg>'
pinhtml = ''.join(PIN % (x / 480 * 100, y / 254.8 * 100, s / 480 * 100 * 0.9, r) for x, y, s, r in pins)

FROG = '''<svg viewBox="0 0 120 100" aria-hidden="true"><g fill="currentColor"><circle cx="34" cy="26" r="22"/><circle cx="86" cy="26" r="22"/><path d="M6 46 Q60 14 114 46 L114 66 Q114 96 60 96 Q6 96 6 66 Z"/></g><g fill="#fff"><circle cx="34" cy="26" r="11"/><circle cx="86" cy="26" r="11"/></g><g fill="currentColor"><circle cx="38" cy="28" r="6"/><circle cx="90" cy="28" r="6"/></g><path d="M28 70 Q60 92 92 70" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></svg>'''

CSS = '''
@font-face{font-family:'Anton';src:url(/assets/fonts/Anton-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Nunito';font-weight:400;src:url(/assets/fonts/Nunito-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Nunito';font-weight:700;src:url(/assets/fonts/Nunito-Bold.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Space Mono';font-weight:400;src:url(/assets/fonts/SpaceMono-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Space Mono';font-weight:700;src:url(/assets/fonts/SpaceMono-Bold.woff2) format('woff2');font-display:swap}
:root{--blue:#1F6BED;--yel:#F4FF1E;--ink:#000;--paper:#fff}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:'Nunito',system-ui,sans-serif;color:var(--ink);background:var(--paper);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.display{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;line-height:.95;letter-spacing:.5px;margin:0}
.mono{font-family:'Space Mono',monospace;font-weight:700;letter-spacing:3px;text-transform:uppercase}
.tag{display:inline-block;background:#fff;color:#000;border:3px solid #000;font-family:'Space Mono',monospace;font-weight:700;font-size:13px;letter-spacing:3px;padding:8px 14px 6px;text-transform:uppercase}
.tag.inv{background:#000;color:#fff}
.btn{display:inline-flex;align-items:center;gap:12px;background:#000;color:#fff;text-decoration:none;font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:22px;letter-spacing:1px;padding:16px 26px;border:3px solid #000;box-shadow:6px 6px 0 var(--yel);transition:transform .12s,box-shadow .12s}
.btn:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--yel)}
.btn.light{background:var(--yel);color:#000;box-shadow:6px 6px 0 #000}
.btn.light:hover{box-shadow:8px 8px 0 #000}
.btn svg{width:22px;height:22px}
header{background:var(--blue);border-bottom:4px solid #000}
nav{display:flex;align-items:center;justify-content:space-between;padding:18px 0;gap:20px}
.logo{display:flex;flex-direction:column;align-items:flex-start;text-decoration:none;color:#000;line-height:1}
.logo .k{display:flex;align-items:center;font-family:'Anton',Impact,sans-serif;font-size:40px}
.logo .k svg{width:36px;margin:0 2px}
.logo .h{font-family:'Space Mono',monospace;font-weight:700;font-size:10px;letter-spacing:6px;margin-left:5px;margin-top:2px}
nav ul{display:flex;gap:26px;list-style:none;margin:0;padding:0}
nav ul a{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;letter-spacing:2px;text-transform:uppercase;text-decoration:none}
nav ul a:hover{background:#000;color:var(--yel)}
.hero{background:var(--blue);padding:64px 0 80px;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.mm{display:inline-flex;flex-direction:column;align-items:flex-start}
.mm .m1{background:#000;color:#fff;font-family:'Anton',Impact,sans-serif;font-size:clamp(44px,6vw,84px);line-height:.95;padding:6px 22px 2px;text-transform:uppercase;transform:rotate(-2deg);letter-spacing:1px}
.mm .m2{font-family:'Anton',Impact,sans-serif;font-size:clamp(72px,10vw,140px);line-height:.9;color:var(--yel);-webkit-text-stroke:4px #000;paint-order:stroke fill;text-transform:uppercase;letter-spacing:2px;margin-top:-8px;margin-left:12px}
.tagbox{background:#fff;border:3px solid #000;box-shadow:6px 6px 0 #000;padding:18px 22px;font-family:'Anton',Impact,sans-serif;font-size:clamp(20px,2.4vw,28px);line-height:1.2;text-transform:uppercase;margin:28px 0 22px;max-width:560px;line-height:1.35}
.tagbox mark{background:#000;color:var(--yel);padding:1px 10px 0}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:30px}
.cover{position:relative;justify-self:center;width:min(100%,420px)}
.cover img{border:3px solid #000;box-shadow:14px 14px 0 #000;transform:rotate(3deg)}
.cover .sticker{position:absolute;left:-30px;bottom:40px;background:var(--yel);border:3px solid #000;box-shadow:6px 6px 0 #000;font-family:'Anton',Impact,sans-serif;font-size:22px;text-transform:uppercase;padding:10px 16px;transform:rotate(-8deg)}
section{padding:80px 0}
.eyebrow{display:inline-block;margin-bottom:18px}
.case .tag{align-self:flex-start}
.about h2.display{font-size:clamp(30px,3.4vw,44px)}
h2.display{font-size:clamp(38px,5vw,64px);margin-bottom:24px}
.lead{font-size:20px;font-weight:700;max-width:640px}
.yellow{background:var(--yel)}
.dark{background:#000;color:#fff}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:40px}
.step{background:#fff;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:24px}
.step .n{font-family:'Anton',Impact,sans-serif;font-size:72px;line-height:.9;color:var(--yel);-webkit-text-stroke:3px #000;paint-order:stroke fill}
.step h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:24px;margin:10px 0 8px;line-height:1}
.step p{margin:0;font-weight:700;font-size:15px}
.paris{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.map{position:relative}
.map svg.sil{width:100%;height:auto;overflow:visible}
.map .pin{position:absolute;overflow:visible}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin-top:28px}
.stat{background:#fff;border:3px solid #000;box-shadow:6px 6px 0 #000;padding:16px 20px;min-width:150px}
.stat b{display:block;font-family:'Anton',Impact,sans-serif;font-size:44px;line-height:1}
.stat span{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase}
.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.case{background:var(--yel);color:#000;border:3px solid #000;box-shadow:10px 10px 0 var(--blue);padding:28px;display:flex;flex-direction:column;gap:14px;min-height:320px}
.case h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:32px;line-height:.95;margin:0}
.case p{margin:0;font-weight:700;font-size:16px}
.case .meta{margin-top:auto;font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px}
.pages{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:40px}
.pages img{border:3px solid #000;box-shadow:8px 8px 0 #000;transition:transform .15s}
.pages figure{margin:0}
.pages figcaption{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase;margin-top:14px}
.pages img:hover{transform:rotate(-2deg) scale(1.03)}
.buy{background:var(--blue);text-align:center}
.buy .btns{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.buy small{display:block;margin-top:22px;font-family:'Space Mono',monospace;font-weight:700;font-size:12px;letter-spacing:2px;text-transform:uppercase}
.about{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.about .biglogo .k{font-size:110px}
.about .biglogo .k svg{width:96px}
.about .biglogo .h{font-size:22px;letter-spacing:14px;margin-left:12px}
.coming{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}
.coming span{border:3px solid #000;padding:10px 16px;font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:20px}
.coming span.soon{background:#000;color:#fff}
footer{background:#000;color:#fff;padding:40px 0;font-family:'Space Mono',monospace;font-size:12px;letter-spacing:1px}
footer .wrap{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:center}
footer a{color:#fff}
@media(max-width:900px){.hero .wrap,.paris,.about{grid-template-columns:1fr}.steps,.pages{grid-template-columns:1fr 1fr}.cases{grid-template-columns:1fr}nav ul{display:none}.cover img{transform:none}.cover .sticker{left:8px}}
@media(max-width:560px){.steps,.pages{grid-template-columns:1fr}section{padding:56px 0}}
'''

LOGO = '<a class="logo" href="/" aria-label="Kob House"><span class="k">K%sB</span><span class="h">HOUSE</span></a>' % FROG

AMAZON_JS = '''
// Amazon links: one ASIN, the marketplace follows the visitor's language.
var ASIN = null; // set to the KDP ASIN once the book is live, e.g. "B0XXXXXXXX"
var MARKETS = {fr:"amazon.fr",de:"amazon.de",it:"amazon.it",es:"amazon.es",nl:"amazon.nl",ja:"amazon.co.jp"};
function market(){
  var l=(navigator.language||"en").toLowerCase();
  if(l==="en-gb"||l==="en-ie")return "amazon.co.uk";
  if(l==="en-ca"||l==="fr-ca")return "amazon.ca";
  if(l==="en-au")return "amazon.com.au";
  var k=l.split("-")[0]; return MARKETS[k]||"amazon.com";
}
function amazonUrl(host){
  host=host||market();
  return ASIN?("https://www."+host+"/dp/"+ASIN):("https://www."+host+"/s?k=Murder+Map+Paris+Kob+House");
}
document.querySelectorAll("[data-amazon]").forEach(function(a){
  var h=a.getAttribute("data-amazon"); a.href=amazonUrl(h==="auto"?null:h);
  if(h==="auto"){var s=a.querySelector(".mk"); if(s)s.textContent=market().replace("amazon","Amazon");}
});
'''

CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3h2l2.4 12.5a2 2 0 0 0 2 1.5h8.6a2 2 0 0 0 2-1.5L22 7H6"/><circle cx="10" cy="21" r="1"/><circle cx="18" cy="21" r="1"/></svg>'

def page(title, desc, body, extra_js=''):
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="https://kobhouse.com/assets/cover.png">
<meta property="og:url" content="https://kobhouse.com/">
<meta name="theme-color" content="#1F6BED">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>%s</style>
</head>
<body>
<header><div class="wrap"><nav>%s<ul><li><a href="/#how">How it works</a></li><li><a href="/#paris">Real Paris</a></li><li><a href="/#cases">The cases</a></li><li><a href="/#about">Kob House</a></li><li><a href="/#buy">Buy</a></li></ul></nav></div></header>
%s
<footer><div class="wrap"><div>© 2026 Kob House · Pen-and-paper mysteries with exactly one solution.</div><div><a href="/legal.html">Legal notice</a> · <a href="mailto:contact@kobhouse.com">contact@kobhouse.com</a></div></div></footer>
<script>%s</script>
</body>
</html>
''' % (title, desc, title, desc, CSS, LOGO, body, AMAZON_JS + extra_js)

INDEX = '''
<section class="hero"><div class="wrap">
  <div>
    <div class="mm"><span class="m1">Murder</span><span class="m2">Map</span></div>
    <div class="tagbox">14,400 addresses. Three crime scenes.<br><mark>Cross out the city</mark> until one door is left.</div>
    <div class="tags"><span class="tag">3 cases</span><span class="tag">Real streets</span><span class="tag">6 hours of play</span><span class="tag">One solution</span></div>
    <a class="btn" data-amazon="auto" href="#buy">%s Buy on <span class="mk">Amazon</span></a>
  </div>
  <div class="cover"><img src="/assets/cover.png" width="1000" height="1500" alt="Murder Map: Paris, paperback cover"><div class="sticker">Paperback · Out now</div></div>
</div></section>

<section id="how"><div class="wrap">
  <span class="tag inv eyebrow">How it works</span>
  <h2 class="display">How do you find one door among 14,400 addresses?</h2>
  <p class="lead">Inspector Marchetti has done the legwork: doors knocked, statements taken, notebook filled. What she has not done is put it together. That part is yours. Four steps, one pen, no knowledge of Paris needed.</p>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Read the statement</h3><p>Every witness gives you one fact. None of them lies. Each fact rules out part of the city.</p></div>
    <div class="step"><div class="n">2</div><h3>Strike out arrondissements</h3><p>Hatch the districts the clue eliminates on the printed map of Paris.</p></div>
    <div class="step"><div class="n">3</div><h3>Strike out streets</h3><p>Six real streets per arrondissement. Cross the ones that no longer fit.</p></div>
    <div class="step"><div class="n">4</div><h3>Cross out the numbers</h3><p>Numbers 1 to 120 on every street. Keep going until a single door survives, then check the verification code.</p></div>
  </div>
</div></section>

<section id="paris" class="yellow"><div class="wrap paris">
  <div>
    <span class="tag inv eyebrow">Real streets</span>
    <h2 class="display">The real Paris, door by door.</h2>
    <p class="lead">20 genuine arrondissements with their official boundaries. 120 famous streets, six per arrondissement. 14,400 house numbers to cross out. Every clue is printed on the page: rive gauche or rive droite, along the Seine or by the périphérique, a street named after a saint, a number divisible by seven.</p>
    <div class="stats"><div class="stat"><b>20</b><span>arrondissements</span></div><div class="stat"><b>120</b><span>famous streets</span></div><div class="stat"><b>14,400</b><span>house numbers</span></div></div>
  </div>
  <div class="map"><svg class="sil" viewBox="-10 -10 500 274.8" aria-hidden="true"><path d="%s" fill="#F4FF1E" stroke="#000" stroke-width="16" stroke-linejoin="round"/><path d="%s" fill="#F4FF1E" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><path d="%s" fill="#F4FF1E" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/></svg>%s</div>
</div></section>

<section id="cases" class="dark"><div class="wrap">
  <span class="tag eyebrow">Three cases</span>
  <h2 class="display">Three crime scenes. Three arrondissements. One inspector.</h2>
  <p class="lead">Each case comes with its own printed grid of Paris, so you can mark the book up freely. Sixteen statements per case, about two hours each, and exactly one answer, checked by an independent solver before printing.</p>
  <div class="cases">
    <article class="case"><span class="tag inv">Case 1</span><h3>The Sourdough Martyr</h3><p>A baker with a six-month waiting list, found on a Sunday morning. The bread came out. He did not.</p><div class="meta">16 statements · about 2 hours</div></article>
    <article class="case"><span class="tag inv">Case 2</span><h3>The Influencer Who Fell Off the Map</h3><p>2.3 million followers, one beige apartment, and a Monday with no post.</p><div class="meta">16 statements · about 2 hours</div></article>
    <article class="case"><span class="tag inv">Case 3</span><h3>Last Round at the Wine Bar</h3><p>A founder, a natural wine bar, 140 guests and one missing host.</p><div class="meta">16 statements · about 2 hours</div></article>
  </div>
</div></section>

<section id="inside"><div class="wrap">
  <span class="tag inv eyebrow">Inside the book</span>
  <h2 class="display">156 pages of black, white and ink.</h2>
  <p class="lead">6 × 9 inch paperback, matte cover, white paper made to take a pen. The city is printed three times, once per case.</p>
  <div class="pages">
    <figure><img src="/assets/page-title.png" width="660" height="990" alt="Title page" loading="lazy"><figcaption>Title page</figcaption></figure>
    <figure><img src="/assets/page-rules.png" width="660" height="990" alt="How to play page" loading="lazy"><figcaption>How to play</figcaption></figure>
    <figure><img src="/assets/page-case.png" width="660" height="990" alt="Case opener page" loading="lazy"><figcaption>Case opener</figcaption></figure>
    <figure><img src="/assets/page-statements.png" width="660" height="990" alt="Witness statements page" loading="lazy"><figcaption>Witness statements</figcaption></figure>
  </div>
</div></section>

<section id="buy" class="buy"><div class="wrap">
  <h2 class="display">Get Murder Map: Paris</h2>
  <p class="lead" style="margin:0 auto">Paperback, printed on demand and shipped by Amazon. Pick your store.</p>
  <div class="btns">
    <a class="btn light" data-amazon="amazon.com" href="#">%s Amazon.com</a>
    <a class="btn light" data-amazon="amazon.co.uk" href="#">%s Amazon.co.uk</a>
    <a class="btn light" data-amazon="amazon.fr" href="#">%s Amazon.fr</a>
    <a class="btn light" data-amazon="amazon.de" href="#">%s Amazon.de</a>
  </div>
  <small>Also on Amazon.ca, .com.au, .it, .es, .nl and .co.jp</small>
</div></section>

<section id="about"><div class="wrap about">
  <div><div class="logo biglogo" style="pointer-events:none"><span class="k">K%sB</span><span class="h">HOUSE</span></div></div>
  <div>
    <h2 class="display">Kob House makes puzzle books you solve with a pen, a map, and a suspicious mind.</h2>
    <p class="lead">Every case is generated and then re-solved by an independent solver before it goes to print, which means the logic always holds: one solution, no guessing, no dead ends, no case that falls apart on page forty.</p>
    <p class="lead">The Murder Map series hides a single killer somewhere in a real city and hands you the witness statements, the street grid and about two hours per case.</p>
    <div class="coming"><span>Paris</span><span class="soon">Tokyo · soon</span><span class="soon">New York · soon</span></div>
  </div>
</div></section>
''' % (CART, UNION, UNION, UNION, pinhtml, CART, CART, CART, CART, FROG)

LEGAL = '''
<section><div class="wrap">
  <span class="tag inv eyebrow">Legal notice</span>
  <h2 class="display">Legal notice</h2>
  <p class="lead">kobhouse.com is published by Kob House, an independent publishing imprint registered in France.</p>
  <p><strong>Publisher</strong><br>Kob House<br>Sole proprietorship registered in France · SIRET 892 358 953 00016<br>Contact: <a href="mailto:contact@kobhouse.com">contact@kobhouse.com</a></p>
  <p><strong>Publication director</strong><br>Kob House, reachable at the address above.</p>
  <p><strong>Hosting</strong><br>GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States.</p>
  <p><strong>Personal data and cookies</strong><br>This site sets no cookies, runs no analytics and collects no personal data. Links to Amazon lead to Amazon's own stores, governed by Amazon's terms and privacy policy. Emails sent to contact@kobhouse.com are used only to answer you.</p>
  <p><strong>Intellectual property</strong><br>Murder Map, Kob House, the frog mark, and the texts, puzzles and images on this site are © Kob House. All rights reserved. Map outlines of Paris are derived from open data under the ODbL licence.</p>
  <p><strong>Mentions légales (FR)</strong><br>Éditeur du site : Kob House, entreprise individuelle immatriculée en France, SIRET 892 358 953 00016, contact@kobhouse.com. Directeur de la publication : Kob House. Hébergeur : GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis. Le site ne dépose aucun cookie et ne collecte aucune donnée personnelle.</p>
</div></section>
'''

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><rect width="120" height="120" fill="#1F6BED"/><g transform="translate(6 14) scale(0.9)"><g fill="#000"><circle cx="34" cy="26" r="22"/><circle cx="86" cy="26" r="22"/><path d="M6 46 Q60 14 114 46 L114 66 Q114 96 60 96 Q6 96 6 66 Z"/></g><g fill="#fff"><circle cx="34" cy="26" r="11"/><circle cx="86" cy="26" r="11"/></g><g fill="#000"><circle cx="38" cy="28" r="6"/><circle cx="90" cy="28" r="6"/></g><path d="M28 70 Q60 92 92 70" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></g></svg>'

open(H + '/index.html', 'w').write(page('Murder Map: Paris · Kob House', 'A deduction puzzle book set in the real Paris: 3 murder cases, 14,400 addresses, one killer to find. By Kob House.', INDEX))
open(H + '/legal.html', 'w').write(page('Legal notice · Kob House', 'Legal notice for kobhouse.com.', LEGAL))
open(H + '/assets/favicon.svg', 'w').write(FAVICON)
open(H + '/CNAME', 'w').write('kobhouse.com\n')
open(H + '/.nojekyll', 'w').write('')
open(H + '/robots.txt', 'w').write('User-agent: *\nAllow: /\nSitemap: https://kobhouse.com/sitemap.xml\n')
open(H + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://kobhouse.com/</loc></url><url><loc>https://kobhouse.com/legal.html</loc></url></urlset>\n')
print('ok')
