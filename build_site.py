"""Builds kobhouse.com: a series hub (index.html) and one page per book (paris/, tokyo/, new-york/)."""
import json, os, re, random
H = os.path.dirname(os.path.abspath(__file__))
# Kob House brand (charte A « Dossier »): cream paper, black ink, one red stamp accent. Book pages keep their own duo.
BRAND_BG = '#EFE8D6'
BRAND_ACC = '#D8261C'
D = os.path.join(H, 'data')

FROG = '''<svg viewBox="0 0 120 100" aria-hidden="true"><g fill="currentColor"><circle cx="34" cy="26" r="22"/><circle cx="86" cy="26" r="22"/><path d="M6 46 Q60 14 114 46 L114 66 Q114 96 60 96 Q6 96 6 66 Z"/></g><g fill="#fff"><circle cx="34" cy="26" r="11"/><circle cx="86" cy="26" r="11"/></g><g fill="currentColor"><circle cx="38" cy="28" r="6"/><circle cx="90" cy="28" r="6"/></g><path d="M28 70 Q60 92 92 70" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></svg>'''
CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3h2l2.4 12.5a2 2 0 0 0 2 1.5h8.6a2 2 0 0 0 2-1.5L22 7H6"/><circle cx="10" cy="21" r="1"/><circle cx="18" cy="21" r="1"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7"/></svg>'
PIN = '<svg class="pin" viewBox="0 0 48 60" style="left:%.1f%%;top:%.1f%%;width:%.1f%%;transform:translate(-50%%,-100%%) rotate(%ddeg)"><path d="M24 58 C24 58 4 34 4 22 A20 20 0 0 1 44 22 C44 34 24 58 24 58 Z" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/><path d="M16 14 L32 30 M32 14 L16 30" stroke="#000" stroke-width="5" stroke-linecap="round"/></svg>'

# ------------------------------------------------------------------ books
BOOKS = [
 dict(key='paris', slug='paris', city='Paris', bg='#1F6BED', acc='#F4FF1E', dark_on_acc=True,
      asin='B0HKYJG39P', status='out', pages=156, addresses='14,400', statements='48',
      subtitle='A Deduction Puzzle Book for Adults: 3 Murder Cases, 14,400 Addresses, One Killer to Find',
      unit='arrondissements', unit_n='20', street_n='120', num_word='house numbers',
      hero_tags=['3 cases', 'Real streets', '6 hours of play', 'One solution'],
      how_lead='Inspector Marchetti has done the legwork: doors knocked, statements taken, notebook filled. What she has not done is put it together. That part is yours. Four steps, one pen, no knowledge of Paris needed.',
      steps=[('Read the statement', 'Every witness gives you one fact. None of them lies. Each fact rules out part of the city.'),
             ('Strike out arrondissements', 'Hatch the districts the clue eliminates on the printed map of Paris.'),
             ('Strike out streets', 'Six real streets per arrondissement. Cross the ones that no longer fit.'),
             ('Cross out the numbers', 'Numbers 1 to 120 on every street. Keep going until a single door survives, then check the verification code.')],
      real_title='The real Paris, door by door.',
      real_lead='20 genuine arrondissements with their official boundaries. 120 famous streets, six per arrondissement. 14,400 house numbers to cross out. Every clue is printed on the page: rive gauche or rive droite, along the Seine or by the périphérique, a street named after a saint, a number divisible by seven.',
      stats=[('20', 'arrondissements'), ('120', 'famous streets'), ('14,400', 'house numbers')],
      twist=None,
      cases_title='Three crime scenes. Three arrondissements. One inspector.',
      cases_lead='Each case comes with its own printed grid of Paris, so you can mark the book up freely. Sixteen statements per case, about two hours each, and exactly one answer, checked by an independent solver before printing.',
      cases=[('The Sourdough Martyr', 'A baker with a six-month waiting list, found on a Sunday morning. The bread came out. He did not.', '16 statements'),
             ('The Influencer Who Fell Off the Map', '2.3 million followers, one beige apartment, and a Monday with no post.', '16 statements'),
             ('Last Round at the Wine Bar', 'A founder, a natural wine bar, 140 guests and one missing host.', '16 statements')],
      pages_list=[('page-title', 'Title page'), ('page-rules', 'How to play'), ('page-case', 'Case opener'), ('page-statements', 'Witness statements')],
      card_blurb='Inspector Marchetti retired to Biarritz and left you her notebook. Twenty arrondissements, one killer.'),
 dict(key='tokyo', slug='tokyo', city='Tokyo', bg='#F26A4B', acc='#D9F2E3', dark_on_acc=True,
      asin=None, status='soon', pages=177, addresses='16,560', statements='47',
      subtitle='A Deduction Puzzle Book for Adults: 3 Murder Cases, 16,560 Addresses, One Loop Line to Ride',
      unit='wards', unit_n='23', street_n='138', num_word='block numbers',
      hero_tags=['3 cases', '23 real wards', 'The Yamanote twist', 'One solution'],
      how_lead='Detective Kanzaki found three case files in an unclaimed umbrella at the Lost and Found. Everything in this city has a number: the stations, the wards, the blocks. Four steps, one pen, no knowledge of Tokyo needed.',
      steps=[('Read the statement', 'Every witness gives you one fact. None of them lies. Each fact rules out part of the city.'),
             ('Strike out wards', 'Hatch the wards the clue eliminates, or ride the Yamanote loop and count the stations.'),
             ('Strike out neighbourhoods', 'Six real neighbourhoods per ward, with their kanji. Cross the ones that no longer fit.'),
             ('Cross out the blocks', 'Blocks 1 to 120 in every neighbourhood. Keep going until a single door survives, then check the verification code.')],
      real_title='The real Tokyo, ward by ward.',
      real_lead='23 genuine wards with their official boundaries. 138 real neighbourhoods, six per ward, printed with their kanji. 16,560 block numbers to cross out. Every clue is printed on the page: on the bay or beyond the Sumida, inside the loop or out at the edge of the 23, a block number that is prime.',
      stats=[('23', 'genuine wards'), ('138', 'real neighbourhoods'), ('16,560', 'block numbers')],
      twist=('The Yamanote twist', 'This time, the train is a witness.',
             'The Yamanote loop line circles the city with 30 stations. Witnesses tell you how far someone rode, clockwise or against the clock. Count the stations, cross out the wards they serve, and the loop closes in on the killer. A worked example sits next to the loop of each case.', 'page-twist'),
      cases_title='Three crime scenes. Three wards. One umbrella.',
      cases_lead='Three cases inspired by Japanese ghost stories, each with its own printed city. Fifteen to sixteen statements per case, about two hours each, and exactly one answer, checked by an independent solver before printing.',
      cases=[('The Lantern Bride', 'A lantern maker with a husband, a debt and a jar of face cream. The lanterns went out. So did she.', '16 statements'),
             ('Am I Pretty?', 'A cosmetic surgeon, a woman in a surgical mask, a paper bag of candy on his desk.', '15 statements'),
             ('Platform 31', 'A night track inspector who swore the loop has a thirty-first station, and went to get off there.', '16 statements')],
      pages_list=[('page-case', 'Case opener'), ('page-map', 'The map'), ('page-twist', 'The loop'), ('page-statements', 'Witness statements')],
      card_blurb='Three case files in an unclaimed umbrella. Twenty-three wards, one loop line, and a station that is not on the map.'),
 dict(key='newyork', slug='new-york', city='New York', bg='#FBBA16', acc='#F7F1E1', dark_on_acc=True,
      asin=None, status='soon', pages=185, addresses='17,280', statements='49',
      subtitle='A Deduction Puzzle Book for Adults: 3 Murder Cases, 17,280 Manhattan Addresses, One Grid to Walk',
      unit='neighborhoods', unit_n='24', street_n='144', num_word='house numbers',
      hero_tags=['3 cases', '24 real neighborhoods', 'The grid twist', 'One solution'],
      how_lead='Augustus Pell drew the street atlas that taxi drivers kept under the seat, and pencilled three unsolved cases into his last copy. Nobody in this city walks diagonally. Four steps, one pen, no knowledge of New York needed.',
      steps=[('Read the statement', 'Every witness gives you one fact. None of them lies. Each fact rules out part of the city.'),
             ('Strike out neighborhoods', 'Hatch the neighborhoods the clue eliminates, or count the squares on the grid.'),
             ('Strike out streets', 'Six real streets per neighborhood. Cross the ones that no longer fit.'),
             ('Cross out the numbers', 'Numbers 1 to 120 on every street. Keep going until a single door survives, then check the verification code.')],
      real_title='The real Manhattan, door by door.',
      real_lead='24 genuine neighborhoods, from the Battery to Inwood. 144 real streets, six per neighborhood. 17,280 house numbers to cross out. Every clue is printed on the page: on the Hudson or the East River, downtown or above the park, a street named after a person, a number divisible by four.',
      stats=[('24', 'real neighborhoods'), ('144', 'real streets'), ('17,280', 'house numbers')],
      twist=('The grid twist', 'This time, count the blocks.',
             'Manhattan is drawn the New York way, avenues straight up the page, and cut into squares lettered A to F and numbered 1 to 22. Witnesses tell you how far they walked, up, down or across, never diagonally. Count the squares and strike out everything too near or too far. A worked example sits next to the grid of each case.', 'page-twist'),
      cases_title='Three crime scenes. Three neighborhoods. One atlas.',
      cases_lead='Three cases inspired by New York urban legends, each with its own printed city. Fifteen to seventeen statements per case, about two hours each, and exactly one answer, checked by an independent solver before printing.',
      cases=[('The Alligator King', 'A sewer inspector who swore there was something under Manhattan, and finally had it on film.', '17 statements'),
             ('The Weeping Woman', 'A night nurse who laughed at the legend, until the crying started under her window.', '17 statements'),
             ('The Penny', 'A coin dealer found under a tower, a 1943 copper penny closed in his fist.', '15 statements')],
      pages_list=[('page-case', 'Case opener'), ('page-map', 'The grid'), ('page-twist', 'Walking the grid'), ('page-statements', 'Witness statements')],
      card_blurb='Three cases pencilled into a taxi driver\'s street atlas. Twenty-four neighborhoods, and a grid nobody walks diagonally.'),
]

# ------------------------------------------------------------------ silhouettes
def sil_paris():
    m = json.load(open(D + '/paris_map.json')); pins = json.load(open(D + '/paris_pins.json'))
    U = m['union']
    svg = '<svg class="sil" viewBox="-10 -10 500 274.8" aria-hidden="true"><path d="%s" fill="var(--acc)" stroke="#000" stroke-width="16" stroke-linejoin="round"/><path d="%s" fill="var(--acc)" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><path d="%s" fill="var(--acc)" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/></svg>' % (U, U, U)
    return svg + ''.join(PIN % (x / 480 * 100, y / 254.8 * 100, s / 480 * 100 * 0.9, r) for x, y, s, r in pins)

def sil_city(key):
    S = json.load(open(D + '/%s_shapes.json' % key)); W, Hh = S['W'], S['H']; U = S['outline']
    svg = '<svg class="sil" viewBox="-10 -10 %d %d" aria-hidden="true"><path d="%s" fill="var(--acc)" stroke="#000" stroke-width="16" stroke-linejoin="round"/><path d="%s" fill="var(--acc)" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><path d="%s" fill="var(--acc)" stroke="#000" stroke-width="2.5" stroke-linejoin="round"/></svg>' % (W + 20, Hh + 20, U, U, U)
    rnd = random.Random(3); kept = []
    for dd in sorted(S['districts'].values(), key=lambda d: d['d']):
        pts = [(float(a), float(b)) for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', dd['d'])]
        cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        if any(((cx - a) ** 2 + (cy - b) ** 2) ** 0.5 < 45 for a, b in kept): continue
        kept.append((cx, cy))
    out = svg
    for cx, cy in kept[:14]:
        s = rnd.choice([26, 28, 30, 34])
        out += PIN % ((cx + 10) / (W + 20) * 100, (cy + 10) / (Hh + 20) * 100, s / (W + 20) * 100, rnd.choice([-8, -5, -3, 0, 3, 5, 8]))
    return out

def silhouette(b):
    return sil_paris() if b['key'] == 'paris' else sil_city(b['key'])

# ------------------------------------------------------------------ css
CSS = '''
@font-face{font-family:'Anton';src:url(/assets/fonts/Anton-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Nunito';font-weight:400;src:url(/assets/fonts/Nunito-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Nunito';font-weight:700;src:url(/assets/fonts/Nunito-Bold.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Space Mono';font-weight:400;src:url(/assets/fonts/SpaceMono-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Space Mono';font-weight:700;src:url(/assets/fonts/SpaceMono-Bold.woff2) format('woff2');font-display:swap}
:root{--bg:%s;--acc:%s;--ink:#000;--paper:#fff}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:'Nunito',system-ui,sans-serif;color:var(--ink);background:var(--paper);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%%;height:auto;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.display{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;line-height:.95;letter-spacing:.5px;margin:0}
.mono{font-family:'Space Mono',monospace;font-weight:700;letter-spacing:3px;text-transform:uppercase}
.tag{display:inline-block;background:#fff;color:#000;border:3px solid #000;font-family:'Space Mono',monospace;font-weight:700;font-size:13px;letter-spacing:3px;padding:8px 14px 6px;text-transform:uppercase}
.tag.inv{background:#000;color:#fff}
.btn{display:inline-flex;align-items:center;gap:12px;background:#000;color:#fff;text-decoration:none;font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:22px;letter-spacing:1px;padding:16px 26px;border:3px solid #000;box-shadow:6px 6px 0 var(--acc);transition:transform .12s,box-shadow .12s}
.btn:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--acc)}
.btn.light{background:var(--acc);color:#000;box-shadow:6px 6px 0 #000}
.btn.light:hover{box-shadow:8px 8px 0 #000}
.btn.ghost{background:#fff;color:#000;box-shadow:6px 6px 0 #000}
.btn.ghost:hover{box-shadow:8px 8px 0 #000}
.btn.off{background:#fff;color:#000;box-shadow:none;border-style:dashed;cursor:default;pointer-events:none}
.btn svg{width:22px;height:22px}
header{background:var(--bg);border-bottom:4px solid #000}
nav{display:flex;align-items:center;justify-content:space-between;padding:18px 0;gap:20px}
.logo{display:flex;flex-direction:column;align-items:flex-start;text-decoration:none;color:#000;line-height:1}
.logo .k{display:flex;align-items:center;font-family:'Anton',Impact,sans-serif;font-size:40px}
.logo .k svg{width:36px;margin:0 2px}
.logo .h{font-family:'Space Mono',monospace;font-weight:700;font-size:10px;letter-spacing:6px;margin-left:5px;margin-top:2px}
nav ul{display:flex;gap:22px;list-style:none;margin:0;padding:0}
nav ul a{font-family:'Space Mono',monospace;font-weight:700;font-size:13px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;padding:4px 6px}
nav ul a:hover,nav ul a.on{background:#000;color:var(--acc)}
.hero{background:var(--bg);padding:64px 0 80px;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.mm{display:inline-flex;flex-direction:column;align-items:flex-start}
.mm .m1{background:#000;color:#fff;font-family:'Anton',Impact,sans-serif;font-size:clamp(44px,6vw,84px);line-height:.95;padding:6px 22px 2px;text-transform:uppercase;transform:rotate(-2deg);letter-spacing:1px}
.mm .m2{font-family:'Anton',Impact,sans-serif;font-size:clamp(72px,10vw,140px);line-height:.9;color:var(--acc);-webkit-text-stroke:4px #000;paint-order:stroke fill;text-transform:uppercase;letter-spacing:2px;margin-top:-8px;margin-left:12px}
.citytag{display:inline-block;margin:14px 0 0 14px;background:var(--acc);color:#000;border:3px solid #000;box-shadow:5px 5px 0 #000;font-family:'Space Mono',monospace;font-weight:700;font-size:clamp(16px,2vw,24px);letter-spacing:5px;padding:10px 18px 8px;text-transform:uppercase;transform:rotate(-2deg)}
.tagbox{background:#fff;border:3px solid #000;box-shadow:6px 6px 0 #000;padding:18px 22px;font-family:'Anton',Impact,sans-serif;font-size:clamp(20px,2.4vw,28px);text-transform:uppercase;margin:28px 0 22px;max-width:560px;line-height:1.35}
.tagbox mark{background:#000;color:var(--acc);padding:1px 10px 0}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:30px}
.cover{position:relative;justify-self:center;width:min(100%%,420px)}
.cover img{border:3px solid #000;box-shadow:14px 14px 0 #000;transform:rotate(3deg)}
.cover .sticker{position:absolute;left:-30px;bottom:40px;background:var(--acc);border:3px solid #000;box-shadow:6px 6px 0 #000;font-family:'Anton',Impact,sans-serif;font-size:22px;text-transform:uppercase;padding:10px 16px;transform:rotate(-8deg)}
.fan{position:relative;justify-self:center;width:min(100%%,520px);aspect-ratio:1/1.05}
.fan img{position:absolute;width:52%%;border:3px solid #000;box-shadow:12px 12px 0 #000;background:#fff}
.fan img:nth-child(1){left:0;top:12%%;transform:rotate(-9deg);z-index:1}
.fan img:nth-child(2){left:24%%;top:0;transform:rotate(1deg);z-index:2}
.fan img:nth-child(3){left:48%%;top:14%%;transform:rotate(8deg);z-index:3}
section{padding:80px 0}
.eyebrow{display:inline-block;margin-bottom:18px}
h2.display{font-size:clamp(38px,5vw,64px);margin-bottom:24px}
.about h2.display{font-size:clamp(30px,3.4vw,44px)}
.lead{font-size:20px;font-weight:700;max-width:640px}
.accent{background:var(--acc)}
.tint{background:var(--bg)}
.dark{background:#000;color:#fff}
.paper{background:#fff}
.stamp{display:inline-block;font-family:'Space Mono',monospace;font-weight:700;font-size:12px;letter-spacing:4px;text-transform:uppercase;border:4px solid var(--acc);color:var(--acc);padding:10px 14px;transform:rotate(-6deg);line-height:1.5;margin:0 0 30px 6px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:40px}
.step{background:#fff;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:24px}
.step .n{font-family:'Anton',Impact,sans-serif;font-size:72px;line-height:.9;color:var(--acc);-webkit-text-stroke:3px #000;paint-order:stroke fill}
.step h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:24px;margin:10px 0 8px;line-height:1}
.step p{margin:0;font-weight:700;font-size:15px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.map{position:relative}
.map svg.sil{width:100%%;height:auto;overflow:visible}
.map .pin{position:absolute;overflow:visible}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin-top:28px}
.stat{background:#fff;border:3px solid #000;box-shadow:6px 6px 0 #000;padding:16px 20px;min-width:150px}
.stat b{display:block;font-family:'Anton',Impact,sans-serif;font-size:44px;line-height:1}
.stat span{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase}
.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.case{background:var(--acc);color:#000;border:3px solid #000;box-shadow:10px 10px 0 var(--bg);padding:28px;display:flex;flex-direction:column;gap:14px;min-height:320px}
.case .tag{align-self:flex-start}
.case h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:32px;line-height:.95;margin:0}
.case p{margin:0;font-weight:700;font-size:16px}
.case .meta{margin-top:auto;font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px}
.pages{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:40px}
.pages img{border:3px solid #000;box-shadow:8px 8px 0 #000;transition:transform .15s}
.pages figure{margin:0}
.pages figcaption{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase;margin-top:14px}
.pages img:hover{transform:rotate(-2deg) scale(1.03)}
.twistimg img{border:3px solid #000;box-shadow:12px 12px 0 #000;transform:rotate(-2deg);max-width:420px;margin:0 auto}
.buy{background:var(--bg);text-align:center}
.buy .btns{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.buy small{display:block;margin-top:22px;font-family:'Space Mono',monospace;font-weight:700;font-size:12px;letter-spacing:2px;text-transform:uppercase}
.about{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.about .biglogo .k{font-size:110px}
.about .biglogo .k svg{width:96px}
.about .biglogo .h{font-size:22px;letter-spacing:14px;margin-left:12px}
.books{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:40px}
.book{--bg:%s;--acc:%s;background:var(--bg);border:3px solid #000;box-shadow:10px 10px 0 #000;padding:28px;display:flex;flex-direction:column;gap:16px;text-decoration:none;color:#000;transition:transform .12s}
.book:hover{transform:translate(-3px,-3px)}
.book img{width:70%%;margin:0 auto;border:3px solid #000;box-shadow:8px 8px 0 #000;transform:rotate(2deg)}
.book h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:34px;line-height:.95;margin:14px 0 0}
.book p{margin:0;font-weight:700;font-size:15px}
.book .tag{align-self:flex-start}
.book .meta{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase}
.book .go{margin-top:auto;display:inline-flex;align-items:center;gap:10px;font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:20px;background:#000;color:#fff;padding:12px 18px;align-self:flex-start}
.book .go svg{width:20px;height:20px}
.why{background:#000;color:#fff}
.why .tag{background:#fff;color:#000}
.why .lead{color:#fff}
.whys{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:40px}
.why-card{background:#fff;color:#000;border:3px solid #000;box-shadow:8px 8px 0 var(--acc);padding:24px;display:flex;flex-direction:column;gap:10px}
.why-k{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:3px;text-transform:uppercase;background:#000;color:var(--acc);padding:4px 8px;align-self:flex-start}
.why-card h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:24px;line-height:1;margin:0}
.why-card p{margin:0;font-weight:700;font-size:15px}
.why-foot{margin:36px 0 0;font-size:12px;color:var(--acc)}
.twists{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.twist{background:#fff;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:26px}
.twist h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:26px;line-height:1;margin:12px 0 10px}
.twist p{margin:0;font-weight:700;font-size:15px}
.series{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}
.series a,.series span{border:3px solid #000;padding:10px 16px;font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:20px;text-decoration:none}
.series .soon{background:#000;color:#fff}
.series a:hover{background:var(--acc)}
footer{background:#000;color:#fff;padding:40px 0;font-family:'Space Mono',monospace;font-size:12px;letter-spacing:1px}
footer .wrap{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:center}
footer a{color:#fff}

/* motion: hero entrance, stamp, scroll reveals; all off with prefers-reduced-motion */
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes riseRot{from{opacity:0;transform:translateY(18px) rotate(-2deg)}to{opacity:1;transform:rotate(-2deg)}}
@keyframes stampIn{0%%{opacity:0;transform:scale(1.6) rotate(-6deg)}70%%{opacity:1;transform:scale(.96) rotate(-6deg)}100%%{opacity:1;transform:scale(1) rotate(-6deg)}}
@keyframes fanIn{from{opacity:0;transform:translateY(30px) rotate(0deg)}to{opacity:1}}
@keyframes coverIn{from{opacity:0;transform:translateX(40px) rotate(6deg)}to{opacity:1;transform:rotate(3deg)}}
@keyframes pinDrop{from{opacity:0}to{opacity:1}}
.js .hero .mm{animation:rise .6s cubic-bezier(.2,.8,.2,1) backwards}
.js .hero .citytag{animation:riseRot .6s .15s cubic-bezier(.2,.8,.2,1) backwards}
.js .hero .tagbox{animation:rise .6s .25s cubic-bezier(.2,.8,.2,1) backwards}
.js .hero .tags{animation:rise .6s .35s cubic-bezier(.2,.8,.2,1) backwards}
.js .hero .stamp{animation:stampIn .5s .7s cubic-bezier(.2,.8,.2,1) backwards}
.js .hero .btn{animation:rise .6s .5s cubic-bezier(.2,.8,.2,1) backwards}
.js .fan img:nth-child(1){animation:fanIn .7s .2s cubic-bezier(.2,.8,.2,1) backwards;--r:-9deg}
.js .fan img:nth-child(2){animation:fanIn .7s .35s cubic-bezier(.2,.8,.2,1) backwards;--r:1deg}
.js .fan img:nth-child(3){animation:fanIn .7s .5s cubic-bezier(.2,.8,.2,1) backwards;--r:8deg}
.js .fan img{transform:rotate(var(--r))}
.js .cover img{animation:coverIn .8s .2s cubic-bezier(.2,.8,.2,1) backwards}
.js .cover .sticker{animation:stampIn .5s .9s cubic-bezier(.2,.8,.2,1) backwards;transform:rotate(-8deg)}
.js .map .pin{animation:pinDrop .5s backwards;animation-delay:calc(.06s * var(--i,0))}
.js .rv{opacity:0;transform:translateY(22px);transition:opacity .6s cubic-bezier(.2,.8,.2,1),transform .6s cubic-bezier(.2,.8,.2,1);transition-delay:calc(.08s * var(--i,0))}
.js .rv.in{opacity:1;transform:none}
.js .book.rv.in:hover{transform:translate(-3px,-3px)}
.cover img,.pages img,.twistimg img{transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.cover img:hover{transform:rotate(1deg) scale(1.02)}
.step,.twist,.stat{transition:transform .2s,box-shadow .2s}
.step:hover,.twist:hover{transform:translate(-3px,-3px);box-shadow:11px 11px 0 #000}
.logo .k svg{transition:transform .3s cubic-bezier(.34,1.56,.64,1)}
.logo:hover .k svg{transform:rotate(-12deg) scale(1.15)}
@media(prefers-reduced-motion:reduce){.js .hero *,.js .fan img,.js .cover img,.js .cover .sticker,.js .map .pin{animation:none!important}.js .rv{opacity:1;transform:none;transition:none}*{scroll-behavior:auto!important}}
@media(max-width:900px){.hero .wrap,.two,.about{grid-template-columns:1fr}.steps,.pages,.whys{grid-template-columns:1fr 1fr}.cases,.books,.twists{grid-template-columns:1fr}nav ul{display:none}.cover img{transform:none}.cover .sticker{left:8px}}
@media(max-width:560px){.steps,.pages,.whys{grid-template-columns:1fr}section{padding:56px 0}.fan{width:min(86%%,520px);margin:10px auto 0}.fan img:nth-child(1){left:2%%}.fan img:nth-child(3){left:46%%}}
'''

LOGO = '<a class="logo" href="/" aria-label="Kob House"><span class="k">K%sB</span><span class="h">HOUSE</span></a>' % FROG

MOTION_JS = r'''
// Motion: mark the page as JS-enabled, then reveal cards and sections as they scroll in.
document.documentElement.classList.add("js");
(function(){
  var sel=".book,.step,.twist,.why-card,.case,.stat,.pages figure,#books .lead,#how .lead,#twists .lead,#cases .lead,#inside .lead,#city .lead,.about h2,.about .lead,h2.display,.eyebrow";
  var groups=new WeakMap();
  document.querySelectorAll(sel).forEach(function(el){
    if(el.closest(".hero"))return;
    var g=el.parentElement, n=groups.get(g)||0; groups.set(g,n+1);
    el.style.setProperty("--i",Math.min(n,5)); el.classList.add("rv");
  });
  document.querySelectorAll(".map .pin").forEach(function(p,i){p.style.setProperty("--i",i)});
  if(!("IntersectionObserver" in window)){document.querySelectorAll(".rv").forEach(function(e){e.classList.add("in")});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.1});
  document.querySelectorAll(".rv").forEach(function(e){io.observe(e)});
})();
'''

AMAZON_JS = '''
// Amazon links: one ASIN per book, the marketplace follows the visitor's language.
var MARKETS = {fr:"amazon.fr",de:"amazon.de",it:"amazon.it",es:"amazon.es",nl:"amazon.nl",ja:"amazon.co.jp"};
function market(){
  var l=(navigator.language||"en").toLowerCase();
  if(l==="en-gb"||l==="en-ie")return "amazon.co.uk";
  if(l==="en-ca"||l==="fr-ca")return "amazon.ca";
  if(l==="en-au")return "amazon.com.au";
  var k=l.split("-")[0]; return MARKETS[k]||"amazon.com";
}
function amazonUrl(asin,host,q){
  host=host||market();
  return asin?("https://www."+host+"/dp/"+asin):("https://www."+host+"/s?k="+encodeURIComponent(q));
}
document.querySelectorAll("[data-amazon]").forEach(function(a){
  var h=a.getAttribute("data-amazon"), asin=a.getAttribute("data-asin")||"", q=a.getAttribute("data-q")||"Murder Map Kob House";
  a.href=amazonUrl(asin,h==="auto"?null:h,q);
  if(h==="auto"){var s=a.querySelector(".mk"); if(s)s.textContent=market().replace("amazon","Amazon");}
});
'''

def page(title, desc, body, bg, acc, url, image, nav_items, extra_js=''):
    nav = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="on"' if on else '', t) for h, t, on in nav_items)
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="https://kobhouse.com%s">
<meta property="og:url" content="https://kobhouse.com%s">
<meta name="theme-color" content="%s">
<link rel="canonical" href="https://kobhouse.com%s">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>%s</style>
</head>
<body>
<header><div class="wrap"><nav>%s<ul>%s</ul></nav></div></header>
%s
<footer><div class="wrap"><div>© 2026 Kob House · Pen-and-paper mysteries with exactly one solution.</div><div><a href="/legal.html">Legal notice</a> · <a href="mailto:contact@kobhouse.com">contact@kobhouse.com</a></div></div></footer>
<script>%s</script>
</body>
</html>
''' % (title, desc, title, desc, image, url, bg, url, (CSS % (bg, acc, bg, acc)) + MM_CSS, LOGO, nav, body, AMAZON_JS + MOTION_JS + extra_js)


WHY_HTML = '''
<section id="why" class="why"><div class="wrap">
  <span class="tag inv eyebrow">Why it works</span>
  <h2 class="display">The slow puzzle.</h2>
  <p class="lead">You'll know the rules in two minutes. You'll need about two hours per case. That is the point: one pen, one city, one thing on your mind.</p>
  <div class="whys">
    <div class="why-card"><span class="why-k">Calm</span><h3>Calm is a method</h3><p>A clear task, a simple gesture, progress you can see. Cross out the city one line at a time and let the rest of the day wait.</p></div>
    <div class="why-card"><span class="why-k">Focus</span><h3>Two hours where your phone doesn't exist</h3><p>Paper, pen, sixteen statements. Nothing to swipe, nothing to check, nothing to charge.</p></div>
    <div class="why-card"><span class="why-k">Finish</span><h3>You don't guess the ending, you earn it</h3><p>Every hatched district and every crossed-out number is work you did. When one door is left, the code at the back confirms it.</p></div>
    <div class="why-card"><span class="why-k">Fair</span><h3>Hard, never unfair</h3><p>Every witness tells the truth. Every case has exactly one solution, checked by an independent solver before printing. No trick questions.</p></div>
  </div>
  <p class="why-foot mono">A case for a rainy Sunday · a long flight · a quiet evening</p>
</div></section>
'''

HUB_NAV = [('/#murder-map', 'Murder Map', False), ('/#how', 'How it works', False), ('/#murder-mate', 'Murder Mate', False), ('/#about', 'Kob House', False)]

def book_nav(b):
    items = [('/#books', 'All books', False), ('#how', 'How it works', False)]
    if b['twist']: items.append(('#twist', 'The twist', False))
    items += [('#why', 'Why it works', False), ('#city', 'Real %s' % b['city'], False), ('#cases', 'The cases', False), ('#buy', 'Buy', False)]
    return items

def buy_buttons(b, cls='light'):
    if b['status'] != 'out':
        return '<span class="btn off">Coming soon on Amazon</span>'
    q = 'Murder Map %s Kob House' % b['city']
    return ''.join('<a class="btn %s" data-amazon="%s" data-asin="%s" data-q="%s" href="#">%s %s</a>' % (cls, h, b['asin'] or '', q, CART, h.replace('amazon', 'Amazon')) for h in ('amazon.com', 'amazon.co.uk', 'amazon.fr', 'amazon.de'))

def hero_cta(b):
    if b['status'] == 'out':
        return '<a class="btn" data-amazon="auto" data-asin="%s" data-q="Murder Map %s Kob House" href="#buy">%s Buy on <span class="mk">Amazon</span></a>' % (b['asin'] or '', b['city'], CART)
    return '<span class="btn off">Coming soon on Amazon</span>'

# ------------------------------------------------------------------ book page
def book_page(b):
    A = '/assets/%s/' % b['key']
    sticker = 'Paperback · Out now' if b['status'] == 'out' else 'Paperback · Coming soon'
    twist_html = ''
    if b['twist']:
        tag, title, body, img = b['twist']
        twist_html = '''
<section id="twist" class="accent"><div class="wrap two">
  <div><span class="tag inv eyebrow">%s</span><h2 class="display">%s</h2><p class="lead">%s</p><p class="lead">Every Murder Map book has one twist, taken from something real about its city. Same rules, same pen, a different way to close in.</p></div>
  <div class="twistimg"><img src="%s%s.png" width="660" height="990" alt="%s page" loading="lazy"></div>
</div></section>''' % (tag, title, body, A, img, title)
    steps = ''.join('<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>' % (i, t, p) for i, (t, p) in enumerate(b['steps'], 1))
    stats = ''.join('<div class="stat"><b>%s</b><span>%s</span></div>' % s for s in b['stats'])
    cases = ''.join('<article class="case"><span class="tag inv">Case %d</span><h3>%s</h3><p>%s</p><div class="meta">%s · about 2 hours</div></article>' % (i, t, p, m) for i, (t, p, m) in enumerate(b['cases'], 1))
    pages = ''.join('<figure><img src="%s%s.png" width="660" height="990" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (A, f, c, c) for f, c in b['pages_list'])
    others = [o for o in BOOKS if o['key'] != b['key']]
    series = ''.join(('<a href="/%s/">%s</a>' if o['status'] == 'out' else '<a class="soon" href="/%s/">%s · soon</a>') % (o['slug'], o['city']) for o in others)
    body = '''
<section class="hero"><div class="wrap">
  <div>
    <div class="mm"><span class="m1">Murder</span><span class="m2">Map</span></div><br><span class="citytag">%s</span>
    <div class="tagbox">%s addresses. Three crime scenes.<br><mark>Cross out the city</mark> until one door is left.</div>
    <div class="tags">%s</div>
    %s
  </div>
  <div class="cover"><img src="%scover.png" width="1000" height="1500" alt="Murder Map: %s, paperback cover"><div class="sticker">%s</div></div>
</div></section>

<section id="how"><div class="wrap">
  <span class="tag inv eyebrow">How it works</span>
  <h2 class="display">How do you find one door among %s addresses?</h2>
  <p class="lead">%s</p>
  <div class="steps">%s</div>
</div></section>
%s
%s
<section id="city" class="tint"><div class="wrap two">
  <div>
    <span class="tag inv eyebrow">Real streets</span>
    <h2 class="display">%s</h2>
    <p class="lead">%s</p>
    <div class="stats">%s</div>
  </div>
  <div class="map">%s</div>
</div></section>

<section id="cases" class="dark"><div class="wrap">
  <span class="tag eyebrow">Three cases</span>
  <h2 class="display">%s</h2>
  <p class="lead">%s</p>
  <div class="cases">%s</div>
</div></section>

<section id="inside"><div class="wrap">
  <span class="tag inv eyebrow">Inside the book</span>
  <h2 class="display">%d pages of black, white and ink.</h2>
  <p class="lead">6 × 9 inch paperback, matte cover, white paper made to take a pen. The city is printed three times, once per case.</p>
  <div class="pages">%s</div>
</div></section>

<section id="buy" class="buy"><div class="wrap">
  <h2 class="display">Get Murder Map: %s</h2>
  <p class="lead" style="margin:0 auto">%s</p>
  <div class="btns">%s</div>
  <small>%s</small>
</div></section>

<section id="about"><div class="wrap about">
  <div><div class="logo biglogo" style="pointer-events:none"><span class="k">K%sB</span><span class="h">HOUSE</span></div></div>
  <div>
    <h2 class="display">Kob House makes puzzle books you solve with a pen, a map, and a suspicious mind.</h2>
    <p class="lead">Every case is generated and then re-solved by an independent solver before it goes to print, which means the logic always holds: one solution, no guessing, no dead ends, no case that falls apart on page forty.</p>
    <p class="lead">Also in the Murder Map series:</p>
    <div class="series">%s</div>
  </div>
</div></section>
''' % (b['city'], b['addresses'], ''.join('<span class="tag">%s</span>' % t for t in b['hero_tags']), hero_cta(b), A, b['city'], sticker,
       b['addresses'], b['how_lead'], steps, twist_html, WHY_HTML,
       b['real_title'], b['real_lead'], stats, silhouette(b),
       b['cases_title'], b['cases_lead'], cases, b['pages'], pages,
       b['city'], 'Paperback, printed on demand and shipped by Amazon. Pick your store.' if b['status'] == 'out' else 'The paperback is on its way to Amazon. Check back in a few days, or follow Kob House on Instagram.',
       buy_buttons(b), 'Also on Amazon.ca, .com.au, .it, .es, .nl and .co.jp' if b['status'] == 'out' else 'Same format as the other books: 6 × 9 inch paperback, printed on demand.',
       FROG, series)
    return page('Murder Map: %s · Kob House' % b['city'], 'A deduction puzzle book set in the real %s: 3 murder cases, %s addresses, one killer to find. By Kob House.' % (b['city'], b['addresses']),
                body, b['bg'], b['acc'], '/%s/' % b['slug'], A + 'cover.png', book_nav(b))

# ------------------------------------------------------------------ hub
# ------------------------------------------------------------------ Murder Mate (next collection, coming soon)
MM_BG, MM_ACC, MM_SHADE = '#0F7B5F', '#CDB8F5', '#0B5A45'
MURDER_MATE_HUB = """
<section id="murder-mate" style="background:#0F7B5F;border-top:4px solid #000;border-bottom:4px solid #000;color:#fff"><div class="wrap mmhub">
  <div class="mmcov"><a href="/murder-mate/"><img src="/assets/murdermate/cover-sm.png" width="400" height="600" alt="Murder Mate: India cover" loading="lazy"></a></div>
  <div>
    <span class="tag eyebrow">Murder Mate: India · October 2026</span>
    <h2 class="display" style="color:#fff">Murder Mate. <span style="color:#CDB8F5">The weapon is a checkmate.</span></h2>
    <p class="lead" style="color:#fff">Chess murder mysteries. The board is the crime scene, the black king is the victim, every white piece is a suspect. Several of them could have delivered mate. The witnesses say only one did.</p>
    <div class="tags"><span class="tag">40 cases</span><span class="tag">Mate in 1 to 3</span><span class="tag">4 levels</span><span class="tag">A QR board on every case</span></div>
    <div class="mmcta"><a class="btn" href="/murder-mate/">%s Discover Murder Mate</a><a class="btn ghost" href="/mm/1/01/">Play the board of case 01</a></div>
  </div>
</div></section>
""" % ARROW

MM_CSS = """
.spread{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:36px;border:3px solid #000;box-shadow:12px 12px 0 #000;background:#fff}
.spread .pg{position:relative}.spread .pg:first-child{border-right:2px solid #ddd}
.spread img{width:100%;height:auto;display:block}
.spread i{position:absolute;font-style:normal;width:34px;height:34px;border-radius:50%;background:#0F7B5F;color:#fff;border:3px solid #000;display:flex;align-items:center;justify-content:center;font-family:'Anton',Impact,sans-serif;font-size:18px;transform:translate(-50%,-50%)}
.anat{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:40px}
.anat div{border:3px solid #000;padding:16px;background:#fff;position:relative}
.anat b{position:absolute;top:-17px;left:14px;width:34px;height:34px;border-radius:50%;background:#0F7B5F;color:#fff;border:3px solid #000;display:flex;align-items:center;justify-content:center;font-family:'Anton',Impact,sans-serif;font-size:18px;font-weight:400}
.anat h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:21px;margin:10px 0 6px;line-height:1}
.anat p{margin:0;font-size:14px;font-weight:700}
.rules3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:32px}
.rule{background:#CDB8F5;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:20px;color:#000}
.rule h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:24px;margin:0 0 10px;line-height:1}
.rule p{margin:0;font-weight:700;font-size:15px}
.look{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:34px}
.look figure{margin:0}.look img{border:3px solid #000;box-shadow:8px 8px 0 #000;background:#fff;width:100%;height:auto}
.look figcaption{margin-top:14px;font-weight:700;font-size:14px}
@media(max-width:860px){.spread{grid-template-columns:1fr}.spread .pg:first-child{border-right:0;border-bottom:2px solid #ddd}.anat,.rules3{grid-template-columns:1fr 1fr}.look{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.anat,.rules3{grid-template-columns:1fr}}

.khtitle{font-size:clamp(46px,6.4vw,92px);margin:4px 0 18px;color:#000}
.collections{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:26px}
.coll{display:flex;flex-direction:column;gap:8px;background:var(--c);color:#fff;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:18px;text-decoration:none;transition:transform .12s}
.coll:hover{transform:translate(-2px,-2px)}
.coll .mono{font-size:11px;color:var(--a)}
.coll b{font-family:'Anton',Impact,sans-serif;font-size:32px;text-transform:uppercase;line-height:1;font-weight:400}
.coll>span:not(.mono):not(.tag){font-weight:700;font-size:15px}
.coll .tag{align-self:flex-start;margin-top:4px}
.colband{background:var(--c);color:#fff;border-top:4px solid #000;border-bottom:4px solid #000;padding:34px 0 30px}
.colband .wrap{display:flex;align-items:center;gap:28px;flex-wrap:wrap}
.colband .mono{font-family:'Space Mono',monospace;font-weight:700;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--a);flex-basis:100%;margin-bottom:-12px}
.colband p{margin:0;font-weight:700;font-size:19px;max-width:420px}
.colband .mm .m1{font-size:44px}
.colband .mm .m2{font-size:72px;color:var(--a)}
.mmate{font-family:'Anton',Impact,sans-serif;font-size:72px;line-height:.9;text-transform:uppercase}
.mmate .l{color:var(--a)}
@media(max-width:860px){.collections{grid-template-columns:1fr}.colband .mm .m2,.mmate{font-size:56px}}

.mmhub{display:grid;grid-template-columns:320px 1fr;gap:56px;align-items:center}
.mmcov img{border:3px solid #000;box-shadow:12px 12px 0 #000;transform:rotate(-2deg)}
.mmcta{display:flex;flex-wrap:wrap;gap:16px;margin-top:28px}
.mmlevels{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:36px}
.mmlevel{background:#CDB8F5;color:#000;border:3px solid #000;box-shadow:8px 8px 0 #000;padding:20px}
.mmlevel .k{font-size:26px;letter-spacing:2px;font-family:'DejaVu Sans','Segoe UI Symbol',sans-serif}
.mmlevel h3{font-family:'Anton',Impact,sans-serif;text-transform:uppercase;font-size:26px;margin:8px 0 6px;line-height:1}
.mmlevel p{margin:0;font-weight:700;font-size:14px}
.mmlevel .mono{font-size:11px;margin-top:10px;display:block}
.mmseries{display:grid;grid-template-columns:repeat(4,1fr);gap:28px 22px;margin-top:36px}
.mmvol{margin:0}.mmvol img{width:100%;height:auto;border:3px solid #000;box-shadow:8px 8px 0 #000;display:block}
.mmvol figcaption{margin-top:14px;display:flex;flex-direction:column;gap:3px}
.mmvol b{font-family:'Anton',Impact,sans-serif;font-size:24px;text-transform:uppercase;line-height:1;font-weight:400}
.mmvol span{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase}
.mmvol em{font-style:normal;font-weight:700;font-size:15px}
.mmvol .when{color:#CDB8F5}
.mmc{border:3px solid #000;padding:14px 16px;color:#fff;box-shadow:6px 6px 0 #000}
.mmc b{font-family:'Anton',Impact,sans-serif;font-size:24px;text-transform:uppercase;display:block;line-height:1}
.mmc span{font-family:'Space Mono',monospace;font-weight:700;font-size:11px;letter-spacing:2px;text-transform:uppercase}
@media(max-width:860px){.mmhub{grid-template-columns:1fr;gap:32px}.mmcov{max-width:260px}.mmlevels,.mmseries{grid-template-columns:1fr 1fr}}
"""

def murder_mate_page():
    levels = [(1, 'Rookie', 'Mate in one. Anyone who knows how the pieces move.', 'Cases 01-08 · 5-10 min'),
              (2, 'Detective', 'Mate in two, and the obvious check is usually a trap.', 'Cases 09-20 · 15-30 min'),
              (3, 'Chief Inspector', 'Five suspects on a busy board, and one witness is lying.', 'Cases 21-33 · 30-40 min'),
              (4, 'Commissioner', 'Mate in three. One liar. Trust nobody, least of all the Maharani.', 'Cases 34-40 · 30-45 min')]
    lv = ''.join('<div class="mmlevel"><div class="k">%s</div><h3>%s</h3><p>%s</p><span class="mono">%s</span></div>' % ('&#x265A;&#xFE0E;' * n, t, d, m) for n, t, d, m in levels)
    series = [('india', 'India', 'Udaipur · 1932', 'The weapon is the mate', 'October 2026'),
              ('uzbekistan', 'Uzbekistan', 'Samarkand · 1403', 'Promotion: the impostor pawn', 'Early 2027'),
              ('persia', 'Persia', 'Isfahan · 1611', 'Discovered check: the accomplice', '2027'),
              ('spain', 'Spain', 'Toledo · 1283', 'Castling: the perfect alibi', 'To be announced'),
              ('russia', 'Russia', 'Moscow · 1956', 'En passant: just passing by', 'To be announced'),
              ('iceland', 'Iceland', 'Reykjavik · 1972', 'Stalemate: the accident', 'To be announced'),
              ('scotland', 'Scotland', 'Isle of Lewis · 1150', "Underpromotion: the knight's choice", 'To be announced'),
              ('cuba', 'Cuba', 'Havana · 1921', 'Endgames: the king runs', 'To be announced')]
    se = ''.join('<figure class="mmvol"><img src="/assets/murdermate/covers/%s-sm.png" width="400" height="600" alt="Murder Mate: %s cover" loading="lazy"><figcaption><b>%s</b><span>%s</span><em>%s</em><span class="when">%s</span></figcaption></figure>' % (k, n, n, c, t, w) for k, n, c, t, w in series)
    body = """
<section class="hero" style="background:#0F7B5F;color:#fff"><div class="wrap mmhub">
  <div class="mmcov"><img src="/assets/murdermate/cover.png" width="1000" height="1500" alt="Murder Mate: India cover"></div>
  <div>
    <span class="tag">Coming soon · October 2026</span>
    <h1 class="display" style="color:#fff;font-size:clamp(48px,8vw,96px);margin:18px 0 10px">Murder Mate: <span style="color:#CDB8F5">India</span></h1>
    <p class="lead" style="color:#fff">Udaipur, 1932. The monsoon has cut the palace off from the world, the telephone line is down, and guests keep dying at a rate of roughly one per evening. Inspector Rao of the Bombay police was only supposed to stay for the weekend.</p>
    <div class="tags"><span class="tag">40 cases</span><span class="tag">From your first mate to 1800+</span><span class="tag">Full solutions</span><span class="tag">Any board or app</span></div>
    <div class="mmcta"><a class="btn ghost" href="/mm/1/01/">Play the board of case 01</a></div>
  </div>
</div></section>

<section id="how" class="paper"><div class="wrap">
  <span class="tag inv eyebrow">How it works</span>
  <h2 class="display">The board is the palace. The black king is the victim.</h2>
  <p class="lead">Every case is a real chess position, and every square belongs to a room of the palace. The white pieces are the guests, and all of them had a reason.</p>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Set up the board</h3><p>On a real chessboard, or scan the QR code on the case: the position opens on your phone, ready to play, with no engine.</p></div>
    <div class="step"><div class="n">2</div><h3>Find every mate</h3><p>Only one white piece moves, whatever Black tries. Several suspects can still pull it off. List them all.</p></div>
    <div class="step"><div class="n">3</div><h3>Read the witnesses</h3><p>The cook, the butler and the palace clockmaker saw who went where. From Chief Inspector on, one of them is lying.</p></div>
    <div class="step"><div class="n">4</div><h3>Name the killer</h3><p>Who gave mate, in which room, and how. Exactly one answer per case, checked by an independent solver before printing.</p></div>
  </div>
</div></section>


<section id="inside" class="paper"><div class="wrap">
  <span class="tag inv eyebrow">Anatomy of a case</span>
  <h2 class="display">Two pages, one murder.</h2>
  <p class="lead">Every case fills a double page: the crime on the left, the suspects and the witnesses on the right. Here is case 01, the first and easiest of the forty.</p>
  <div class="spread">
    <div class="pg"><img src="/assets/murdermate/page-case-left.png" width="800" height="1200" alt="Case 01, left page: story and board" loading="lazy">
      <i style="left:3%%;top:5%%">1</i><i style="left:3%%;top:18%%">2</i><i style="left:3%%;top:39%%">3</i><i style="left:86%%;top:86%%">4</i></div>
    <div class="pg"><img src="/assets/murdermate/page-case-right.png" width="800" height="1200" alt="Case 01, right page: suspects, testimonies and verdict" loading="lazy">
      <i style="left:3%%;top:5%%">5</i><i style="left:3%%;top:37%%">6</i><i style="left:3%%;top:76%%">7</i></div>
  </div>
  <div class="anat">
    <div><b>1</b><h3>The case file</h3><p>Case number, level, how many moves the killer needs, and a rough thinking time.</p></div>
    <div><b>2</b><h3>The victim</h3><p>A short story: who died, and why half the palace wanted them to. Then who stood around the victim, which is to say the black pieces.</p></div>
    <div><b>3</b><h3>The board is the palace</h3><p>A real chess position. Every square belongs to a room, drawn with thick walls and a letter: Library, Mirror Hall, Monsoon Courtyard, Stepwell...</p></div>
    <div><b>4</b><h3>The QR code</h3><p>Scan it and the position opens on your phone, set up and ready to play, with no engine to spoil it.</p></div>
    <div><b>5</b><h3>The suspects</h3><p>Every white piece is a guest of the palace, with a name and a room. The white king is you, Inspector Rao. The white pawns are guards.</p></div>
    <div><b>6</b><h3>The testimonies</h3><p>The staff saw who went where. Each statement is one of three sentences, defined in the rules, so nothing is vague.</p></div>
    <div><b>7</b><h3>Your verdict</h3><p>Who gave mate, in which room, and how. The answer, and the reasoning, are at the back of the book.</p></div>
  </div>
</div></section>

<section id="rules"><div class="wrap">
  <span class="tag inv eyebrow">The rules in one minute</span>
  <h2 class="display">Find every mate. Then believe the witnesses.</h2>
  <div class="rules3">
    <div class="rule"><h3>The killer acts alone</h3><p>Only one white piece moves. Black answers with anything he likes, and the killer still mates in the number of moves the case states. Several suspects can usually manage it on the board. That is the point.</p></div>
    <div class="rule"><h3>Three sentences, no gossip</h3><p><b>“X never left the Library.”</b> Every square X touched was in the Library.<br><b>“Nobody set foot in the Stepwell.”</b> No suspect passed through it.<br><b>“Somebody went through the Kitchens.”</b> The killer crossed it at least once.</p></div>
    <div class="rule"><h3>Who, where, how</h3><p>Name the guest, the room where the mating move lands, and the kind of mate: back-rank, smothered, queen's kiss, or named after the piece. From Chief Inspector on, one witness is lying: find out who.</p></div>
  </div>
</div></section>

<section id="look" class="tint"><div class="wrap">
  <span class="tag inv eyebrow">Look inside</span>
  <h2 class="display">A palace, eight guests, forty evenings.</h2>
  <div class="look">
    <figure><img src="/assets/murdermate/page-palace.png" width="800" height="1200" alt="The palace map" loading="lazy"><figcaption>The palace: seven rooms laid over the chessboard.</figcaption></figure>
    <figure><img src="/assets/murdermate/page-guests.png" width="800" height="1200" alt="The guests" loading="lazy"><figcaption>The guests: eight suspects, always the same piece.</figcaption></figure>
    <figure><img src="/assets/murdermate/page-testimonies.png" width="800" height="1200" alt="The testimonies rules" loading="lazy"><figcaption>The testimonies: what each sentence means, exactly.</figcaption></figure>
    <figure><img src="/assets/murdermate/page-levels.png" width="800" height="1200" alt="Choose your case" loading="lazy"><figcaption>Choose your case: four levels, from Rookie to Commissioner.</figcaption></figure>
  </div>
</div></section>

<section id="levels"><div class="wrap">
  <span class="tag inv eyebrow">Four levels, one book</span>
  <h2 class="display">Start easy. End at 1800.</h2>
  <p class="lead">You only need to know how the pieces move. The cases get harder as the book goes on, and the last ones will keep strong club players busy.</p>
  <div class="mmlevels">%s</div>
</div></section>

<section id="series" class="tint"><div class="wrap">
  <span class="tag inv eyebrow">The series</span>
  <h2 class="display">One chess country per book. One chess rule per crime.</h2>
  <p class="lead">Same rules everywhere, a new palace, new suspects, and one chess rule that turns into a plot: promotion hides an impostor, a discovered check needs an accomplice, castling makes the perfect alibi. Each book stands alone.</p>
  <div class="mmseries">%s</div>
</div></section>
""" % (lv, se)
    nav = [('/', 'Kob House', False), ('#how', 'How it works', False), ('#inside', 'Inside a case', False), ('#levels', 'The levels', False), ('#series', 'The series', False), ('/mm/1/01/', 'Try a board', False)]
    return page('Murder Mate: India · Chess murder mysteries · Kob House',
                'Murder Mate: chess murder mysteries. The board is the crime scene, the black king is the victim, every white piece is a suspect. 40 cases, from your first mate to 1800+. Coming soon from Kob House.',
                body, MM_BG, MM_ACC, '/murder-mate/', '/assets/murdermate/cover.png', nav)

def hub():
    cards = ''
    for b in BOOKS:
        meta = '%s pages · %s addresses' % (b['pages'], b['addresses'])
        st = '<span class="tag">Out now</span>' if b['status'] == 'out' else '<span class="tag inv">Coming soon</span>'
        cards += '<a class="book" style="--bg:%s;--acc:%s" href="/%s/"><img src="/assets/%s/cover-sm.png" width="400" height="600" alt="Murder Map: %s cover" loading="lazy"><h3>Murder Map: %s</h3><p>%s</p><div class="meta">%s</div>%s<span class="go">See the book %s</span></a>' % (
            b['bg'], b['acc'], b['slug'], b['key'], b['city'], b['city'], b['card_blurb'], meta, st, ARROW)
    twists = """
<div class="twist"><span class="tag inv">Paris</span><h3>The original</h3><p>Rive gauche or rive droite, along the Seine or by the périphérique: twenty arrondissements and the clues to cut them down, one statement at a time.</p></div>
<div class="twist"><span class="tag inv">Tokyo</span><h3>The train is a witness</h3><p>The Yamanote loop circles the city with 30 stations. Witnesses tell you how far someone rode, clockwise or against the clock, and the loop closes in on the killer.</p></div>
<div class="twist"><span class="tag inv">New York</span><h3>Count the blocks</h3><p>Manhattan on a lettered grid, avenues straight up the page. Witnesses tell you how far they walked, up, down or across, never diagonally.</p></div>"""
    fan = ''.join('<img src="/assets/%s/cover-sm.png" width="400" height="600" alt="%s cover">' % (k, t) for k, t in
                  [('paris', 'Murder Map: Paris'), ('newyork', 'Murder Map: New York'), ('murdermate', 'Murder Mate: India')])
    why = WHY_HTML.replace('<span class="tag inv eyebrow">Why it works</span>', '<span class="tag inv eyebrow">Murder Map · Why it works</span>')
    body = """
<section class="hero"><div class="wrap">
  <div>
    <div class="stamp">Kob House · Puzzle books</div>
    <h1 class="display khtitle">Mysteries you solve with a pen.</h1>
    <p class="lead">Two collections of paper murder cases. Every case has exactly one solution, checked by an independent solver before it goes to print.</p>
    <div class="collections">
      <a class="coll" href="#murder-map" style="--c:#1F6BED;--a:#F4FF1E"><span class="mono">Collection 01 · 3 books</span><b>Murder Map</b><span>Deduction in real cities. Cross out the streets until one door is left.</span><span class="tag">Out now</span></a>
      <a class="coll" href="#murder-mate" style="--c:#0F7B5F;--a:#CDB8F5"><span class="mono">Collection 02 · New</span><b>Murder Mate</b><span>Chess murder mysteries. The weapon is a checkmate.</span><span class="tag inv">Coming soon</span></a>
    </div>
  </div>
  <div class="fan">%s</div>
</div></section>

<div id="murder-map" class="colband" style="--c:#1F6BED;--a:#F4FF1E"><div class="wrap">
  <span class="mono">Collection 01</span>
  <div class="mm"><span class="m1">Murder</span><span class="m2">Map</span></div>
  <p>A real city, three crime scenes. <b>Cross out the city</b> until one door is left.</p>
</div></div>

<section id="books"><div class="wrap">
  <span class="tag inv eyebrow">Murder Map · The books</span>
  <h2 class="display">Three cities. Nine murders. One pen.</h2>
  <p class="lead">Each book hides three killers in a real city and hands you the witness statements, the map and the street grids. Same rules everywhere, and one twist per city taken from something real about it.</p>
  <div class="books">%s</div>
</div></section>

<section id="how" class="paper"><div class="wrap">
  <span class="tag inv eyebrow">Murder Map · How it works</span>
  <h2 class="display">Every witness tells the truth. None of them knows the address.</h2>
  <p class="lead">Read the statements in order. Each one is true, and each one lets you cross out part of the city. Four steps, one pen, no knowledge of the city needed.</p>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Read the statement</h3><p>Every witness gives you one fact. None of them lies. Each fact rules out part of the city.</p></div>
    <div class="step"><div class="n">2</div><h3>Strike out districts</h3><p>Hatch the districts the clue eliminates on the printed map. Trust the map, not your memory.</p></div>
    <div class="step"><div class="n">3</div><h3>Strike out streets</h3><p>Six real streets per district. Cross the ones that no longer fit.</p></div>
    <div class="step"><div class="n">4</div><h3>Cross out the numbers</h3><p>Numbers 1 to 120 on every street. Keep going until a single door survives, then check the verification code.</p></div>
  </div>
</div></section>

%s
<section id="twists"><div class="wrap">
  <span class="tag inv eyebrow">Murder Map · One twist per city</span>
  <h2 class="display">Same rules. A different way to close in.</h2>
  <p class="lead">Every city gets one mechanic of its own, taken from something real: a loop line, a street grid. The books stand alone and can be played in any order.</p>
  <div class="twists">%s</div>
</div></section>

<div class="colband" style="--c:#0F7B5F;--a:#CDB8F5"><div class="wrap">
  <span class="mono">Collection 02 · Coming soon</span>
  <div class="mmate"><span class="w">Murder</span> <span class="l">Mate</span></div>
  <p>Chess murder mysteries. <b>The board is the crime scene.</b></p>
</div></div>
%s

<section id="about" class="tint"><div class="wrap about">
  <div><div class="logo biglogo" style="pointer-events:none"><span class="k">K%sB</span><span class="h">HOUSE</span></div></div>
  <div>
    <h2 class="display">Kob House makes puzzle books you solve with a pen and a suspicious mind.</h2>
    <p class="lead">Every case is generated and then re-solved by an independent solver before it goes to print, which means the logic always holds: one solution, no guessing, no dead ends, no case that falls apart on page forty.</p>
    <p class="lead">Paperbacks, 6 × 9 inches, printed on demand and shipped by Amazon worldwide.</p>
    <div class="series"><a href="/paris/">Paris</a><a class="soon" href="/tokyo/">Tokyo · soon</a><a class="soon" href="/new-york/">New York · soon</a><a class="soon" href="/murder-mate/">Murder Mate · soon</a></div>
  </div>
</div></section>
""" % (fan, cards, why, twists, MURDER_MATE_HUB, FROG)
    return page('Kob House · Murder Map and Murder Mate puzzle books', 'Kob House makes pen-and-paper mystery books with exactly one solution. Murder Map: deduction in real cities (Paris, Tokyo, New York). Murder Mate: chess murder mysteries, coming soon.',
                body, BRAND_BG, BRAND_ACC, '/', '/assets/paris/cover.png', HUB_NAV)

# ------------------------------------------------------------------ legal + files
exec(open(D + '/_legal.txt').read())
exec(open(D + '/_favicon.txt').read())

open(H + '/index.html', 'w').write(hub())
for b in BOOKS:
    os.makedirs(os.path.join(H, b['slug']), exist_ok=True)
    open(os.path.join(H, b['slug'], 'index.html'), 'w').write(book_page(b))
os.makedirs(os.path.join(H, 'murder-mate'), exist_ok=True)
open(os.path.join(H, 'murder-mate', 'index.html'), 'w').write(murder_mate_page())
open(H + '/legal.html', 'w').write(page('Legal notice · Kob House', 'Legal notice for kobhouse.com.', LEGAL, BRAND_BG, BRAND_ACC, '/legal.html', '/assets/paris/cover.png', HUB_NAV))
open(H + '/assets/favicon.svg', 'w').write(FAVICON)
open(H + '/CNAME', 'w').write('kobhouse.com\n')
open(H + '/.nojekyll', 'w').write('')
open(H + '/robots.txt', 'w').write('User-agent: *\nAllow: /\nSitemap: https://kobhouse.com/sitemap.xml\n')
urls = ['https://kobhouse.com/'] + ['https://kobhouse.com/%s/' % b['slug'] for b in BOOKS] + ['https://kobhouse.com/murder-mate/', 'https://kobhouse.com/legal.html']
open(H + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % ''.join('<url><loc>%s</loc></url>' % u for u in urls))
print('ok')
