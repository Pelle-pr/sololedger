import os
BASE = "https://pelle-pr.github.io/sololedger/"
BUY = "https://payhip.com/b/EtfdW"
CSS = """body{font:16px/1.5 system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 16px;color:#1b2430}
label{display:block;margin:.8rem 0 .2rem}input{width:100%;padding:.5rem;font-size:1rem;box-sizing:border-box}
.out{background:#eef4ff;padding:1rem;border-radius:8px;margin-top:1.2rem}.big{font-size:2rem;font-weight:700}
.cta{background:#1f3a5f;color:#fff;padding:1rem;border-radius:8px;margin-top:2rem}.cta a{color:#ffd66b}nav a{margin-right:1rem}"""
NAV = '<nav><a href="index.html">Hourly rate</a><a href="project-price-calculator.html">Project price</a><a href="invoice-late-fee-calculator.html">Late fee</a><a href="freelance-tax-set-aside-calculator.html">Tax set-aside</a></nav>'
pages = {
 "project-price-calculator.html": dict(
  title="Freelance Project Price Calculator – free", h1="Freelance Project Price Calculator",
  desc="Free project price calculator for freelancers. Estimate hours, add a buffer and get a fixed quote.",
  intro="Turn an hour estimate into a fixed project quote with a safety buffer.",
  fields=[("rate","Your hourly rate",75),("hours","Estimated hours",40),("buf","Buffer for scope creep (%)",20),("cost","Direct costs (software, stock, etc.)",0)],
  js="const p=($('rate')*$('hours'))*(1+$('buf')/100)+$('cost');R.innerHTML='Fixed quote<div class=big>'+f(p)+'</div>Effective rate if buffer is unused: '+f(p/$('hours'))+' / hour';"),
 "invoice-late-fee-calculator.html": dict(
  title="Invoice Late Fee Calculator – free", h1="Invoice Late Fee Calculator",
  desc="Free calculator for interest and late fees on overdue invoices. Enter amount, days late and annual rate.",
  intro="Estimate interest on an overdue invoice. Check what late-payment rules apply in your country and what your contract says.",
  fields=[("amt","Invoice amount",1000),("days","Days overdue",30),("rate","Annual interest rate (%)",8),("flat","Flat reminder fee (if any)",0)],
  js="const i=$('amt')*($('rate')/100)*$('days')/365;R.innerHTML='Interest + fees<div class=big>'+f(i+$('flat'))+'</div>Interest: '+f(i)+' | Total due: '+f($('amt')+i+$('flat'));"),
 "freelance-tax-set-aside-calculator.html": dict(
  title="Freelance Tax Set-Aside Calculator – free", h1="Freelance Tax Set-Aside Calculator",
  desc="Free calculator showing how much of each payment to set aside for tax as a freelancer.",
  intro="Enter a payment and your own estimated tax rate to see how much to reserve. Estimate only, not tax advice.",
  fields=[("pay","Payment received (before tax)",5000),("exp","Deductible expenses tied to it",0),("tax","Your estimated tax rate (%)",35)],
  js="const s=Math.max(0,$('pay')-$('exp'))*$('tax')/100;R.innerHTML='Set aside<div class=big>'+f(s)+'</div>You keep about '+f($('pay')-s);"),
}
def page(fn, p, extra_fields=None):
    fields = "".join(f'<label>{l}<input id="{i}" type="number" value="{v}"></label>' for i,l,v in p["fields"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['title']}</title><meta name="description" content="{p['desc']}"><link rel="canonical" href="{BASE}{fn}"><style>{CSS}</style></head><body>
{NAV}<h1>{p['h1']}</h1><p>{p['intro']}</p>{fields}<div class="out" id="R"></div>
<div class="cta"><b>Track invoices, expenses and tax in one Excel file.</b><br>Freelancer Finance Toolkit by SoloLedger. <a href="{BUY}">Get the toolkit</a></div>
<p style="font-size:.85rem;color:#556">Estimates only, not tax, legal or financial advice.</p>
<script>const $=id=>+document.getElementById(id).value;const R=document.getElementById('R');
const f=n=>isFinite(n)?n.toLocaleString(undefined,{{maximumFractionDigits:2}}):'-';
function calc(){{{p['js']}}}document.querySelectorAll('input').forEach(i=>i.oninput=calc);calc();</script></body></html>"""
for fn, p in pages.items():
    open(fn, "w", encoding="utf-8").write(page(fn, p))
urls = [BASE] + [BASE + fn for fn in pages]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
