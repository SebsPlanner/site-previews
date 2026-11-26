"""Full demo website for a florist: shop grid, a real order form that turns into a ready-to-send Instagram DM,
how-it-works, pickup/delivery, about, FAQ. Only public facts from the lead; no invented prices, reviews or awards.
Usage: python3 florist.py lead.json out_dir/   (designer info from config.json next to this file)"""
import json, sys, os, html, hashlib

PALETTES = [  # (bg, ink, accent, accent2, petal colors)
    ("#fff7f8", "#3a1d26", "#d6336c", "#f8c8d4", ["#f06595", "#faa2c1", "#ffdeeb", "#e64980"]),
    ("#fbf7ff", "#2d1f3d", "#7048e8", "#d0bfff", ["#9775fa", "#e5dbff", "#f783ac", "#b197fc"]),
    ("#fff9f2", "#3b2415", "#e8590c", "#ffd8a8", ["#ff922b", "#ffc078", "#ffa8a8", "#fd7e14"]),
    ("#fdf6f4", "#3a1418", "#c92a2a", "#ffc9c9", ["#e03131", "#ff8787", "#ffe3e3", "#c2255c"]),
    ("#f6faf5", "#1f2d22", "#2f9e44", "#c3fae8", ["#f783ac", "#ffd43b", "#ffffff", "#8ce99a"]),
    ("#fffaf0", "#2f2410", "#d9480f", "#fff3bf", ["#fcc419", "#ff6b6b", "#ffa94d", "#ffe066"]),
]

def flower_svg(petals, seed, size=220):
    """a little bouquet drawn in SVG, different per seed"""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    out = [f'<svg viewBox="0 0 220 220" width="{size}" height="{size}" aria-hidden="true">']
    out.append('<path d="M110 210 L95 130 M110 210 L110 120 M110 210 L128 132" stroke="#5c8a4f" stroke-width="5" stroke-linecap="round"/>')
    out.append('<ellipse cx="80" cy="150" rx="22" ry="9" fill="#74b816" transform="rotate(-30 80 150)"/><ellipse cx="142" cy="152" rx="22" ry="9" fill="#74b816" transform="rotate(30 142 152)"/>')
    spots = [(110, 80), (72, 100), (148, 100), (90, 60), (132, 60), (110, 112)]
    for i, (x, y) in enumerate(spots):
        c = petals[(h >> (i * 3)) % len(petals)]; r = 18 + (h >> (i * 2)) % 8
        for k in range(6):
            out.append(f'<ellipse cx="{x}" cy="{y - r * .7:.0f}" rx="{r * .45:.0f}" ry="{r * .75:.0f}" fill="{c}" opacity=".92" transform="rotate({k * 60} {x} {y})"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * .32:.0f}" fill="#fff3bf"/>')
    out.append('<path d="M84 182 L110 214 L136 182 Z" fill="#fff" opacity=".85"/></svg>')
    return "".join(out)

def build(lead, cfg):
    e = lambda s: html.escape(str(s))
    slug = lead["slug"]; pi = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(PALETTES)
    bg, ink, acc, acc2, petals = PALETTES[pi]
    name = e(lead["name"]); ig = lead.get("instagram", ""); city = e(lead.get("city", "Las Vegas")); area = e(lead.get("area", ""))
    tagline = e(lead.get("tagline") or "Fresh flowers for every moment.")
    sub = e(lead.get("subline") or "")
    services = lead.get("services") or ["Custom bouquets"]
    delivery = lead.get("delivery", "Pickup or local delivery")
    spanish = lead.get("spanish")
    d_ig = cfg.get("designer_ig", ""); dm = f"https://ig.me/m/{ig}"
    shop = [s for s in services if not any(w in s.lower() for w in ("dm", "order", "pickup", "delivery", "español", "espanol", "89"))] or services
    cards = "".join(f'''<article class="card"><div class="art">{flower_svg(petals, slug + s, 170)}</div><h3>{e(s)}</h3>
      <p>Made to order in your colors.</p><button onclick="pick('{e(s)}')">Order this</button></article>''' for s in shop[:6])
    opts = "".join(f"<option>{e(s)}</option>" for s in shop[:6]) + "<option>Something custom</option>"
    sp = '<span class="pill">Se habla español</span>' if spanish else ""
    loc = f"{area + ', ' if area else ''}{city}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} · Flowers in {city}</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&display=swap">
<style>
:root{{--bg:{bg};--ink:{ink};--acc:{acc};--acc2:{acc2}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}}
a{{color:inherit}}.wrap{{max-width:1100px;margin:0 auto;padding:0 20px}}
nav{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px)}}
nav .wrap{{display:flex;align-items:center;justify-content:space-between;height:68px;gap:12px}}
.logo{{font:700 24px Fraunces,serif;white-space:nowrap}}.links{{display:flex;gap:22px;font-weight:500}}.links a{{text-decoration:none;opacity:.8}}
.btn{{display:inline-block;background:var(--acc);color:#fff;border:0;border-radius:999px;padding:13px 24px;font:600 15px Inter,sans-serif;text-decoration:none;cursor:pointer;white-space:nowrap;transition:transform .15s}}
.btn:hover{{transform:translateY(-2px)}}.btn.alt{{background:transparent;color:var(--ink);border:2px solid var(--ink)}}
.hero{{display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:30px;padding:60px 0 70px}}
.hero h1{{font:700 clamp(44px,7vw,82px)/1.02 Fraunces,serif;margin:0 0 18px;letter-spacing:-.02em}}
.hero p{{font-size:19px;opacity:.8;max-width:46ch;margin:0 0 26px}}.ctas{{display:flex;gap:12px;flex-wrap:wrap}}
.blob{{position:relative;aspect-ratio:1;border-radius:46% 54% 50% 50%/55% 45% 55% 45%;background:radial-gradient(circle at 30% 30%,#fff,var(--acc2));display:grid;place-items:center;animation:morph 9s ease-in-out infinite alternate}}
.blob svg{{width:78%;height:auto;animation:sway 5s ease-in-out infinite alternate;transform-origin:50% 95%}}
@keyframes morph{{to{{border-radius:58% 42% 45% 55%/45% 58% 42% 55%}}}}@keyframes sway{{from{{transform:rotate(-3deg)}}to{{transform:rotate(3deg)}}}}
.petal{{position:fixed;top:-20px;width:14px;height:10px;border-radius:60% 0;background:var(--acc2);opacity:.7;pointer-events:none;animation:fall linear infinite}}
@keyframes fall{{to{{transform:translate(60px,110vh) rotate(540deg)}}}}
.pill{{display:inline-block;background:var(--acc2);border-radius:999px;padding:6px 14px;font-weight:600;font-size:14px;margin:0 6px 8px 0}}
section{{padding:64px 0}}h2{{font:700 clamp(32px,5vw,48px)/1.1 Fraunces,serif;margin:0 0 10px}}.lead{{opacity:.75;margin:0 0 30px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}}
.card{{background:#fff;border-radius:24px;padding:18px;box-shadow:0 10px 30px rgba(0,0,0,.06);display:flex;flex-direction:column;transition:transform .2s}}
.card:hover{{transform:translateY(-6px) rotate(-.5deg)}}.card .art{{background:var(--acc2);border-radius:18px;display:grid;place-items:center;padding:10px 0;margin-bottom:12px}}
.card h3{{font:700 21px Fraunces,serif;margin:4px 0}}.card p{{margin:0 0 14px;opacity:.7;font-size:15px}}
.card button{{margin-top:auto;background:var(--ink);color:#fff;border:0;border-radius:999px;padding:11px;font:600 14px Inter;cursor:pointer}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}}.step{{background:#fff;border-radius:22px;padding:24px}}
.step b{{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--acc);color:#fff;margin-bottom:10px}}
form{{background:#fff;border-radius:28px;padding:28px;box-shadow:0 14px 40px rgba(0,0,0,.07);display:grid;grid-template-columns:1fr 1fr;gap:14px}}
label{{font-weight:600;font-size:14px;display:grid;gap:6px}}input,select,textarea{{font:15px Inter;padding:12px 14px;border-radius:14px;border:1.5px solid #e9e2e2;background:var(--bg);color:var(--ink)}}
.full{{grid-column:1/-1}}.chips{{display:flex;gap:8px;flex-wrap:wrap}}.chips label{{display:flex;align-items:center;gap:6px;font-weight:500;background:var(--bg);padding:8px 12px;border-radius:999px;cursor:pointer}}
.sw{{width:16px;height:16px;border-radius:50%;display:inline-block}}
.done{{display:none;background:var(--acc2);border-radius:18px;padding:16px}}.done.show{{display:block}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}.box{{background:#fff;border-radius:22px;padding:26px}}
details{{background:#fff;border-radius:18px;padding:16px 20px;margin-bottom:10px}}summary{{font-weight:600;cursor:pointer}}
footer{{padding:40px 0 70px;opacity:.7;font-size:14px}}
.badge{{position:fixed;left:14px;bottom:14px;background:rgba(0,0,0,.75);color:#fff;font:500 12px Inter;padding:7px 12px;border-radius:999px;text-decoration:none;z-index:9}}
@media(max-width:760px){{.hero{{grid-template-columns:1fr;padding-top:30px}}.links{{display:none}}form{{grid-template-columns:1fr}}.logo{{font-size:20px}}nav .btn{{padding:10px 16px;font-size:14px}}}}
</style></head><body>
<nav><div class="wrap"><div class="logo">{name}</div><div class="links"><a href="#shop">Shop</a><a href="#how">How it works</a><a href="#delivery">Pickup &amp; delivery</a><a href="#faq">FAQ</a></div><a class="btn" href="#order">Order flowers</a></div></nav>
<div class="wrap">
<header class="hero"><div>{sp}<span class="pill">{e(loc)}</span><h1>{tagline}</h1><p>{sub}</p>
<div class="ctas"><a class="btn" href="#order">Order flowers</a><a class="btn alt" href="#shop">See arrangements</a></div></div>
<div class="blob">{flower_svg(petals, slug, 320)}</div></header>
<section id="shop"><h2>Arrangements</h2><p class="lead">Every piece is made to order. Pick a style, choose your colors, and we'll make it yours.</p><div class="grid">{cards}</div></section>
<section id="how"><h2>How ordering works</h2><p class="lead">No more back-and-forth in the DMs.</p><div class="steps">
<div class="step"><b>1</b><h3>Pick your arrangement</h3><p>Choose a style, size and color palette below.</p></div>
<div class="step"><b>2</b><h3>Choose a date</h3><p>Tell us the day and whether it's {e(delivery.lower())}.</p></div>
<div class="step"><b>3</b><h3>Send &amp; confirm</h3><p>Your order is sent straight to {name} to confirm the details and price.</p></div></div></section>
<section id="order"><h2>Start your order</h2><p class="lead">Fill this out and your order request goes straight to {name}.</p>
<form onsubmit="return send(event)"><label>Arrangement<select id="arr">{opts}</select></label>
<label>Size<select id="size"><option>Petite</option><option selected>Classic</option><option>Statement</option></select></label>
<div class="full"><label>Color palette</label><div class="chips">{"".join(f'<label><input type="radio" name="pal" value="{n}" {"checked" if i == 0 else ""}><span class="sw" style="background:{c}"></span>{n}</label>' for i, (n, c) in enumerate([("Pinks", "#f06595"), ("Reds", "#e03131"), ("Whites", "#f1f3f5"), ("Pastels", "#d0bfff"), ("Bright mix", "#ffa94d"), ("Florist's choice", "#69db7c")]))}</div></div>
<label>Occasion<select id="occ"><option>Birthday</option><option>Anniversary</option><option>Just because</option><option>Graduation</option><option>Sympathy</option><option>Event / party</option></select></label>
<label>Date needed<input type="date" id="date" required></label>
<label>Pickup or delivery<select id="how2"><option>Pickup</option><option>Local delivery</option></select></label>
<label>Your name<input id="nm" required placeholder="First name"></label>
<label class="full">Notes<textarea id="note" rows="3" placeholder="Card message, favorite flowers, budget..."></textarea></label>
<div class="full"><button class="btn" type="submit">Send order request</button></div>
<div class="full done" id="done">Your order request is copied. Instagram is opening so you can paste it and send it to @{e(ig)}.</div></form></section>
<section id="delivery" class="two"><div class="box"><h2>Pickup &amp; delivery</h2><p>{e(delivery)} in {e(loc)}.</p><p class="lead">Exact times and delivery areas are confirmed with your order.</p></div>
<div class="box"><h2>Say hi</h2><p>Questions about an order or a custom piece? Message {name} on Instagram.</p><a class="btn" href="{dm}">Message @{e(ig)}</a></div></section>
<section id="faq"><h2>Questions</h2>
<details><summary>How far ahead should I order?</summary><p>As early as you can, especially around holidays. {e(lead.get("rush", "Ask about last-minute availability."))}</p></details>
<details><summary>Can I choose my flowers and colors?</summary><p>Yes, every order is custom. Pick a palette in the form or describe it in the notes.</p></details>
<details><summary>How do I pay?</summary><p>{name} confirms the price and payment details with you directly after you send your request.</p></details></section>
<footer>© {name} · {e(loc)} · <a href="https://instagram.com/{e(ig)}">@{e(ig)}</a></footer></div>
<a class="badge" href="https://instagram.com/{e(d_ig)}">Demo site by @{e(d_ig)}</a>
<script>
for(let i=0;i<10;i++){{const p=document.createElement('div');p.className='petal';p.style.left=Math.random()*100+'vw';p.style.animationDuration=(9+Math.random()*9)+'s';p.style.animationDelay=(-Math.random()*15)+'s';p.style.background=['{petals[0]}','{petals[1]}','{petals[2]}'][i%3];document.body.appendChild(p)}}
function pick(s){{document.getElementById('arr').value=s;document.getElementById('order').scrollIntoView()}}
function send(ev){{ev.preventDefault();const g=id=>document.getElementById(id).value;const pal=(document.querySelector('input[name=pal]:checked')||{{}}).value||'';
const msg=`Hi! I'd like to order: ${{g('arr')}} (${{g('size')}}), ${{pal}}, for ${{g('occ').toLowerCase()}} on ${{g('date')}}. ${{g('how2')}}. Name: ${{g('nm')}}. ${{g('note')}}`;
try{{navigator.clipboard.writeText(msg)}}catch(e){{}};document.getElementById('done').classList.add('show');setTimeout(()=>window.open('{dm}','_blank'),900);return false}}
</script></body></html>"""

if __name__ == "__main__":
    lead = json.load(open(sys.argv[1])); here = os.path.dirname(os.path.abspath(__file__))
    cfgp = os.path.join(here, "config.json"); cfg = json.load(open(cfgp)) if os.path.exists(cfgp) else {}
    out = os.path.join(sys.argv[2], lead["slug"]); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(build(lead, cfg)); print(out)
