"""Generate a free one-page website preview for a local business.
Usage: python3 preview.py lead.json out_dir/
lead.json fields (only use facts found publicly; leave unknown fields out, never invent reviews/awards/prices):
  name, niche (detailer|barber|salon|nails|florist|foodtruck|restaurant), city, area (optional neighborhood),
  instagram (handle, no @), phone (optional), address (optional), hours (optional list of strings),
  services (list of short strings from their page/menu), tagline (optional, from their bio), slug
Designer info comes from config.json next to this script: {"designer": "...", "designer_ig": "...", "designer_site": "..."}"""
import json, sys, os, html

THEMES = {
    "detailer":   dict(bg="#0b0d10", panel="#14181e", ink="#f2f5f8", muted="#9aa4b1", a1="#22d3ee", a2="#3b82f6",
                       font="'Archivo Black', 'Archivo', sans-serif", body="'Archivo', sans-serif",
                       hero="Showroom shine, wherever you park.", cta="Book a detail", icon="car"),
    "barber":     dict(bg="#111010", panel="#1b1918", ink="#f6efe6", muted="#b3a89b", a1="#d4a24c", a2="#b45309",
                       font="'Oswald', sans-serif", body="'Inter', sans-serif",
                       hero="Fresh cuts. Clean fades. No guesswork.", cta="Book a cut", icon="scissors"),
    "salon":      dict(bg="#fbf6f2", panel="#ffffff", ink="#2a1f1c", muted="#7a6a63", a1="#c0846b", a2="#e7b8a6",
                       font="'Playfair Display', serif", body="'Inter', sans-serif",
                       hero="Hair you'll want to show off.", cta="Book an appointment", icon="sparkle"),
    "nails":      dict(bg="#fff5f8", panel="#ffffff", ink="#2b1b24", muted="#86687a", a1="#ec4899", a2="#f9a8d4",
                       font="'DM Serif Display', serif", body="'Inter', sans-serif",
                       hero="Nails worth the close-up.", cta="Book your set", icon="sparkle"),
    "florist":    dict(bg="#f7f5ef", panel="#ffffff", ink="#1f2a1f", muted="#66705f", a1="#7c9a5b", a2="#e6a4b4",
                       font="'Cormorant Garamond', serif", body="'Inter', sans-serif",
                       hero="Flowers for every moment.", cta="Order flowers", icon="flower"),
    "foodtruck":  dict(bg="#fff8e7", panel="#ffffff", ink="#231a10", muted="#7a6650", a1="#f97316", a2="#facc15",
                       font="'Bebas Neue', sans-serif", body="'Inter', sans-serif",
                       hero="Find us. Eat well. Repeat.", cta="See the menu", icon="truck"),
    "restaurant": dict(bg="#1a1512", panel="#241d19", ink="#f7efe6", muted="#bba795", a1="#e4572e", a2="#f3a712",
                       font="'Fraunces', serif", body="'Inter', sans-serif",
                       hero="Come hungry. Leave happy.", cta="View the menu", icon="plate"),
}
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&family=Archivo+Black&family=Oswald:wght@500;700"
         "&family=Playfair+Display:wght@600&family=DM+Serif+Display&family=Cormorant+Garamond:wght@600&family=Bebas+Neue"
         "&family=Fraunces:wght@600&family=Inter:wght@400;500;600&display=swap")
ICONS = {
    "car": '<path d="M5 17h14M6 17l1.5-5h9L18 17M7 17v2M17 17v2M8 12l1-3h6l1 3" />',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "flower": '<circle cx="12" cy="9" r="3"/><path d="M12 12v9M12 6a3 3 0 1 1 3 3M12 6a3 3 0 1 0-3 3M9 15c-2 0-3-1-3-3M15 15c2 0 3-1 3-3"/>',
    "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',
    "plate": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/>',
}

def build(lead, cfg):
    t = THEMES.get(lead.get("niche"), THEMES["detailer"])
    e = lambda s: html.escape(str(s))
    name = e(lead["name"]); city = e(lead.get("city", "Las Vegas")); area = e(lead.get("area", ""))
    ig = lead.get("instagram", ""); phone = lead.get("phone", "")
    services = lead.get("services") or []
    tagline = e(lead.get("tagline") or t["hero"])
    book = f"tel:{phone}" if phone else (f"https://ig.me/m/{ig}" if ig else "#contact")
    icon = ICONS[t["icon"]]
    svc = "".join(f'<li><svg viewBox="0 0 24 24">{icon}</svg><span>{e(s)}</span></li>' for s in services[:8])
    hours = "".join(f"<li>{e(h)}</li>" for h in lead.get("hours") or [])
    contact_bits = []
    if phone: contact_bits.append(f'<a class="btn" href="tel:{e(phone)}">Call {e(phone)}</a>')
    if ig: contact_bits.append(f'<a class="btn ghost" href="https://instagram.com/{e(ig)}">@{e(ig)}</a>')
    addr = f'<p class="muted">{e(lead["address"])}</p>' if lead.get("address") else f'<p class="muted">Serving {area + ", " if area else ""}{city}</p>'
    d_ig = cfg.get("designer_ig", ""); d_name = e(cfg.get("designer", "Sebastien"))
    d_link = f"https://ig.me/m/{d_ig}" if d_ig else "#"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} · {city}</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="{FONTS}">
<style>
:root{{--bg:{t['bg']};--panel:{t['panel']};--ink:{t['ink']};--muted:{t['muted']};--a1:{t['a1']};--a2:{t['a2']}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:{t['body']};line-height:1.55}}
a{{color:inherit}}.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.bar{{background:var(--a1);color:#fff;text-align:center;font:600 14px/1.4 Inter,sans-serif;padding:10px 16px}}
.bar a{{font-weight:700}}
nav{{display:flex;justify-content:space-between;align-items:center;padding:22px 0}}
.logo{{font-family:{t['font']};font-size:26px;letter-spacing:.02em}}
.btn{{display:inline-block;background:var(--a1);color:#fff;text-decoration:none;font-weight:600;padding:14px 24px;border-radius:999px;transition:transform .15s}}
.btn:hover{{transform:translateY(-2px)}}.btn{{white-space:nowrap}}@media(max-width:520px){{nav .btn{{padding:10px 16px;font-size:14px}}.logo{{font-size:20px}}}}.btn.ghost{{background:transparent;border:2px solid var(--a1);color:var(--ink)}}
.hero{{padding:64px 0 80px;display:grid;gap:28px}}
.hero h1{{font-family:{t['font']};font-size:clamp(42px,8vw,88px);line-height:1;margin:0;max-width:14ch}}
.hero p{{font-size:20px;color:var(--muted);max-width:52ch;margin:0}}
.glow{{height:280px;border-radius:28px;background:radial-gradient(circle at 25% 30%,var(--a2),transparent 55%),radial-gradient(circle at 80% 70%,var(--a1),transparent 50%),var(--panel);
  display:grid;place-items:center;color:var(--muted);font-size:14px;letter-spacing:.12em;text-transform:uppercase;animation:drift 8s ease-in-out infinite alternate}}
@keyframes drift{{to{{background-position:30px 20px,-30px -10px,0 0}}}}
h2{{font-family:{t['font']};font-size:clamp(30px,5vw,48px);margin:0 0 24px}}
section{{padding:56px 0}}
.svc{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}
.svc li{{background:var(--panel);border-radius:18px;padding:20px;display:flex;gap:14px;align-items:center;font-weight:600}}
.svc svg{{width:30px;height:30px;flex:none;fill:none;stroke:var(--a1);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}}
.card{{background:var(--panel);border-radius:22px;padding:28px}}
.muted{{color:var(--muted)}}ul.hours{{padding-left:18px;margin:0}}
.gallery{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.gallery div{{aspect-ratio:1;border-radius:16px;background:linear-gradient(135deg,var(--a2),var(--a1));opacity:.35}}
footer{{padding:40px 0 60px;color:var(--muted);font-size:14px}}
.made{{position:fixed;right:16px;bottom:16px;background:#111;color:#fff;font:600 13px Inter,sans-serif;padding:10px 14px;border-radius:999px;text-decoration:none;box-shadow:0 6px 24px #0005}}
</style></head><body>
<div class="bar">Free website preview made for {name} · not live yet · <a href="{d_link}">want it live? message {d_name}</a></div>
<div class="wrap">
<nav><div class="logo">{name}</div><a class="btn" href="{book}">{e(t['cta'])}</a></nav>
<header class="hero"><h1>{tagline}</h1><p>{e(lead.get("subline") or (", ".join(services[:3]) + "." if services else ""))} {name}, serving {area + ", " if area else ""}{city}.</p>
<div><a class="btn" href="{book}">{e(t['cta'])}</a></div><div class="glow">your photos go here</div></header>
<section><h2>Services</h2><ul class="svc">{svc or '<li><span>Your services, prices and packages go here</span></li>'}</ul></section>
<section><h2>Your work, front and center</h2><div class="gallery"><div></div><div></div><div></div><div></div><div></div><div></div></div>
<p class="muted">Your best Instagram photos, pulled into a gallery that loads fast on any phone.</p></section>
<section id="contact" class="cols"><div class="card"><h2>Visit &amp; book</h2>{addr}<p>{' '.join(contact_bits)}</p></div>
{'<div class="card"><h2>Hours</h2><ul class="hours">' + hours + '</ul></div>' if hours else ''}</section>
<footer>© {name}. Preview design by {d_name}.</footer></div>
<a class="made" href="{d_link}">Like it? Get this site →</a>
</body></html>"""

if __name__ == "__main__":
    lead = json.load(open(sys.argv[1])); here = os.path.dirname(os.path.abspath(__file__))
    cfg = json.load(open(os.path.join(here, "config.json"))) if os.path.exists(os.path.join(here, "config.json")) else {}
    out = os.path.join(sys.argv[2], lead["slug"]); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(build(lead, cfg)); print(out)
