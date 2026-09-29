#!/usr/bin/env python3
"""DiggerLid BFCM 2026 campaign deck, version 2.0 (Slides artifact format).
Rules: no system/AI references; measured numbers stated plainly; proposals labelled as proposals;
brand voice (short, plain, tradesperson); no em dashes; every slide answers a question the exec
or the team would ask."""
import os, json, datetime, re
ROOT = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(ROOT, "project", "slides"); os.makedirs(SL, exist_ok=True)

K="#231f20"; K90="#3a3637"; K80="#4f4b4c"; Y="#f5eb19"; Y70="#f8f163"; Y40="#fbf7a3"; W="#fdfdfb"; MUTE="#4f4b4c"; GREY="#9a9697"
HEAD="'Roboto Condensed', 'Arial Narrow', Arial, sans-serif"
BODY="'League Spartan', Arial, sans-serif"
DISP="'Anton', Impact, 'Arial Narrow', sans-serif"

def banner(text, bg=K, fg=Y, size=28):
    return (f'<div style="display:flex; align-items:center; background:{bg}; padding:10px 28px; transform:skewX(-8deg); align-self:start">'
            f'<p style="font-family:{DISP}; font-size:{size}px; color:{fg}; text-transform:uppercase; letter-spacing:1px; transform:skewX(8deg)">{text}</p></div>')

def foot(src=""):
    return (f'<div style="position:absolute; left:128px; right:128px; bottom:64px; display:flex; justify-content:space-between; align-items:center">'
            f'<p style="font-size:24px; color:{MUTE}">BFCM 2026 Sale Plan{(" · Source: " + src) if src else ""}</p>'
            f'<p style="font-size:24px; color:{MUTE}">{{{{N}}}}</p></div>')

def content(id_, title, body, src="", notes="", kicker=None, gap=32):
    kick = banner(kicker, size=24) if kicker else ""
    return (f'<section id="{id_}" data-transition="fade" style="background:{W}; color:{K}; font-family:{BODY}; '
            f'padding:104px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">'
            f'{kick}<h2 style="font-family:{HEAD}; font-size:60px; font-weight:700; line-height:1.05; text-transform:uppercase">{title}</h2>'
            f'{body}{foot(src)}{("<aside>"+notes+"</aside>") if notes else ""}</section>')

def section(id_, num, title, sub):
    return (f'<section id="{id_}" data-transition="push" style="background:{K}; color:{W}; font-family:{BODY}; '
            f'padding:128px; display:flex; flex-direction:column; justify-content:center; gap:40px">'
            f'<p style="font-family:{DISP}; font-size:44px; color:{Y}; letter-spacing:2px">{num}</p>'
            f'<h1 style="font-family:{HEAD}; font-size:120px; font-weight:700; line-height:1; text-transform:uppercase; color:{W}">{title}</h1>'
            f'<p style="font-size:36px; color:{Y70}; line-height:1.3">{sub}</p>'
            f'<div style="position:absolute; left:128px; right:128px; bottom:64px; display:flex; justify-content:space-between">'
            f'<p style="font-size:24px; color:{GREY}">BFCM 2026 Sale Plan</p><p style="font-size:24px; color:{GREY}">{{{{N}}}}</p></div></section>')

def card(title, lines, bg="#ffffff", accent=Y, tsize=30, lsize=25, flex="1"):
    lis="".join(f'<li>{l}</li>' for l in lines)
    return (f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:12px; background:{bg}; padding:26px 28px; border:2px solid {K}; border-top:12px solid {accent}">'
            f'<h3 style="font-family:{HEAD}; font-size:{tsize}px; font-weight:700; line-height:1.1; text-transform:uppercase">{title}</h3>'
            f'<ul style="font-size:{lsize}px; line-height:1.35; color:{K90}">{lis}</ul></div>')

def big(num, label, bg=Y40, nsize=68):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:26px 28px; border:2px solid {K}">'
            f'<p style="font-family:{HEAD}; font-size:{nsize}px; font-weight:700; line-height:1">{num}</p>'
            f'<p style="font-size:25px; line-height:1.3; color:{K90}">{label}</p></div>')

def table(headers, rows, widths, size=25, hl=None, align_first_left=True):
    th="".join(f'<th style="width:{w}%; text-align:left; color:{W}; background:{K}">{h}</th>' for i,(h,w) in enumerate(zip(headers,widths)))
    trs=""
    for ri,r in enumerate(rows):
        bg=f' style="background:{Y40}"' if hl is not None and ri in (hl if isinstance(hl,(list,tuple)) else [hl]) else ""
        trs+=f'<tr{bg}>'+"".join(f'<td style="text-align:left">{c}</td>' for c in r)+'</tr>'
    return f'<table style="font-size:{size}px; font-family:{BODY}; border:1px solid {K}"><tr style="background:{K}; color:{W}">{th}</tr>{trs}</table>'

def note(text, size=24):
    return f'<p style="font-size:{size}px; color:{K90}; line-height:1.35">{text}</p>'

def qa(items, qsize=28, asize=24):
    out=""
    for q,a in items:
        out+=(f'<div style="display:flex; flex-direction:column; gap:6px; border-bottom:2px solid {K}; padding:0 0 12px 0">'
              f'<h3 style="font-family:{HEAD}; font-size:{qsize}px; font-weight:700; line-height:1.1">{q}</h3>'
              f'<p style="font-size:{asize}px; line-height:1.3; color:{K90}">{a}</p></div>')
    return f'<div style="display:flex; flex-direction:column; gap:14px">{out}</div>'

S={}
# ------------------------------------------------------------------ INTRO
S["cover"]=(f'<section id="cover" data-transition="push" style="background:{K}; color:{W}; font-family:{BODY}; padding:128px; display:flex; flex-direction:column; justify-content:space-between">'
 f'<div style="display:flex; justify-content:space-between; align-items:center">'
 f'<p style="font-family:{HEAD}; font-size:40px; font-weight:700; letter-spacing:1px; color:{W}">DiggerLid</p>'
 f'<p style="font-size:26px; color:{GREY}">Executive and team briefing · September 2026 · v3.3</p></div>'
 f'<div style="display:flex; flex-direction:column; gap:28px">'
 f'{banner("Black Friday · Cyber Monday", bg=Y, fg=K, size=36)}'
 f'<h1 style="font-family:{HEAD}; font-size:168px; font-weight:700; line-height:0.95; text-transform:uppercase; color:{W}">BFCM 2026<br>Sale Plan</h1>'
 f'<p style="font-size:38px; color:{Y70}; line-height:1.3">What we learned last time, what we are running, what we are selling, and what has to be locked before the hype starts.</p></div>'
 f'<aside>Four parts: research, strategy, offer and creative, production. Research slides are measured numbers; the rest is the proposal for this room to decide.</aside></section>')

S["onepage"]=content("onepage","The plan on one page",
 f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; flex:1">'
 +"".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:22px 24px; border:2px solid {K}">'
   f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>'
   for t,d,bg in [
   ("When","Hype Tue 17 and Wed 18 Nov. Sale Thu 19 Nov 12:00 PM (midday) to Tue 1 Dec 11:59 PM AEDT: 13 days, Black Friday on day 9, Cyber Monday on day 12. Christmas gifting push from mid-sale, Mon 23 Nov.",Y40),
   ("Target","$990k sale revenue incl. GST (about $900k net). Floor: $585k (2025 repeated). Stretch: $1.27M on the Aug to Sep run rate. Spend $230k, about 23% of revenue; ceiling 28%.","#ffffff"),
   ("Offer","Up to 25% off + free gifts + huge bundles. Sitewide up to 25% off, grease excluded; DiggerShield $150 / $200 off. Gifts: $399 Digger Wipes + free shipping; $599 adds a Magnet Tool Mat; $799 adds a Drawbar Cover. Bundles: Hardcore Tradie $777 (30% off), Ultimate Earthmover $732 and Owner Operator $778 (35% off the hero gear, the rest free).",Y40),
   ("Theme","All Aussie Earthmoving Adventures: The Great Black Friday Haul. Jack Clacker, four locations, one episode per location, cut down for paid. Christmas gifting page live from the mid-sale push.","#ffffff"),
   ("Channels","Meta paid social for acquisition (cold traffic to product pages), email and SMS for the base (segmented sends), organic and creator content for the theme, site pages built before hype.",Y40),
   ("Pre-sale to-dos","Popup reach above 50% on paid pages by 15 Oct · bundle, DiggerShield and gift margins signed off by 30 Oct · collab bundle confirmed · block 2 shoot 27 and 28 Oct · pages live and tracked by 13 Nov · ads and sends scheduled before hype on 17 Nov.","#ffffff")]) + '</div>',
 notes="If someone reads only one slide, this is it. Target $990k incl. GST, spend $230k (about 23%). Dates moved on 28 Sep: hype Tue 17 and Wed 18 Nov, sale Thu 19 Nov to Tue 1 Dec.")

S["changes"]=content("changes","What changes from 2025",
 table(["","2025","2026"],[
  ["Launch","Tue 18 Nov, 3:05 PM: day one was nine hours long","Wed 18 Nov, 12:00 PM (midday) AEDT, launch send at midday, 14 days to Tue 1 Dec"],
  ["Hype traffic","Sent to the sale page before it was live: 2,328 sessions, 13 orders","Sent to a first-access capture page with a countdown"],
  ["Cold prospecting","Sent to the sale page: 19 Nov, 4,628 sessions at 0.99%","Sent to grease and PRO Mat product pages; sale page for warm traffic"],
  ["Mid-sale","One engaged send (25 Nov) and a Black Friday blast","Daily 3:30 PM knock-off drop plus a mid-sale engaged send with a bonus gift"],
  ["Offer","Sitewide discount","Up to 25% ex-grease, dollar-off on DiggerShield, gift tiers, three hero bundles"],
  ["Theme","Sale creative","All Aussie Adventure film with four episodes, plus cut-downs and stills from one shoot"],
  ["Popup","Discount popup left running: 53% saw it, 2.3% submitted (EOFY)","Sale-specific popup: early access or bonus gift"],
  ["Measurement","Cart tracking broken; no daily rule for cutting spend","Tracking verified before hype; daily scorecard with written cut rules"],
  ["After","Discount hangover into December","Gift guide, new product launch, shipping cut-off messaging, no December list buying"]],[16,42,42],size=24),
 src="Shopify, Klaviyo send log, 2025 sale review",notes="Every row on the right is backed by a number on the research slides. This is the slide for anyone who ran last year and wants to know what is different.")

S["agenda"]=content("agenda",'Agenda',
 f'<div style="display:flex; gap:24px; flex:1">'+"".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:14px; background:{bg}; padding:32px 28px; border:2px solid {K}">'
 f'<p style="font-family:{DISP}; font-size:60px; color:{K}; line-height:1">{i}</p>'
 f'<h3 style="font-family:{HEAD}; font-size:36px; font-weight:700; text-transform:uppercase; line-height:1.05">{t}</h3>'
 f'<p style="font-size:24px; line-height:1.35; color:{K90}">{d}</p></div>'
 for i,(t,d,bg) in enumerate([
  ("Research","The last three sales side by side, and the shape a DiggerLid sale takes day by day.",Y40),
  ("Strategy","Eight moves for 2026: what changes from last year and why.","#ffffff"),
  ("Offer and creative","Discount, gift tiers, bundles with prices, the Christmas gifting page, theme, creative volume.",Y40),("Production","The four shoot days, the concepts so far, and the deliverables.","#ffffff")],1))+'</div>')

# ------------------------------------------------------------------ 01 RESEARCH
S["s-research"]=section("s-research","01","Research","What the last three sales measured, and the five questions the team asked for 2026.")

S["scorecard"]=content("scorecard","The last three sales, side by side",
 table(["Measure","BFCM 2025","EOFY 2026","Father&#39;s Day 2026"],[
  ["Sale dates","18 Nov to 1 Dec 2025","17 to 30 Jun 2026","23 Aug to 7 Sep 2026"],["Net revenue over the sale","$535k (14 days)","$543k (14 days)","$292k (16 days)"],["Orders","1,759","2,107","1,022"],
  ["Share of sale revenue in the first 48 hours","31%","19%","11%"],["Mid-sale revenue per day","5.3%","4.9%","6.7%"],
  ["Share of sale revenue in the last 48 hours","15%","32%","9%"],["Revenue from returning customers","22%","29%","22%"],
  ["Sale landing page conversion","2.09%","3.38%","2.33%"],["Orders from landing page sessions","373","382","104"],
  ["Meta spend as % of revenue","25.5% (month)","25% (month)","28% (sale window)"]],[40,20,20,20],size=25,hl=7)+
 note("BFCM front-loads because the urgency is the launch; EOFY back-loads because the urgency is 30 June. Father&#39;s Day (23 Aug to 7 Sep) ran flat: no launch spike and no deadline spike, about 6.7% a day throughout, because the gift deadline sat after the sale ended."),
 src="Shopify analytics, Meta, Klaviyo send log",notes="Father&#39;s Day ran 16 days. Meta spend is shown for the sale window; the other two sales show the whole month.")

S["mix"]=content("mix","What sold in the 2025 sale",
 f'<div style="display:flex; gap:28px; flex:1"><div style="flex:3">'+table(["Product","Net revenue","Share","Orders"],[
  ["Pro Excavator Enclosure","$154k","29%","262"],["KAJO Grease Packs","$134k","25%","485"],["PRO Mat","$59k","11%","328"],["DiggerShield Kit","$44k","8%","32"],
  ["1.7 Tonne Excavator Cover","$39k","7%","126"],["Battery Grease Gun Adapter","$20k","4%","381"],["KAJO Grease Gun","$13k","2%","101"],["Quicky Cover","$12k","2%","121"],
  ["Mini Loader and Universal covers","$22k","4%","132"],["Grease Coupler","$10k","2%","418"]],[40,20,16,24],size=24)+'</div>'
 f'<div style="flex:2; display:flex; flex-direction:column; gap:16px">{big("33%","of sale revenue was the grease system ($177k). Grease packs were the one product with a recorded discount: 14% off, $21.6k.")}{big("$3k","from bundles: 31 orders across two bundles. The three hero bundles are new ground, not a repeat.",bg="#ffffff")}{big("27%","of sale revenue was international ($147k: US $36k, NZ $30k, UK $28k, Canada $20k) at an average order of $570 against $258 in Australia.")}</div></div>',
 src="Shopify analytics, 18 Nov to 1 Dec 2025",notes="Three facts that change decisions: grease is a third of the sale, bundles have no track record, and international orders are big-ticket. Other product markdowns were made as price changes, so their discount depth does not show in this data.")

S["wellpoorly"]=content("wellpoorly","What went well, what went poorly",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Went well",["EOFY sale page converted 3.38%, and made more orders than the BFCM page on 37% fewer sessions","Segmented sends to the engaged base lifted returning share to 42 to 43% on Cyber Monday and EOFY day 9","Launch and deadline spikes each delivered about 30% of sale revenue","EOFY page ordering (grease first): 5.7 pages per session","Email signups kept converting: about 30% of popup signups buy, every month"],accent=Y)
 +card("Went poorly",["BFCM day 2: 4,628 cold-social sessions at 0.99% pulled the page average to 2.09%","Hype traffic sent to a sale page with nothing to buy: 4,300 sessions, 25 orders, no email capture","Father&#39;s Day page went live four days after the sale started","BFCM cart-add tracking was broken (fewer cart adds than orders)","Popup in the EOFY sale: 53% of sessions saw it, 2.3% submitted","Mid-sale offer did not lift engagement; the promo broke even at best"],accent=K80)+'</div>',
 src="Shopify, PostHog, Alia, planning notes",notes="Design, landing page, ads, email, budget allocation, sale performance, creative output and tactics, as asked in the notes. The right-hand column becomes the lock-up checklist.")

S["lpresults"]=content("lpresults","Landing pages: the EOFY page converted 62% better",
 table(["Measure","BFCM 25 /pages/blackfriday","EOFY 26 /pages/eofy-2026","FD 26 /pages/fathers-day-2026"],[
  ["Landing sessions","17,870","11,304","4,464"],["Session to order","2.09%","3.38%","2.33%"],["Orders","373","382","104"],
  ["Direct traffic share","16%","28%","not split"],["Social traffic conversion","1.37%","2.04%","not split"],["Reached checkout","2.8%","4.7%","not split"],
  ["Pages per session","not tracked","5.7","5.4"],["Live","before hype","before hype","4 days after launch"]],[34,22,22,22],size=25,hl=1)
 +f'<div style="display:flex; gap:24px">{big("0.99%","conversion on 19 Nov 2025: one day of cold social was a quarter of the page traffic.")}{big("3 to 4x","higher conversion on the homepage than on either sale page, because warm traffic lands there. Judge the sale page by traffic source.",bg="#ffffff")}{big("0.6%","conversion of hype traffic sent to the sale page before launch: 4,300 sessions, 25 orders, nothing captured.")}</div>',
 src="Shopify analytics, PostHog",notes="Answers the design and landing page questions. Fix list: build before hype, split cold from warm, capture the hype traffic, verify tracking.")

S["repeat"]=content("repeat","Are we a low-repeat or a hybrid business? Low, on the line",
 f'<div style="display:flex; gap:24px">{big("21.4%","of customers in the last 12 months had bought before. Lifetime: 17.7%. Industry bands: low repeat under 20%, hybrid 20 to 39%.")}{big("16.4%","the same measure with grease removed. Grease is the only product that repeats (about 27% of grease-pack buyers reorder).",bg="#ffffff")}{big("93.5%","of PRO Mat buyers were new to DiggerLid on that order. It brings people in; 2 to 8% buy again.")}</div>'
 +table(["Product set","Repeat orders per buyer","What it means for the sale"],[["Grease system","31%","Exclude from the sitewide discount; it is the reorder base"],["Whole store","27%","Run the sale on first-order economics: AOV, first-order margin, day-one payback"],["Covers","11%","Repeat here is a second machine, not a replacement"],["Machine protection (all durables)","10%","One and done; no retention play to protect"],["PRO Mat","2.6%","Lead with it for acquisition; bundle it for AOV"]],[32,26,42],size=24),
 src="Shopify customer records",notes="The sale curve still looks like a hybrid store, but the mechanism is urgency on new customers, not the base returning. Plan spend accordingly.")

S["questions"]=content("questions","The five questions from the planning session, answered",
 qa([("1. Do we ramp spend now, or spend on profitability?","Not on traffic yet. The email popup reached 23% of sessions in September against 70% early in the year, while its conversion never moved. Fix reach first; email capture pays within weeks (about 30% of signups buy in their first month)."),
     ("2. Dial up UGC?","Yes, and wider. 70% of launch-day buyers are new customers, so creative that qualifies cold traffic is the constraint, not budget. Test markets get a fixed budget and a kill rule."),
     ("3. Are we low repeat or hybrid?","Low repeat: 17.7% lifetime, 21.4% in the last 12 months; 14 to 16% without grease. The sale curve is hybrid-shaped because urgency acts on new customers."),
     ("4. Should we raise any prices now, such as DiggerShield?","DiggerShield is the candidate: 622 buyers ever, 3.5% repeat, the highest contribution per customer in the range ($1,063 in 12 months). A price test in the pre-hype window carries low risk. Decide by mid-October."),
     ("5. Mid-sale offer: continue?","Yes, as a segmented send to the engaged base with a real reason (early access or a bonus gift), not a database blast. Segmented sends moved returning share; blasts did not.")],qsize=27,asize=24),
 src="Shopify, Alia, Klaviyo",notes="Question four is the only one that needs a test rather than a read.")

bfcm=[17.9,13.5,7.6,6.4,5.4,5.4,4.1,5.5,5.4,4.3,4.0,5.2,5.6,9.7]; eofy=[12.6,6.8,5.7,4.1,5.2,4.7,4.0,5.4,4.9,4.7,3.7,6.7,11.6,20.0]
def bars(vals,color,hype=()):
    out=""
    for n,v in enumerate(list(hype)+list(vals)):
        is_h=n<len(hype); lab=f"H{n+1}" if is_h else str(n-len(hype)+1)
        h=int(v/20.0*270)
        box=(f'background:#ffffff; border:2px dashed {K}' if is_h else f'background:{color}; border:2px solid {K}')
        out+=(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px">'
              f'<p style="font-size:22px; color:{K90}">{v:.0f}%</p><div style="width:30px; height:{max(h,4)}px; {box}"></div><p style="font-size:22px; color:{MUTE if not is_h else K}; font-weight:{700 if is_h else 400}">{lab}</p></div>')
    return out
S["curve"]=content("curve","The daily shape we are planning to",
 f'<div style="display:flex; gap:32px; flex:1">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:8px"><h3 style="font-family:{HEAD}; font-size:27px; font-weight:700">BFCM 2025: share of sale revenue by day</h3><div style="display:flex; gap:4px; align-items:end; height:330px; border-bottom:2px solid {K}">{bars(bfcm,Y,hype=[1.7,1.0])}</div>'
 f'<p style="font-size:22px; line-height:1.3; color:{K90}"><b>Hype, 16 and 17 Nov:</b> $14k and 57 orders. Site sessions flat on the week before (5.5k); conversion 1.0% against 1.4%.</p></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:8px"><h3 style="font-family:{HEAD}; font-size:27px; font-weight:700">EOFY 2026: share of sale revenue by day</h3><div style="display:flex; gap:4px; align-items:end; height:330px; border-bottom:2px solid {K}">{bars(eofy,K80,hype=[2.8,1.5])}</div>'
 f'<p style="font-size:22px; line-height:1.3; color:{K90}"><b>Hype, 15 and 16 Jun:</b> $24k and 106 orders. Sessions up 50% on the week before (10.3k); conversion fell to 1.0% from 2.1%.</p></div></div>'
 +f'<div style="display:flex; gap:24px">{big("30%","of sale revenue in the first 48 hours at BFCM. On the $990k plan that is about $297k for the launch weekend.")}{big("5%","per day through the middle. The mid-sale content drop, the gifting push and segmented sends exist to lift this number.",bg="#ffffff")}{big("70%","of launch-day buyers were new customers. The launch is an acquisition play; keep prospecting on.")}</div>',
 src="Shopify analytics",notes="Dashed bars H1 and H2 are the two hype days before each launch, as a share of the sale revenue that followed. Both sales saw hype days sell less than an ordinary day while traffic held or rose: people browsed and waited. Plan spend and stock to the front for BFCM.")

reach=[("Jan","67"),("Feb","70"),("Mar","64"),("Apr","80"),("May","44"),("Jun","53"),("Jul","33"),("Aug","34"),("Sep","23")]
rb="".join(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px"><p style="font-size:26px; font-weight:700">{v}%</p><div style="width:88px; height:{int(int(v)/80*280)}px; background:{Y if int(v)>=50 else K80}; border:2px solid {K}"></div><p style="font-size:25px; color:{MUTE}">{m}</p></div>' for m,v in reach)
S["reach"]=content("reach","Before more traffic: the popup reaches a quarter of visitors",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:3; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700">Share of sessions that saw the email popup, 2026</h3><div style="display:flex; gap:10px; align-items:end; height:360px; border-bottom:2px solid {K}">{rb}</div></div>'
 f'<div style="flex:2; display:flex; flex-direction:column; gap:18px">{big("5%","of viewers submit, every month except during the EOFY sale. The popup itself is not the problem.",bg="#ffffff")}{big("921","signups in September. At January reach on September traffic the same month would have produced about 2,800.")}{big("$65","contribution per signup in the first year, before allowing for people who would have bought anyway. The most an extra email is worth.",bg="#ffffff")}</div></div>',
 src="Alia, Shopify, Klaviyo",notes="The first job of the traffic and email push: audit the popup trigger rules and page targeting on the paid landing pages, restore 50%+ reach on paid traffic by 15 October, and check it weekly.")

# ------------------------------------------------------------------ 02 STRATEGY
S["s-strategy"]=section("s-strategy","02","Strategy","Target and budget, eight moves, the channel plan, and how paid, email and SMS each earn their place.")

S["target"]=content("target","Target: three cases on one basis (revenue incl. GST, as the EE calendar)",
 table(["Case","Sale revenue (2 hype + 14 days)","How it is derived","Spend at 20% / 25% / 28%"],[
  ["Floor: 2025 repeated","$585k (net $535k)","2025 sale, 18 Nov to 1 Dec, restated on the calendar basis","$117k / $146k / $164k"],
  ["Plan: EE tool, latest run","$983k (net about $905k)","10.9× the weekly BAU of Sep to Oct 2025 gave Nov 2025; applied to a $90k week (July was $92.7k, August $119k) = $982,777. The calendar&#39;s preloaded plan for November is $990k","$197k / $246k / $275k"],
  ["Stretch: current run rate","$1.27M (net about $1.16M)","Same multiple on Aug to Sep 2026 BAU ($118k/wk)","$254k / $318k / $356k"]],[20,22,40,18],size=24)
 +f'<div style="display:flex; gap:24px">{big("1.72x","EOFY 2026 grew on EOFY 2025 while BAU grew 1.82x: the sale scales with BAU, which is why the multiple method holds.")}{big("$983k","is the tool&#39;s projection at a 25% sale MER ($243k of spend, 24.7% effective with conservative hype), 1% under the calendar&#39;s $990k plan of record. Profit in the tool: $148k, before the corrections on the next slide.",bg="#ffffff")}{big("$90k","base week in the tool, below July (the worst month, $92.7k) and well below Aug to Sep ($118k). The most conservative setting yet; the base week is the difference between $983k and $1.27M.")}</div>',
 src="EE calendar 2025 and 2026, Shopify, EE BFCM tool",notes="The EE multiple method is validated by EOFY 2026 and is the plan case. The tool is now set to Low Repeat, which matches our own repeat research, and recommends zero to two hype days with a lean towards none; the plan keeps two low-spend hype days ($2.1k each). The room confirms the base week and the spend ceiling.")

S["eeinputs"]=content("eeinputs","EE tool inputs (23 Sep run), checked",
 table(["Input in the tool","Tool value","Calendar / Shopify value","Status"],[
  ["2025 BFCM event revenue","$710,000","$710,170 = all of November; the 14-day sale was $585k","Confirmed, month basis"],
  ["Weekly BAU revenue","$95,000","July $92.7k, August $119k, Aug to Sep run rate $118k","Chosen: conservative"],
  ["BAU MER and sale MER","27% and 25% (24% effective)","Aug 30%, Sep 28%, YTD 27.5%; Nov 2025 sale 24%","Confirmed"],
  ["Revenue curve","Custom, on","19 / 12 / 5 a day / BF 7 / CM 8 / last day 9: the 2025 shape","Confirmed"],
  ["Product cost %","30%","Calendar driver 32% landed; 2026 actual 33% of revenue","Set to 32%"],
  ["GST","8%","Nov 2025 ran 6% (27% of the sale was international); BAU 8 to 9%","Confirmed for the sale"],
  ["Daily fixed costs","$2,707","$83,905/month from Aug 2026 (preloaded year)","Confirmed"],
  ["AOV and weekly orders","$279 and 341","Nov 2025 sale $328, Aug 2026 $316; items 2,942 consistent","Orders (3,896) about 400 high; revenue unaffected"],
  ["Gift uptake at $299 / $599","18% / 6%","43% / 15% of 2025 sale orders cleared those spends","Set to 43 / 15 if the gift is automatic"],
  ["Stock at RRP","$950,000 (109% sell-through)","At 15% off the stock yields $807k, so $1.04M is 128% sell-through","Open: incoming stock or trim"],
  ["Dates","Wed 18 Nov to Tue 1 Dec","Decision: Thu 19 Nov to Wed 2 Dec, hype 17 to 18","Shift the tool and its files one day"],
  ],[22,16,42,20],size=22),
 src="EE calendar 2025 and 2026, Shopify, EE BFCM tool export 23 Sep",notes="Two rounds of corrections are now in the tool: fixed costs, spend bracket, sale MER, the curve and the base week. Three inputs are still open and each moves profit: product cost, gift uptake and stock. Also confirmed: Sept and Oct 2025 revenue $566,323; Hybrid, $3K+ a day, Experienced; packaging $2, shipping $24 and merchant fees 2% (2.1% in Nov 2025).")

moves=[("1 · Start wider","Test USA, NZ, TikTok and YouTube on a fixed budget with a kill rule. 70% of launch buyers are new."),
       ("2 · 13 days, 2-day hype","Thu 19 Nov to Tue 1 Dec. Hype Tue 17 and Wed 18 Nov to a new, cold audience, landing on a capture page."),
       ("3 · Stronger theme","All Aussie Earthmoving Adventures: one character, Jack Clacker, across four locations, four shoot days, cut down for paid social."),
       ("4 · Cut and run","Written stop rules: landing page under 1.5% by midday, or two days over 30% spend-to-revenue."),
       ("5 · Mid-sale drop","Mon 23 Nov: a new content drop and the gifting angle, to cold audiences in the gifting segment."),
       ("6 · Pre-game check","Pages built and tracked by 13 Nov, popup reach above 50% on paid pages, ad sets and sends scheduled before hype on 17 Nov."),
       ("7 · Better reactivation","Email and SMS to the 12,745 first-time buyers of the last year; grease reorder nudges."),
       ("8 · Beat the hangover","December without another discount: gift guide, new product, shipping cut-offs. July after EOFY lost money.")]
pregame=[("Popup reach above 50% on paid pages","15 Oct"),("Bundle, DiggerShield and gift-tier margins signed off","30 Oct"),("Stock cover confirmed or hero list trimmed","30 Oct"),("EE tool and shared calendar re-dated","30 Oct"),
         ("Warehouse shoot and stock check","6 Nov"),("Gift stock reserved: wipes, magnet mats, drawbars","10 Nov"),("Hero edit locked; hype teasers ready","10 Nov"),("Sale, bundle, collection and capture pages live","13 Nov"),
         ("Tracking QA: cart, checkout and orders on every page","13 Nov"),("Sale popup live (early access or bonus gift)","13 Nov"),("Offer rules sheet to customer service","13 Nov"),("Mid-sale content drop and PRO Mat gifting creative ready","16 Nov"),
         ("Ad sets and sends scheduled; cold traffic to product pages","16 Nov"),("Gift entry, gift guide and cut-off banner built","20 Nov"),("Hangover plan and new product launch briefed","20 Nov")]
S["moves"]=content("moves","Eight moves for 2026",
 f'<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:18px; flex:1">'+"".join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{"#ffffff" if i%2 else Y40}; padding:22px 24px; border:2px solid {K}"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; line-height:1.1; text-transform:uppercase">{t}</h3><p style="font-size:25px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate(moves))+'</div>'
,
 gap=20,src="Planning notes, 2025 sale review",notes="The eight moves from the strategy page of the notes, each with the number behind it.")

S["unit"]=content("unit","Profit per sale order: the tool&#39;s number and the corrected number",
 table(["Per sale order (with gift, 18% / 6% uptake in the tool)","EE tool, latest run","Corrected (product 32%, gift uptake at the 2025 order spread)"],[
  ["Revenue per order","$266.28","$266.28 (fewer, larger orders if AOV holds at 2025 sale levels)"],
  ["GST","$19.72 (7.4%)","$19.72: confirmed against Nov 2025"],
  ["Media at 24.7% MER","$65.81","$65.81"],
  ["Variable costs incl. gifts","$128.85 (48.4%)","about $139.20 (52.3%): +$5.33 product cost, +$5.03 gifts"],
  ["Fixed costs per order","$11.73","$11.73"],
  ["Profit per order","$40.16 (15.1%)","about $30 (11.2%)"],
  ["Total profit on 3,691 orders","$148,231 (after $10k of hype-day losses)","about $110k"]],[36,26,38],size=24)
 +note("Estimates: the tool&#39;s formula is not fully visible, so the corrected column moves each line by the input difference only. Three tool inputs stay open and each moves profit: product cost (30% in the tool, 32% in the calendar), gift uptake (the tool still has the old $299 / $599 tiers; the new $399 / $599 / $799 tiers were cleared by 29% / 15% / 6% of 2025 sale orders) and stock cover ($900k at RRP is 128% sell-through at the plan after the 15% discount, about $255k RRP short)."),
 src="EE BFCM tool section 7 (latest run), EE calendar drivers, Shopify 2025 order values",notes="The sale is profitable at about three quarters of what the tool shows. Product cost and gift uptake are the two open inputs.")

S["channels"]=content("channels","Channel plan: who does what",
 table(["Channel","Job in the sale","Audience","Destination","Owner"],[
  ["Meta paid social","Acquisition: new customers at launch and through the plateau","Cold prospecting; retargeting; email list match","Cold to grease and PRO Mat product pages; warm to the sale page","Paid [name]"],
  ["Email","Launch, daily drops, mid-sale, close, hangover","Full database twice (launch, last day); engaged segments for the rest","Sale page, bundle page, drop of the day","Email [name]"],
  ["SMS","The 3:30 PM drop moment; launch and last-hours alerts","SMS list, engaged buyers","Drop of the day","Email [name]"],
  ["Organic social and creators","The theme: Adventure episodes, cut-downs, behind the scenes; UGC","Followers, shares, creator audiences","Sale page with episode cards","Creative [name]"],
  ["Site","Sale page, bundle page, collection, homepage takeover, capture page, sale popup","All traffic","","Web [name]"],
  ["Partnerships","Tutorial content with Ivan (Earthworks Hub); collaboration moment mid-sale","Operator audience","Sale page","Growth [name]"],
  ["Test markets","USA, NZ prospecting; TikTok and YouTube in AU","Cold","Product pages","Paid [name]"]],[16,26,22,22,14],size=23),
 src="Planning notes, 2025 send log, landing page review",notes="Owners are placeholders for the team to fill. The split that matters most is cold traffic to product pages and warm traffic to the sale page.")

S["paid"]=content("paid","Paid media plan: the EE budget and how to shape it",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Budget (EE tool, latest run)",["Total $242,893 = 24.7% of $983k (sale MER 25%, conservative hype): Meta $221,033 (91%), TikTok $17,003 (7%), Google $4,858 (2%)","Hype days $2,101 each, as the tool now leans to no hype; sale days $17,049 each (smoothed)","Ceiling 28% = $275k; 2025 ran at 24%, so the plan holds at last year&#39;s efficiency","Test markets (USA, NZ, TikTok, YouTube) sit inside the 9% non-Meta share plus one TOF campaign, each with a day-4 kill rule"],accent=Y,lsize=24)
 +card("Meta structure (from the campaign plan)",["Sale campaigns about 55% of Meta: TOF (best-TOF duplicate, ASC broad, CIBS optional), TOM (ASC excluding customers; no-exclusions for the mid-sale offer), MOF, BOF","Evergreen about 45%: TOF interest and broad, Advantage+, MOF, BOF","Hype days on warm sale campaigns and evergreen only; sale TOF starts on day 1","Cold TOF lands on grease and PRO Mat product pages; TOM/MOF/BOF on the sale page"],accent=K80,lsize=24)
 +card("Shape it to the curve",["Smoothed spend gives day-1 MER 9%, plateau days 35%, Black Friday 25%, the last two days 19 to 22%: plateau days clear only $2k each","Shaped (&#39;clunky&#39;) spend from the tool: $46k day 1, $29k day 2, $12k plateau days, $17k Black Friday, $19k and $22k on the last two days","Recommendation: shaped spend; hold plateau days at $12k and add to the last two days only if day-12 MER is under 25%","Daily 8 AM check with the cut rules on the measurement slide"],accent=Y,lsize=24)+'</div>',
 src="EE BFCM tool sections 8 and 9 (latest run), campaign plan",notes="The Meta campaign plan file needs a fresh export: the 23 Sep file totals $219,550; the latest tool run puts Meta at $221,033.")

S["emailplan"]=content("emailplan","Email and SMS plan",
 f'<div style="display:flex; gap:24px">{big("29.4%","of popup signups buy; about 85% of that in the first month. Emails collected now pay now.")}{big("4 to 7%","of pre-sale signups who had not bought went on to buy during a sale. Capture is not a launch-day payload.",bg="#ffffff")}{big("43%","returning-customer share on Cyber Monday 2025 after a segmented send; blasts left it flat.")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("October to 13 November",["Restore popup reach on paid pages; then capture continuously","Split the welcome flow by the popup interest answer: grease offer and reorder cadence, or machine-fit guide","Reactivation to the 12,745 first-time buyers of the last year","Build the segments: engaged 30 and 90 days, grease buyers, SMS list"],accent=Y,lsize=24)
 +card("Hype and sale",["Hype sends to a first-access capture page with a countdown","Sale-specific popup (early access or bonus gift), not a discount","Full database on launch and last day only; engaged segments for everything else","3:30 PM drop by SMS daily and by email to the engaged segment","Christmas gifting from the mid-sale push on 23 Nov"],accent=K80,lsize=24)
 +card("After the sale",["Thank-you and gift guide on 2 Dec; shipping cut-off reminders 2 and 9 Dec","New product launch send","No December list buying: December signups convert worst (21.7%)","Grease reorder nudge at about 90 days for sale buyers"],accent=Y,lsize=24)+'</div>',
 src="Shopify, Klaviyo, Alia",notes="Full-database sends twice, segments for the rest. That is the single biggest change to the email plan.")

S["tests"]=content("tests","Test markets: start wider, with a kill rule written down",
 table(["Test","Budget cap","Runs","Passes if (proposal)","Stops if"],[
  ["USA prospecting","[$ ]","Hype plus the first four sale days","Spend-to-revenue at or under 35% and cost per order at or under $120 by day 4","Either miss at day 4: prospecting off, retargeting stays"],
  ["New Zealand prospecting","[$ ]","Same","Same","Same"],
  ["TikTok, Australia","[$ ]","Hype plus the first four sale days","Landing conversion at or above 1.5% and spend-to-revenue at or under 35%","Miss at day 4: off"],
  ["YouTube, Australia","[$ ]","Same","Same","Miss at day 4: off"]],[22,12,24,26,16],size=24)
 +note("Thresholds are proposals set above the 28% sale ceiling to give a test cell room. International earned 27% of 2025 sale revenue ($147k) at a $570 average order, so the question is not whether to spend there but how to keep it efficient: the US and NZ tests run with a budget and a kill rule. Budgets are for the room to set."),
 src="Planning notes, Shopify sessions by country",notes="The point is that cut and run is decided before the sale starts.")

S["hangover"]=content("hangover","Reactivation before, and beating the hangover after",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Before the sale",["12,745 first-time buyers in the last 12 months, most with no reason yet to return","Grease reorder nudge at about 90 days and a 40-piece pack upsell (the stickiest variants, 14 to 15% repeat)","Second-machine angle for cover buyers: universal covers repeat at 9% because owners cover more machines","Segmented sends only"],accent=Y)
 +card("December",["July 2026, after EOFY, ran a 42% spend-to-revenue ratio and a loss. December is the same risk","Hangover plan that is not another discount: new product launch, Christmas gift guide, the last knock-off of the year","Shipping cut-off on every gift surface from 2 Dec; reminder 9 Dec","December signups are the weakest cohort (21.7% buy): spend on buyers, not on list growth"],accent=K80)+'</div>',
 src="Shopify, H2 forecast, signup cohorts",notes="Moves 7 and 8 with the numbers behind them.")

# ------------------------------------------------------------------ 03 OFFER & CREATIVE
S["s-offer"]=section("s-offer","03","Offer and creative","What is on sale, the rules around it, the daily drops, the gifting path, and the theme and shoot that carry it.")

S["offer"]=content("offer","Offer architecture",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Sitewide",["Up to 25% off, grease excluded","DiggerShield: $150 / $200 off instead of a percentage (amounts to confirm against margin)","Percentage plus gift rather than a flat-dollar sitewide offer, to protect basket size"],accent=Y,tsize=32,lsize=26)
 +card("Gift with purchase",["$399: Digger Wipes + free shipping","$599: Digger Wipes + free shipping + Magnet Tool Mat","$799: Digger Wipes + free shipping + Magnet Tool Mat + Drawbar Cover","In 2025, 29% of sale orders cleared $399, 15% cleared $599 and 6% cleared $799"],accent=K,tsize=32,lsize=26)
 +card("Bundles",["Hardcore Tradie, 30% off: $777 (RRP $1,110). 2× PRO Mat Plus, hoodie, drawbar; $244 of gear free","Ultimate Earthmover: $732 (RRP $1,474). Pro Enclosure, PRO Mat Plus, drawbar 35% off; $347 of gear free","Owner Operator: $778 (RRP $1,987). The Hauler, 2× PRO Mat Plus 35% off; $790 of gear free","Existing bundles stay live at sale pricing. Full contents on the next slide"],accent=Y,tsize=32,lsize=26)+'</div>'
 +note("Excluding grease is a decision with a number attached: the grease system was 33% of the 2025 sale and grease packs carried a 14% discount. Options: exclude it and accept a smaller grease share, or feature grease packs as a hero offer instead of a sitewide cut. The $399 free-shipping tier matches the existing signup offer, which converts signups at 37%."),
 src="Planning notes, customer records",notes="The sale format page of the notes, with the reason for each piece.")

S["rules"]=content("rules","Offer rules and open questions",
 table(["Rule","Proposal","Status"],[
  ["Discount mechanic","Automatic sitewide discount, no code; bundles as fixed-price products; gift tiers as automatic free gifts at the thresholds","To confirm with Web"],
  ["Stacking","Gift tiers apply to the discounted subtotal; bundles do not stack with the sitewide percentage; no code stacking","To confirm"],
  ["Exclusions","Grease, gift cards, items already inside a bundle, [any other]","To confirm"],
  ["Price integrity","No price changes from 1 Nov except the DiggerShield test, which ends before hype","Decision this week"],
  ["Daily drops","One extra deal per day at 3:30 PM AEDT; 24 hours or while stocks last; announced by SMS and email","To confirm"],
  ["International","27% of 2025 sale revenue at a $570 average order. Same offer in AUD; free-shipping tier AU only; gift tiers AU only unless stock allows","Decision"],
  ["Price protection","Customers who bought in the 7 days before launch: [policy]","Decision"],
  ["Returns","Standard policy; bundles returned whole","To confirm"]],[20,58,22],size=24),
 src="Planning notes",notes="These are the questions customer service and the web team will be asked on day one. Settle them before the hype sends.")

def bcard(title, items, total, price, bg="#ffffff", accent=Y):
    rows="".join(f'<div style="display:flex; justify-content:space-between; gap:12px; border-bottom:1px solid #d9d5cc; padding:3px 0"><span>{a}</span><span style="white-space:nowrap">{b}</span></div>' for a,b in items)
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:22px 24px; border:2px solid {K}; border-top:12px solid {accent}">'
            f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; line-height:1.1; text-transform:uppercase">{title}</h3>'
            f'<div style="font-size:22px; line-height:1.3; color:{K90}; display:flex; flex-direction:column">{rows}</div>'
            f'<div style="display:flex; justify-content:space-between; font-size:23px; font-weight:700; border-top:2px solid {K}; padding-top:6px"><span>RRP total</span><span>{total}</span></div>'
            f'<div style="display:flex; justify-content:space-between; font-size:26px; font-weight:700; background:{K}; color:{W}; padding:6px 10px"><span>Bundle price</span><span>{price}</span></div></div>')
S["bundles"]=content("bundles","Three hero bundles: contents, RRP and price",
 f'<div style="display:flex; gap:20px; flex:1">'
 +bcard("Hardcore Tradie · 30% off",[("2× PRO Mat Plus","$598"),("1× Drawbar Cover","$129"),("1× Proper Thicc Hoodie","$139"),("10× Digger Wipes","$150"),("1× Boom Bottle Opener","$15"),("1× Magnet Tool Mat","$79")],"$1,110","$777",accent=Y)
 +bcard("Ultimate Earthmover · 40% off",[("1× Pro Excavator Enclosure","$699"),("1× Drawbar Cover","$129"),("1× PRO Mat Plus","$299"),("10× Digger Wipes","$150"),("1× Magnet Tool Mat","$79"),("1× Hydraulic Coupling Cap Set","$15"),("1× Excavator Phone Cradle","$39"),("1× Drink / Tool Caddy","$49"),("1× Boom Bottle Opener","$15")],"$1,474","$884",accent=K)
 +bcard("Ludicrous · 50% off",[("1× The Hauler Luggage Bag","$599"),("2× PRO Mat Plus","$598"),("2× Magnet Tool Mat","$158"),("1× Drawbar Cover","$129"),("1× Quicky Cover","$129"),("1× Proper Thicc Hoodie","$139"),("1× Boom Bottle Opener","$15"),("20× Digger Wipes","$300"),("1× Drink / Tool Caddy","$49")],"$2,116","$1,058",accent=Y)+'</div>'
 +note("RRP from the store: The Hauler at its full $599 (currently selling at $399); Quicky Cover at $129 (tan is $119); phone cradle strap mount at $39 (suction cup $49). Margin and component stock need a costing pass by 30 October.",size=22),
 src="Shopify product prices, 24 Sep 2026",notes="Bundle price = RRP total less the bundle discount, rounded to the dollar. The Ludicrous Bundle is now the headline: over $2,100 of gear for $1,058.")

drops=[("Wed 18","Launch day: whole offer live, no drop"),("Thu 19","Grease 40-piece pack deal (grease was a third of last year&#39;s sale)"),("Fri 20","PRO Mat Plus colour of the day"),("Sat 21","Quicky Cover"),("Sun 22","DiggerShield $200 day"),("Mon 23","Mid-sale push: new content drop and PRO Mat gifting angle; Christmas gift collection launches"),("Tue 24","Gift-tier push: $399, $599 and $799 gift levels"),
       ("Wed 25","Phone cradle and accessories kit (gifts under $150)"),("Thu 26","Universal and engine covers"),("Fri 27","Black Friday: Mystery Box and the Ludicrous Bundle"),("Sat 28","Grease reorder deal"),("Sun 29","Pro Enclosure"),("Mon 30","Cyber Monday: Hardcore Tradie Bundle"),("Tue 1 Dec","Last knock-off of the year: free shipping on everything")]
S["drops"]=content("drops","Knock-off drop calendar (draft for the team)",
 f'<div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px 28px">'+"".join(f'<div style="display:flex; gap:16px; align-items:center; border-bottom:1px solid {K}; padding:0 0 8px 0"><p style="font-family:{DISP}; font-size:26px; width:120px; letter-spacing:1px">{d}</p><p style="font-size:25px; line-height:1.25; flex:1">{t}</p></div>' for d,t in drops)+'</div>'
 +note("One drop a day at 3:30 PM AEDT, 24 hours each; the mid-sale push on Mon 23 is a new content drop and a PRO Mat gifting angle with the Christmas gifting launch; Black Friday keeps the Mystery Box. Timing checks out: the 6 to 9 PM block was the biggest buying window in 2025 (115 to 120 orders an hour). Order is a draft; stock and margin per drop to confirm."),
 src="Planning notes, concept board",notes="Thirteen days, twelve drops. The team owns the final order; the mechanic is the point.")

def acard(title, rows, pay, rrp, free, bg="#ffffff", accent=Y, save=""):
    out=""
    for item,r,price in rows:
        is_free=(price=="FREE")
        tag=(f'<span style="background:{Y}; color:{K}; font-weight:700; padding:0 8px">FREE</span>' if is_free else f'<span style="font-weight:700">{price}</span>')
        out+=(f'<div style="display:flex; gap:10px; border-bottom:1px solid #d9d5cc; padding:3px 0; align-items:center"><span style="flex:1">{item}</span>'
              f'<span style="text-decoration:line-through; color:{MUTE}; white-space:nowrap">{r}</span><span style="width:86px; text-align:right; white-space:nowrap">{tag}</span></div>')
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:22px 24px; border:2px solid {K}; border-top:12px solid {accent}">'
            f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; line-height:1.1; text-transform:uppercase">{title}</h3>'
            f'<div style="font-size:22px; line-height:1.3; color:{K90}; display:flex; flex-direction:column">{out}</div>'
            f'<div style="display:flex; justify-content:space-between; font-size:23px; font-weight:700; border-top:2px solid {K}; padding-top:6px"><span>{free} of gear free</span><span style="color:{MUTE}; text-decoration:line-through">{rrp}</span></div>'
            f'<div style="display:flex; justify-content:space-between; font-size:26px; font-weight:700; background:{K}; color:{W}; padding:6px 10px"><span>You pay</span><span>{pay}</span></div>'
            +(f'<p style="font-size:22px; font-weight:700; text-align:right">{save}</p>' if save else '')+'</div>')
S["bundles-alt"]=content("bundles-alt","Three hero bundles: pay for the hero gear, the rest is free",
 f'<div style="display:flex; gap:20px; flex:1">'
 +acard("Hardcore Tradie · 30% off",[("2× PRO Mat Plus","$598","$538"),("1× Proper Thicc Hoodie","$139","$125"),("1× Drawbar Cover","$129","$114"),("10× Digger Wipes","$150","FREE"),("1× Magnet Tool Mat","$79","FREE"),("1× Boom Bottle Opener","$15","FREE")],"$777","$1,110","$244",accent=Y,save="Save $333: 30% off RRP")
 +acard("Ultimate Earthmover · 35% off the hero gear",[("1× Pro Excavator Enclosure","$699","$454"),("1× PRO Mat Plus","$299","$194"),("1× Drawbar Cover","$129","$84"),("10× Digger Wipes","$150","FREE"),("1× Magnet Tool Mat","$79","FREE"),("1× Drink / Tool Caddy","$49","FREE"),("1× Excavator Phone Cradle","$39","FREE"),("1× Hydraulic Coupling Cap Set","$15","FREE"),("1× Boom Bottle Opener","$15","FREE")],"$732","$1,474","$347",accent=K,save="Save $742: 50% off RRP")
 +acard("Owner Operator · 35% off the hero gear",[("1× The Hauler Luggage Bag","$599","$389"),("2× PRO Mat Plus","$598","$389"),("20× Digger Wipes","$300","FREE"),("1× Proper Thicc Hoodie","$139","FREE"),("1× Drawbar Cover","$129","FREE"),("2× Magnet Tool Mat","$158","FREE"),("1× Drink / Tool Caddy","$49","FREE"),("1× Boom Bottle Opener","$15","FREE")],"$778","$1,987","$790",accent=Y,save="Save $1,209: 61% off RRP")+'</div>'
 +note("Hardcore Tradie is 30% off the whole RRP: the hero items take about 10% and the rest is free. Ultimate Earthmover and Owner Operator take 35% off the hero gear and everything else is $0, which works out at 50% and 61% off RRP. Store RRPs, The Hauler at its full $599. Margin sign-off on the two deeper bundles by 30 Oct.",size=22),
 src="Shopify product prices, 24 Sep 2026",notes="The story is \"buy the hero gear, get the rest free\" instead of a single percentage. Owner Operator replaces the Ludicrous bundle, without the Quicky Cover.")

terr=[("Red dirt + country pub","A changing world","The local country pub, where robots now pull the beers. The long-haul truck run from the bush to the big smoke. Dust trail, campfire at night.","Act 1 and the finale: the world has changed and the call comes at the pub, and he brings the lessons home to it. Hype starts here.","&#39;Show these city boys how it&#39;s done.&#39;","PRO Mat · small covers"),
      ("Warehouse","Getting the call","Bundles, offers, the forklift loading the ute. The boys show Jack what they&#39;ve been up to.","Act 2 and the launch: he meets the DiggerLid boys and his Black Friday shopping pile starts.","Straight product proof.","Grease · accessories · bundles"),
      ("Paddock","Sharing his &#39;wisdom&#39;","The excavator at work in real conditions and the big dog. Practical and authentic.","Act 3: the gear gets tested; his messy methods against better ways.","&#39;Talk slow for earthmovers.&#39;","Pro Enclosure"),
      ("Worksite","The brand realisation","A home build site with a backyard that needs digging. Real operators, including Ivan from Earthworks Hub, rate the gear.","Act 4 and the mid-sale gifting angle: the gear is so good he has to get some for his mates.","&#39;How you might have done it: a history lesson.&#39;","PRO Mat · small covers · grease")]
S["territories"]=content("territories","Four backdrops",
 f'<div style="display:flex; gap:18px; flex:1">'+"".join(
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{"#ffffff" if i%2 else Y40}; padding:22px 22px; border:2px solid {K}; border-top:12px solid {K if i%2 else Y}">'
 f'<p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; color:{MUTE}">{i+1} · {role}</p>'
 f'<h3 style="font-family:{HEAD}; font-size:36px; font-weight:700; text-transform:uppercase; line-height:1">{loc}</h3>'
 f'<p style="font-size:23px; line-height:1.3"><b>What we shoot:</b> {shoot}</p>'
 f'<p style="font-size:23px; line-height:1.3"><b>In the story:</b> {story}</p>'
 f'<p style="font-size:23px; line-height:1.3; font-style:italic; color:{K90}">{line}</p>'
 f'<div style="margin-top:auto; background:{K}; color:{W}; padding:8px 12px; font-size:23px; font-weight:700">{prod}</div></div>'
 for i,(loc,role,shoot,story,line,prod) in enumerate(terr))+'</div>'
 +note("4 locations · 4 shoot days: 1, 2, 27 and 28 Oct · theme: All Aussie Earthmoving Adventures. Each location owns a product, and every hype teaser, cut-down and still comes from the same footage.",size=24),
 src="Planning notes, creative production page",notes="Ordered as the journey runs: the country pub and the truck run to the city, the warehouse, the paddock, the home build site, then home to the pub. The next slide draws the route.")
S["territories"]=S["territories"].replace(f"; border-top:12px solid {Y}\">","\">")

stops=[("1","Red dirt + pub","A changing world","Ep 1 · Tue 17 Nov","AI took the jobs; robots pull the beers. The boys call; he hitches a truck to the big smoke."),
       ("2","Warehouse","Getting the call","Ep 2 · Thu 19 Nov","He drops in on the boys, sure they want his wisdom. His shopping pile starts."),
       ("3","Paddock","Sharing his &#39;wisdom&#39;","Ep 3 · Sat 21 Nov","The Pro Enclosure gets tested. He questions every better way, then adopts it."),
       ("4","Worksite","The brand realisation","Ep 4 · Mon 23 Nov","A backyard dig. The gear is so good he gets some for his mates, the husband, the habibi."),
       ("5","The country pub","Bringing the lessons home","Finale · Sun 29 Nov","Last drinks with a ute of bargains; he teaches the robots. &#39;Tell &#39;em I sent you.&#39;")]
ads=[("Hype · 17 to 18 Nov","10 ads","Bucket Head · Airwalk · Hey dighead","&#39;Kids and their AI. What&#39;s the world coming to?&#39;","A hype ad from each location, plus top performers.","Coming Thu 19 Nov: up to 25% off + free gifts + huge bundles. Early access.",None),
     ("Launch · Thu 19 Nov","20 ads incl. launch wk","Frosty Cold Ones","&#39;So what have you boys been working on?&#39;","Jack finds all the new gear the boys have built.","Up to 25% off + free gifts + huge bundles. Ends 1 Dec.",None),
     ("Launch wk · 20 to 22 Nov","In the 20","The Real Deal","&#39;Now this thing is the real deal.&#39;","Pro Enclosure deep dive: rain comes down, machine stays dry.","Ultimate Earthmover $732: $347 of gear free.",None),
     ("Gifting · 23 to 28 Nov","13 ads, all new","Too Good To Keep","&#39;Too good to keep to yourself.&#39;","For your mates, your husband, your habibi, plus the Titan Sox × DiggerLid × 3D Pro bundle.","Shop the Christmas gifting page: up to 25% off.",("Black Friday","27 Nov")),
     ("Ending · 29 Nov to 1 Dec","6 ads","Last Drinks","&#39;3 days left&#39; &gt; &#39;Last day. Last drinks.&#39;","Countdown from Sunday; Jack calls last drinks.","Ends midnight Tue 1 Dec.",("Cyber Monday","30 Nov"))]
xs=[166,499,832,1165,1498]
road=(f'<svg aria-label="Journey route: red dirt and the pub, warehouse, paddock, worksite, then home to the country pub" viewBox="0 0 1664 64" style="width:1664px; height:64px; flex-shrink:0">'
      f'<path d="M166 32 C 300 0, 380 0, 499 32 S 700 64, 832 32 S 1040 0, 1165 32 S 1380 64, 1498 32" fill="none" stroke="{K}" stroke-width="5" stroke-dasharray="16 10"/>'
      +"".join(f'<circle cx="{x}" cy="32" r="28" fill="{Y if n in (0,4) else (K if n%2 else W)}" stroke="{K}" stroke-width="4"/><text x="{x}" y="44" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="34" fill="{W if n%2 else K}">{n+1}</text>' for n,x in enumerate(xs))
      +'</svg>')
def adcard(phase,vol,concept,hook,shows,offer,peak):
    pk=(f'<div style="display:flex; justify-content:space-between; align-items:center; gap:8px; background:{K}; color:{Y}; padding:4px 10px; margin:-8px -12px 2px"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; white-space:nowrap">★ {peak[0]}</p><p style="font-family:{DISP}; font-size:22px; color:{W}; white-space:nowrap">{peak[1]}</p></div>' if peak else '')
    return (f'<div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:4px; background:{Y}; color:{K}; padding:8px 12px; border:2px solid {K}; font-size:22px; line-height:1.2">'
            +pk+f'<div style="display:flex; justify-content:space-between; gap:6px"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; color:{MUTE}">{phase}</p></div>'
            f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; background:{K}; color:{Y}; padding:1px 8px; align-self:flex-start">{vol}</p>'
            f'<p style="font-family:{HEAD}; font-size:24px; font-weight:700; text-transform:uppercase; line-height:1.05">{concept}</p>'
            f'<p style="font-weight:700">{hook}</p><p>{shows}</p>'
            f'<p style="font-weight:700; border-top:1px solid {K}; padding-top:3px">{offer}</p></div>')
S["journey"]=content("journey","The hero narrative: organic social &gt; paid",
 f'<div style="display:flex; gap:18px">'+"".join(
 f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; border-top:4px solid {K}; padding-top:6px">'
 f'<div style="display:flex; justify-content:space-between; align-items:baseline; gap:6px"><h3 style="font-family:{HEAD}; font-size:26px; font-weight:700; text-transform:uppercase; line-height:1"><span style="font-family:{DISP}; background:{K}; color:{Y}; padding:0 8px; margin-right:8px">{num}</span>{loc}</h3></div>'
 f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; background:{Y}; padding:1px 8px; align-self:flex-start">{date}</p>'
 f'<p style="font-size:22px; font-weight:700; color:{MUTE}; text-transform:uppercase; letter-spacing:.5px; line-height:1.15">{act}</p>'
 f'<p style="font-size:22px; line-height:1.22; color:{K90}">{beat}</p></div>'
 for num,loc,act,date,beat in stops)+'</div>'
 +f'<div style="display:flex; align-items:center; gap:16px; background:{K}; color:{W}; padding:8px 18px"><p style="font-family:{DISP}; font-size:26px; letter-spacing:1px; text-transform:uppercase; color:{Y}; white-space:nowrap">Organic social</p><p style="font-size:22px; line-height:1.25">One episode per location. Episode viewers and early-access sign-ups feed launch and ending-soon retargeting; hype and gifting stay cold.</p></div>'
 +f'<p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; text-align:center">▼ ladders down to performance ads: each one works cold, on its own ▼</p>'
 +f'<div style="display:flex; gap:18px; flex:1; min-height:0">'+"".join(adcard(*a) for a in ads)+'</div>',
 gap=12,src="Creative plan, shoot schedule, concept storyboards",notes="Organic: one episode per location. Ep 1 red dirt Tue 17 Nov with hype; Ep 2 warehouse Thu 19 Nov with launch; Ep 3 paddock Sat 21 Nov in launch week; Ep 4 worksite Mon 23 Nov with the gifting drop; the pub finale Sun 29 Nov as ending soon starts. Paid: 49 ads as on the creative volume slide (hype 10, launch 20 across launch day and launch week, gifting 13, ending soon 6). Black Friday (Fri 27 Nov, day 9) sits in the gifting phase and Cyber Monday (Mon 30 Nov, day 12) in ending soon: both get their own push. Hand-off: episode viewers and early-access sign-ups feed retargeting for launch and ending soon; hype and gifting run to cold audiences. Every paid ad still works cold: hook, product proof, offer and date. Concept storyboards are in the amendment at the back.")

S["gifting"]=content("gifting","Christmas gifting guides",
 f'<div style="display:flex; gap:24px">{big("34%","of PRO Mat Plus buyers are women, in practice gift buyers. Gifting is themed for spouses and family.")}{big("1 page","its own Christmas gifting landing page. Every gift ad, email, SMS and banner lands there, not on the sale page.",bg="#ffffff")}{big("3 brands","a collab gift bundle: Titan Sox × DiggerLid × 3D Pro. Contents and price TBC.")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("On the page",["The Titan Sox × DiggerLid × 3D Pro collab bundle up top","PRO Mat Plus as the hero gift, all four colours","The three bundles from $732; gift with purchase at $399, $599, $799","Cut-off dates by state; gift note at checkout"],accent=Y)
 +card("Driving to it",["Its own gifting ads: 13 all new from 23 Nov: 5 video, 5 image, 3 UGC","Jack&#39;s episode 4: &#39;Too good to keep to yourself&#39;, for your mates, your husband, your habibi","Gift guide email and SMS; gift banner and a Christmas link in the navigation"],accent=K)
 +card("What not to repeat",["The Father&#39;s Day gift page converted 0.5%: generic, with no product depth","Gift traffic sent to the sale page, which leads with grease","Leaving the shipping cut-off implicit"],accent=K80)+'</div>',
 src="PostHog, Shopify, campaign calendar",notes="Spouse and family themed gifting on its own landing page, live from the mid-sale push on 23 Nov through Cyber Monday and into December. The page features a three-way collab bundle from Titan Sox, DiggerLid and 3D Pro; contents, price and stock are still to confirm with both partners. Gifting has its own ad concepts: the 13 all-new mid-sale ads on the creative slide. Ad offer: shop Christmas gifts, up to 25% off, ends 1 Dec.")

S["gifting"]=S["gifting"].replace(f"border:2px solid {K}; border-top:12px solid {Y}\">",f"border:2px solid {K}\">",1)
JACK_IMG="/_blob/f1f1d5c5a725aa67f5afa3a8027a3f7e"
jack_l=[("The old way","On the tools forty years, by his own count. From a long line of hard men, all &#39;retired at forty&#39;."),
        ("Wrong wisdom","Hands out old-man country know-how with total authority, and it&#39;s wrong every time."),
        ("Knows best","Rejects anything new on principle. His answer to every product: &#39;Never needed one.&#39;"),
        ("The lament","Is there still a place for an outback bushman in this new world of AI?"),
        ("Physical comedy","Clumsy, falls over constantly. Never notices, never reacts, never winks.")]
jack_r=[("Talks down to the young","Speaks slowly to young tradies because he thinks they&#39;re simple. They&#39;re always right."),
        ("Bad knees, bad back","He&#39;s got bad knees and a bad back. But doesn&#39;t everyone?"),
        ("Quietly coming around","Ends up using DiggerLid gear. Never admits it works; claims it was his idea all along."),
        ("Never cruel","Condescending but kind. Never mocks the customer, never angry for more than a beat."),
        ("Lovable at heart","Warm, engaging, always trying. All he wants is to share what he knows.")]
def jtrait(t,d,side):
    line=f'<div style="flex:0 0 44px; height:3px; background:{K}; align-self:center"></div>'
    txt=(f'<div style="flex:1; display:flex; flex-direction:column; gap:2px; text-align:{"right" if side=="l" else "left"}">'
         f'<p style="font-family:{HEAD}; font-size:24px; font-weight:700; text-transform:uppercase; line-height:1.1">{t}</p>'
         f'<p style="font-size:22px; line-height:1.22; color:{K90}">{d}</p></div>')
    return f'<div style="display:flex; gap:12px">{txt+line if side=="l" else line+txt}</div>'
jack_q=[("G&#39;day, I&#39;m Jack Clacker, and this is my backyard.","Opens every cut."),
        ("Never needed one.","Said about every product, just before it proves him wrong."),
        ("Old trick.","The lead-in to bush wisdom that turns out to be wrong."),
        ("Another good day&#39;s work. / That&#39;s not going anywhere.",""),
        ("Been saying that for years.","")]
jack_b=[("1 · A changing world","AI took the town&#39;s jobs. Robots pull the beers at the pub."),
        ("2 · Getting the call","The DiggerLid boys call. Secretly keen, he loads the digger for the big smoke."),
        ("3 · Sharing his &#39;wisdom&#39;","Messy methods meet better ways. He questions each, then adopts it."),
        ("4 · The brand realisation","Tough people deserve better gear. He embraces it, claims he taught them."),
        ("5 · Bringing it home","A ute full of bargains for his robot mates. &#39;Tell &#39;em I sent you.&#39;")]
def jband(label, items, qmark=False):
    return (f'<div style="display:flex; gap:14px; background:{K}; padding:12px 18px; align-items:stretch; flex-shrink:0"><p style="font-family:{DISP}; font-size:26px; color:{Y}; letter-spacing:1px; text-transform:uppercase; align-self:center; flex:0 0 150px">{label}</p>'
            +"".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:2px; border-left:2px solid {Y}; padding-left:12px"><p style="font-size:22px; font-weight:700; color:{Y if not qmark else W}; line-height:1.15">{("&#39;"+q+"&#39;") if qmark else q}</p><p style="font-size:22px; color:{"#d6d3d4" if not qmark else GREY}; line-height:1.15">{d}</p></div>' for q,d in items)+'</div>')
S["jack"]=content("jack","Meet Jack Clacker: the hero of the sale",
 jband("Back&#8203;story",jack_b)
 +f'<div style="display:flex; gap:0; flex:1; min-height:0; align-items:stretch">'
 +f'<div style="flex:1; display:flex; flex-direction:column; justify-content:space-between">'+"".join(jtrait(t,d,"l") for t,d in jack_l)+'</div>'
 +f'<div style="flex:0 0 360px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0 0"><img src="{JACK_IMG}" alt="Jack Clacker, sketched: a smiling bushman in a wide-brim hat, squatting in a paddock with a DiggerLid mug, a mini excavator behind him" style="width:330px; height:100%; max-height:440px; object-fit:cover; object-position:center 25%; border:4px solid {K}; box-shadow:12px 12px 0 {Y}"></div>'
 +f'<div style="flex:1; display:flex; flex-direction:column; justify-content:space-between">'+"".join(jtrait(t,d,"r") for t,d in jack_r)+'</div></div>'
 +jband("Catch&#8203;phrases",jack_q,qmark=True),
 gap=16,src="Creative brief: character notes",notes="Backstory in full. 1 A changing world: AI has stolen all the jobs in his country town; at the pub, Tesla robots pull beers, occupy the bar and feed the pokies. &#39;Not much call for country wisdom around here anymore.&#39; 2 Getting the call: the DiggerLid boys call for help with their Black Friday sale; secretly keen to learn and eyeing the deals, he loads his excavator and heads for the big smoke. 3 Sharing his wisdom: messy, uncomfortable methods against better ways to grease, protect his excavator and look after his body; his shopping pile grows. 4 The brand realisation: protecting your machine, equipment and body is part of doing the job properly, and the BFCM deals make now the time to upgrade. 5 Bringing the lessons home: a ute full of bargains; &#39;Look after your machine, look after your body, and know when to grab a good deal.&#39; A robot films it. Close on the offer, deadline and shop CTA. Jack Clacker carries the hero narrative. He is the joke, never the customer: condescending but kind, wrong about everything, and quietly converted by the gear without ever admitting it.")

def beatcol(title, sub, beats, foot_, bg, fg=None, accent=Y):
    fg = fg or K
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; color:{fg}; padding:20px 24px; border:2px solid {K}; border-top:8px solid {accent}">'
            f'<p style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase; line-height:1.05">{title}</p>'
            f'<p style="font-size:22px; color:{GREY if bg==K else MUTE}; line-height:1.2">{sub}</p>'
            + "".join(f'<div style="display:flex; gap:12px; align-items:baseline"><p style="font-family:{DISP}; font-size:26px; color:{Y if bg==K else K}; flex:0 0 22px">{n}</p><p style="font-size:23px; line-height:1.22">{b}</p></div>' for n,b in enumerate(beats,1))
            + (f'<p style="margin-top:auto; font-size:22px; line-height:1.22; font-weight:700; border-top:2px solid {Y if bg==K else K}; padding-top:8px">{foot_}</p>' if foot_ else '')
            + '</div>')
arrow=f'<p style="font-family:{DISP}; font-size:30px; align-self:center; color:{K}">&#9654;</p>'
S["theme"]=content("theme","Theme: All Aussie Earthmoving Adventures",
 f'<div style="display:flex; gap:24px">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{K}; color:{W}; padding:22px 28px">{banner("The Great Black Friday Haul", bg=Y, fg=K, size=24)}'
 f'<p style="font-size:24px; line-height:1.3; color:{W}">A parody of the outback-bumbler format with our own character, Jack Clacker: wrong wisdom, four locations, and gear he rejects until he quietly uses it.</p></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{Y40}; padding:22px 28px; border:2px solid {K}">{banner("How it carries the sale", size=24)}'
 f'<p style="font-size:24px; line-height:1.3">Hype (17 and 18 Nov) teases Jack and the offer to a new, cold audience and drives sign-ups. Launch (Thu 19 Nov, midday) opens with the offer. A new episode lands at the mid-sale drop on 23 Nov.</p></div></div>'
 +f'<p style="font-family:{DISP}; font-size:26px; letter-spacing:1px; text-transform:uppercase">Adapting the format: from the joke to our hero film, our ads and our hype ads</p>'
 +f'<div style="display:flex; gap:14px; flex:1; min-height:0">'
 +beatcol("The original","The format we parody",["Intro","Physical comedy","Overstate / wrong knowledge","Criticise","Stuffs it up","Resolution, or lack of one"],"",W,accent=GREY)
 +arrow
 +beatcol("Hero film · 90 sec","Organic, one per location",["Intro + physical comedy","Overstate + criticise","Have it done the right way: the gear","Double down: &#39;how I&#39;d have done it&#39;","Sale details and CTA"],"Open loops bring people back.",K,fg=W)
 +arrow
 +beatcol("Our ad · 30 to 90 sec","Launch to last day, works cold",["Overstate knowledge + criticise, as the intro","Have it done the right way","Sale CTA"],"Hook, product proof, offer. No episode knowledge needed.",Y40)
 +arrow
 +beatcol("Hype ad · 15 to 20 sec","Hype 17 and 18 Nov, new cold audience",["Hook: a Jack gag in the first 3 sec","Tease: up to 25% off + free gifts + huge bundles, from Thu 19 Nov","Early access CTA"],"Short, loud, one joke. Bucket Head is the model.",W,accent=K)
 +'</div>',
 gap=18,src="Planning notes pp.10 and 11, concept board, format sketch",notes="The original format is intro, physical comedy, wrong knowledge, criticism, stuffing it up and an open resolution. Our 90-second hero keeps the comedy but lets the gear do it the right way while Jack claims he would have done it that way all along, then closes on the sale. The paid ad (30 to 90 sec) drops to three beats so it works for a cold viewer. The hype ad (15 to 20 sec) is the shortest cut: a gag hook, the offer teased, and early access; Bucket Head is the model. Hype builds the story and the sign-up list with the offer teased; launch carries the full offer. Hype traffic converted at about 1% in both past sales. Fallback launch film if the Adventure edit slips: Take Cover, already shot in July.")

locs=[("Paddock","Excavator; DiggerShield and the big dog; practical, authentic; possible Ivan cameo","Talk slow for earthmovers","Pro Enclosure · DiggerShield"),
      ("Worksite","Building an A-frame; backyard with the excavator; translating for tradies","How you might have done it: a history lesson","PRO Mat · small covers"),
      ("Red dirt","Dust trail; camping out; doors; night; campfire","Show these city boys how it is done","PRO Mat · small covers"),
      ("Warehouse","Bundle and offer shots; forklift","Straight product proof","Grease · accessories")]
S["production"]=content("production","Creative production: four locations, 2.5 shoot days, one safety day",
 f'<div style="display:flex; gap:20px; flex:1">'+"".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{"#ffffff" if i%2 else Y40}; padding:22px 24px; border:2px solid {K}; border-top:12px solid {Y if i%2==0 else K}"><h3 style="font-family:{HEAD}; font-size:32px; font-weight:700; text-transform:uppercase">{n}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{sh}</p><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">{ang}</p><p style="font-size:24px; line-height:1.3"><b>Products:</b> {pr}</p></div>' for i,(n,sh,ang,pr) in enumerate(locs))+'</div>'
 +f'<div style="display:flex; gap:24px">{big("4","locations, one character, one arc. Each episode is a location and each location owns a product.",bg="#ffffff")}{big("2.5","shoot days plus one safety day. Hype teasers, cut-downs and stills all come from the same footage.")}{big("13 Nov","the edit, pages and hype assets must be live. The Father&#39;s Day page went live four days after that sale started.",bg="#ffffff")}</div>',
 src="Planning notes p.10",notes="Shoot the warehouse day first: bundle and offer stills unblock the page build.")

S["character"]=content("character","The character: our own outback expert",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Character notes (from the planning session)",["G&#39;day, I&#39;m [name], and this is my backyard: the Aussie outback","Physical comedy: reverses over the esky, falls off the machine","Overstated knowledge of land and conditions","Criticises city folk and early settlers alike","Tries to help and wrecks it; the covered gear is the only thing that comes out fine","Shoddy recreations and bad history lessons"],accent=Y)
 +card("Keeping the homage safe",["Our own recurring character, for example Gravel Grant: khaki, hat, moustache","Parody the format and the archetype only","No show name, no actor name or likeness, no specific scenes or logos in paid media","Our own catchphrases and episode titles","Legal read on the edit before the first paid placement"],accent=K80)+'</div>'
 +note("The character carries on after the sale: grease how-not-tos, cover fit guides, tutorial content with Ivan from Earthworks Hub. The BFCM edit is season one."),
 src="Planning notes p.11, concept board")

cphases=[("Hype","17 to 18 Nov","Attention grab plus sale info in the statics, with cool visuals. New, cold audience.",{"Video":4,"Image":4,"GIF":2,"UGC":0}),
         ("Launch","From 19 Nov","The sale is live: the offer, the bundles and the end date.",{"Video":6,"Image":6,"GIF":4,"UGC":4}),
         ("Mid-sale","From 23 Nov","Gifting focus: PRO Mat as the gift, driving to the Christmas gifting page.",{"Video":5,"Image":5,"GIF":0,"UGC":3}),
         ("Ending soon","From 29 Nov","The final three days: deadline and last chance, ends midnight Tue 1 Dec.",{"Video":2,"Image":2,"GIF":1,"UGC":1})]
cformats=["Video","Image","GIF","UGC"]
ctot=sum(sum(v.values()) for _,_,_,v in cphases)
def ccell(n):
    if not n: return f'<div style="flex:1; display:flex; align-items:center; justify-content:center; border:2px dashed #c9c6c7; color:{GREY}; font-size:22px">none</div>'
    bg = K if n>=5 else (Y if n>=3 else Y40)
    fg = Y if n>=5 else K
    return f'<div style="flex:1; display:flex; align-items:center; justify-content:center; background:{bg}; color:{fg}; border:2px solid {K}"><p style="font-family:{DISP}; font-size:44px; line-height:1">{n}</p></div>'
def crow(label, cells, total, flex="1"):
    return (f'<div style="display:flex; gap:12px; flex:{flex}; min-height:0"><div style="flex:0 0 150px; display:flex; align-items:center"><p style="font-family:{HEAD}; font-size:26px; font-weight:700; text-transform:uppercase; line-height:1.05">{label}</p></div>'
            +"".join(cells)+f'<div style="flex:0 0 124px; display:flex; align-items:center; justify-content:flex-end">{total}</div></div>')
# timeline: chevrons aligned to the columns
TLC=[Y,K,Y40,"#e4e1e2"]
tline=crow("Timeline",[f'<div style="flex:1; display:flex; align-items:center; justify-content:space-between; gap:10px; background:{TLC[i]}; color:{W if i==1 else K}; padding:10px 14px; white-space:nowrap; clip-path:polygon(0 0, calc(100% - 18px) 0, 100% 50%, calc(100% - 18px) 100%, 0 100%{", 18px 50%" if i else ""})"><p style="font-family:{HEAD}; font-size:26px; font-weight:700; text-transform:uppercase; padding-left:{16 if i else 0}px">{ph}</p><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; padding-right:18px">{dt}</p></div>' for i,(ph,dt,why,v) in enumerate(cphases)],
           f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; color:{MUTE}">TOTAL</p>',flex="0 0 auto")
jobs=crow("The job",[f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; border-left:4px solid {K}; padding-left:12px"><div style="display:flex; align-items:baseline; gap:8px"><p style="font-family:{DISP}; font-size:48px; line-height:1">{sum(v.values())}</p><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; color:{MUTE}">ads</p></div><p style="font-size:22px; line-height:1.2; color:{K90}">{why}</p></div>' for ph,dt,why,v in cphases],
          f'<div style="display:flex; flex-direction:column; align-items:flex-end"><p style="font-family:{DISP}; font-size:48px; line-height:1">{ctot}</p><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; color:{MUTE}">ADS</p></div>',flex="0 0 auto")
def mix(t, e, tl="tested + new"):
    seg_t = (f'<div style="flex:{t}; background:{K}; color:{Y}; display:flex; align-items:center; padding-left:10px; white-space:nowrap"><p style="font-size:22px; font-weight:700">{t} {tl}</p></div>' if t else '')
    seg_e = f'<div style="flex:{e}; display:flex; align-items:center; padding-left:10px; white-space:nowrap; background-image:repeating-linear-gradient(45deg, {Y40} 0 10px, {W} 10px 20px)"><p style="font-size:22px; font-weight:700">{e}{" all" if not t else ""} new</p></div>'
    return f'<div style="flex:1; display:flex; border:2px solid {K}; height:56px">{seg_t}{seg_e}</div>'
cmix=[(6,4,"tested + new"),(12,8,"tested + new"),(0,13,""),(2,4,"tested")]
mixrow=crow("Tested vs new",[mix(t,e,tl) for t,e,tl in cmix],f'<p style="font-size:22px; font-weight:700; text-align:right; line-height:1.15">{sum(t for t,_,_ in cmix)} tested<br>{sum(e for _,e,_ in cmix)} new</p>',flex="0 0 auto")
rows="".join(crow(f,[ccell(v[f]) for _,_,_,v in cphases],f'<p style="font-family:{DISP}; font-size:36px">{sum(v[f] for _,_,_,v in cphases)}</p>') for f in cformats)
S["creative"]=content("creative",f"{ctot} performance ads across four phases",
 tline+jobs+mixrow+f'<div style="display:flex; flex-direction:column; gap:10px; flex:1; min-height:0">{rows}</div>'
 +f'<p style="font-size:22px; color:{K90}; line-height:1.25"><b>Hype and launch:</b> 60% tried and tested formats with a new theme, 40% new experiments. <b>Mid-sale:</b> all new content. <b>Ending soon:</b> 60% new, 40% proven.</p>',
 gap=14,src="Creative plan, 24 Sep 2026",notes="Hype 10 (4 video, 4 image, 2 GIF): built to work together, the video and GIFs grab attention and the statics carry the sale information with strong visuals, to a new, cold audience. Launch 20 (6 video, 6 image, 4 GIF, 4 UGC). Mid-sale 13 with a gifting focus (5 video, 5 image, 3 UGC). Ending soon 6, running the final three days from Sun 29 Nov (2 video, 2 image, 1 GIF, 1 UGC). Hype and launch run 60% tried and tested formats with a new theme and 40% new experiments: 6 and 4 in hype, 12 and 8 at launch. Mid-sale is all new content (13). Ending soon is 60% new and 40% proven ads: 4 new and 2 proven of 6, rounded. Every ad follows the cold-audience rule: hook, product proof, offer and date.")

def hcard2(fmt,name,n,where,copy,direction):
    top=f"border-top:10px solid {K};" if fmt=="Video" else ""
    return (f'<div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:8px; background:{W}; border:2px solid {K}; {top} padding:14px 16px">'
            f'<div style="display:flex; justify-content:space-between; align-items:center"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; background:{K}; color:{Y}; padding:2px 10px">{fmt}</p><p style="font-family:{DISP}; font-size:40px; line-height:1">{n}×</p></div>'
            f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase; line-height:1.05">{name}</h3>'
            f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; border-top:2px solid {K}; padding-top:6px; color:{MUTE}">{where}</p>'
            f'<p style="font-size:23px; font-weight:700; line-height:1.22">{copy}</p>'
            f'<p style="font-size:22px; line-height:1.25; color:{K90}">{direction}</p></div>')
def hgroup(label,sub,cards,dark):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; min-width:0">'
            f'<div style="display:flex; align-items:baseline; gap:12px; background:{K if dark else Y}; color:{Y if dark else K}; padding:6px 14px"><p style="font-family:{DISP}; font-size:26px; letter-spacing:1px; text-transform:uppercase">{label}</p><p style="font-size:22px; font-weight:700; color:{W if dark else K}">{sub}</p></div>'
            f'<div style="display:flex; gap:12px; flex:1; min-height:0">'+"".join(hcard2(*c) for c in cards)+'</div></div>')
bfcm_cards=[("Video","Air Walk / Crush","2","Hook, then sale graphics","&#39;If there&#39;s one thing I know about...&#39;","Jack hook, then hard-cut to the sale graphics: up to 25% off + free gifts + huge bundles, from Thu 19 Nov."),
            ("Image","Bundle images","2","1 paddock · 1 warehouse","Product in a paddock; product in the warehouse.","Bundle hero shots with the offer and the early-access line."),
            ("Image","AI statics","2","Generic","Up to 25% off + free gifts + huge bundles.","Generic AI-generated statics carrying the sale info.")]
theme_cards=[("Video","All Up Here","1","Warehouse","&#39;Yep mate, it&#39;s all up here.&#39;","Hype version of Bucket Head: the bucket, the clang, &#39;We&#39;re having a huge sale.&#39;"),
             ("Video","Show You A Thing Or Two","1","Paddock","&#39;I&#39;ll show you a thing or two.&#39;","Hype version: Jack&#39;s wrong wisdom, cut short, then the sale tease."),
             ("Video","Fake Phone Call","1","Car near the paddock","&#39;Boys. It&#39;s Jack.&#39;","Hype version: a call that &#39;wasn&#39;t meant to leak&#39; the sale.")]
def htally(fmt,got,planned):
    ok=got==planned
    return (f'<div style="flex:1; display:flex; align-items:center; justify-content:space-between; background:{K if ok else Y}; color:{Y if ok else K}; border:2px solid {K}; padding:8px 14px">'
            f'<p style="font-family:{HEAD}; font-size:26px; font-weight:700; text-transform:uppercase">{fmt}</p><p style="font-family:{DISP}; font-size:28px">{got} of {planned} {"✓" if ok else "!"}</p></div>')
S["hype-ads"]=content("hype-ads","Hype ads &gt;17 to 18 Nov",
 f'<div style="display:flex; gap:18px; flex:1; min-height:0">'
 +hgroup("BFCM style","6 ads · offer-led",bfcm_cards,False)
 +hgroup("Theme style","3 ads · Jack, 15 to 20 sec",theme_cards,True)+'</div>'
 +f'<div style="display:flex; gap:12px"><div style="flex:0 0 auto; display:flex; align-items:center; padding-right:6px"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">Plan check</p></div>'
 +htally("Video",5,4)+htally("Image",4,4)+htally("GIF",0,2)+htally("Total",9,10)+'</div>',
 gap=16,src="Creative plan, 28 Sep 2026",notes="Hype line-up. BFCM style (6): 2 Air Walk or Crush style videos, hook then sale graphics; 2 product bundle images, 1 in a paddock and 1 in the warehouse; 2 generic AI statics. Theme style (3): hype versions of three concepts, 15 to 20 sec: All Up Here (warehouse; the Bucket Head storyboard), Show You A Thing Or Two (paddock), Fake Phone Call (car near the paddock). That is 5 video, 4 image, no GIF: 9 ads against 10 on the creative volume slide (4 video, 4 image, 2 GIF). The sale opens Thu 19 Nov at midday; hype runs Tue 17 and Wed 18 Nov. Offer line: up to 25% off + free gifts + huge bundles.")


def dstrip(items):
    return (f'<div style="display:flex; gap:0; border:2px solid {K}">'
            +"".join(f'<div style="flex:{fx}; display:flex; flex-direction:column; gap:2px; padding:10px 16px; background:{bg}; color:{fg}; border-right:2px solid {K}"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; color:{Y if bg==K else MUTE}">{lab}</p><p style="font-size:24px; font-weight:700; line-height:1.2">{val}</p></div>' for lab,val,bg,fg,fx in items)+'</div>')
def beats(title, sub, bl, accent=K):
    return (f'<div style="flex:1.15; display:flex; flex-direction:column; gap:8px; background:{K}; color:{W}; padding:20px 22px; border-top:10px solid {Y}">'
            f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase; line-height:1.05">{title}</h3><p style="font-size:22px; color:{GREY}">{sub}</p>'
            +"".join(f'<div style="display:flex; gap:12px; align-items:baseline"><p style="font-family:{DISP}; font-size:26px; color:{Y}; flex:0 0 20px">{n}</p><p style="font-size:22px; line-height:1.25"><b>{a}:</b> {b}</p></div>' for n,(a,b) in enumerate(bl,1))+'</div>')
# overview
def sday(n,date,loc,story,feeds,prod,bg,accent):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; border:2px solid {K}; border-top:12px solid {accent}; padding:20px 22px">'
            f'<p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; color:{MUTE}">Day {n} · {date}</p>'
            f'<h3 style="font-family:{HEAD}; font-size:36px; font-weight:700; text-transform:uppercase; line-height:1">{loc}</h3>'
            f'<p style="font-size:23px; line-height:1.28"><b>Story:</b> {story}</p><p style="font-size:23px; line-height:1.28"><b>Feeds:</b> {feeds}</p>'
            f'<p style="margin-top:auto; font-size:22px; font-weight:700; background:{K}; color:{W}; padding:6px 10px">{prod}</p></div>')
S["shoot"]=content("shoot","The shoot: four days, two blocks",
 f'<div style="display:flex; gap:10px; align-items:center"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; background:{Y}; padding:4px 12px">BLOCK 1 · THU 1 AND FRI 2 OCT</p><div style="flex:1; height:3px; background:{K}"></div><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; background:{K}; color:{Y}; padding:4px 12px">BLOCK 2 · TUE 27 AND WED 28 OCT</p></div>'
 +f'<div style="display:flex; gap:16px; flex:1; min-height:0">'
 +sday(1,"Thu 1 Oct","Warehouse","Act 2, getting the call.","the launch ad, bundle builds and stills, grease and accessories proof.","Grease · accessories · bundles",Y40,Y)
 +sday(2,"Fri 2 Oct","Paddock","Act 3, sharing his wisdom.","the Pro Enclosure deep dive, the excavator at work, the big dog.","Pro Enclosure · Ultimate Earthmover",W,K)
 +sday(3,"Tue 27 Oct","Red dirt + warehouse pickups","Act 1 and the finale; the hype ads start here.","the hype hooks, the Frosty Cold Ones launch film, the last-day ad, pickups from day 1.","PRO Mat · small covers",Y40,Y)
 +sday(4,"Wed 28 Oct","Worksite, with Ivan","Act 4, the brand realisation and the gifting angle.","the gifting ads from 23 Nov, with Ivan from Earthworks Hub on site.","PRO Mat Plus · grease · gifts",W,K)+'</div>'
 +note("Each shoot day has its own page next. Block 2 lands three weeks before hype on 17 Nov, so the edit has to turn around fast. Location concepts to be added.",size=24),
 src="Shoot schedule, 28 Sep 2026",notes="Four shoot days in two blocks. Block 1: warehouse Thu 1 Oct, paddock Fri 2 Oct. Block 2: red dirt plus warehouse pickups Tue 27 Oct, worksite with Ivan Wed 28 Oct. Hype starts Tue 17 Nov, so the red dirt footage for the hype hooks has about three weeks from shoot to live.")

S["shoot-warehouse"]=content("shoot-warehouse","Shoot day 1: warehouse, Thursday 1 October",
 dstrip([("Date","Thu 1 Oct",Y,K,1),("Location","DiggerLid warehouse",W,K,1.3),("Story","Act 2 · Getting the call",W,K,1.4),("Product focus","Grease · accessories · bundles",K,W,1.6)])
 +f'<div style="display:flex; gap:18px; flex:1; min-height:0">'
 +beats("Hero episode 2 · 90 sec","Organic social · draft beats",[("Intro + physical comedy","Jack arrives from the big smoke and trips on the way in. Never reacts."),("Overstate + criticise","He sizes up the boys&#39; setup: &#39;Never needed one.&#39;"),("Right way","The boys walk him through the new range and the bundles."),("Double down","&#39;That&#39;s how I would have done it.&#39;"),("Sale details + CTA","His shopping pile starts; bundles and the offer.")])
 +card("Paid ads to capture",["&#39;Bucket Head&#39;: the 15s hype ad (see amendment)","Launch ad: &#39;So what have you boys been working on?&#39; Jack walks the warehouse","Forklift loading the ute, item by item, for each bundle","Bundle and gift-tier stills","Product bases for the hype statics","Grease and accessories proof shots"],accent=Y,tsize=28,lsize=23)
 +card("Props and product",["Forklift and ute","Hardcore Tradie: 2× PRO Mat Plus, hoodie, drawbar, 10× wipes, magnet mat, bottle opener","Ultimate Earthmover and Owner Operator full sets","Gift tiers: wipes, magnet mat, drawbar cover","PRO Mat Plus in all four colours"],accent=K,tsize=28,lsize=23)+'</div>',
 gap=18,src="Shoot schedule, creative plan, bundle slide",notes="Warehouse day. Beats follow the 90-second hero format on the theme slide and are a draft for the director. The bundle contents come from the bundle slide. Location concept to be added.")

S["shoot-paddock"]=content("shoot-paddock","Shoot day 2: paddock, Friday 2 October",
 dstrip([("Date","Fri 2 Oct",Y,K,1),("Location","The paddock",W,K,1.3),("Story","Act 3 · Sharing his &#39;wisdom&#39;",W,K,1.4),("Product focus","Pro Enclosure · Ultimate Earthmover",K,W,1.6)])
 +f'<div style="display:flex; gap:18px; flex:1; min-height:0">'
 +beats("Hero episode 3 · 90 sec","Organic social · draft beats",[("Intro + physical comedy","&#39;G&#39;day, I&#39;m Jack Clacker, and this is my backyard.&#39; Then he falls over."),("Overstate + criticise","&#39;Old trick&#39;: his way of covering the machine, which fails."),("Right way","The Pro Enclosure goes on; rain comes down; the machine stays dry."),("Double down","&#39;Been saying that for years.&#39;"),("Sale details + CTA","Ultimate Earthmover $732, $347 of gear free.")])
 +card("Paid ads to capture",["Launch week: &#39;Now this thing is the real deal.&#39; Pro Enclosure deep dive","The excavator at work, practical and authentic","The big dog","&#39;Talk slow for earthmovers&#39; line"],accent=Y,tsize=28,lsize=23)
 +card("Props and product",["Excavator and a Pro Excavator Enclosure","Water for the rain gag","Ultimate Earthmover set: PRO Mat Plus, drawbar, wipes, magnet mat, caddy, cradle, cap set, opener","The big dog and handler"],accent=K,tsize=28,lsize=23)+'</div>',
 gap=18,src="Shoot schedule, creative plan, bundle slide",notes="Paddock day. Beats follow the 90-second hero format and are a draft for the director. The rain gag needs water on site. Ivan appears on day 4 at the worksite, not here. Location concept to be added.")

S["shoot-reddirt"]=content("shoot-reddirt","Shoot day 3: red dirt and warehouse pickups, Tuesday 27 October",
 dstrip([("Date","Tue 27 Oct",Y,K,1),("Location","Red dirt · warehouse",W,K,1.3),("Story","Act 1 and the finale",W,K,1.4),("Product focus","PRO Mat · small covers",K,W,1.6)])
 +f'<div style="display:flex; gap:18px; flex:1; min-height:0">'
 +beats("Hero episode 1 · 90 sec","Organic social · draft beats",[("Intro + physical comedy","&#39;G&#39;day, I&#39;m Jack Clacker, and this is my backyard.&#39; Robots at the bar; he falls off his stool."),("Overstate + criticise","Kids and their AI: &#39;Not much call for country wisdom around here anymore.&#39;"),("Right way","The DiggerLid boys call for help with their Black Friday sale."),("Double down","&#39;I imagine they called me in for some real outback wisdom.&#39;"),("CTA","He loads the digger and hitches a truck to the big smoke. Coming soon.")])
 +card("Paid ads to capture",["&#39;Frosty Cold Ones&#39;: the 60s launch film (see amendment)","Hype hooks: &#39;Kids and their AI. What&#39;s the world coming to?&#39;","Airwalk intro: the hole in the ground and the founder","Finale at the pub: last drinks, &#39;Tell &#39;em I sent you&#39;, for the last-day ad","Warehouse pickups from day 1, list after the day 1 review"],accent=Y,tsize=28,lsize=23)
 +card("Props and product",["The long-haul truck and the digger on the back","Robot extras for the pub; the ute full of bargains for the finale","PRO Mat and small covers","Dust trail, campfire, night"],accent=K,tsize=28,lsize=23)+'</div>',
 gap=18,src="Shoot schedule, creative plan",notes="Day 3. Red dirt carries Act 1 and the finale, so it feeds the hype ads from 17 Nov and the last-day ad on 1 Dec. The pub scenes are listed here as part of the red dirt territory; confirm the pub is shot on this day. Warehouse pickups are whatever the day 1 review finds missing. Location concept to be added.")

S["shoot-worksite"]=content("shoot-worksite","Shoot day 4: worksite with Ivan, Wednesday 28 October",
 dstrip([("Date","Wed 28 Oct",Y,K,1),("Location","Home build site, backyard dig",W,K,1.4),("Story","Act 4 · The brand realisation",W,K,1.4),("Product focus","PRO Mat Plus · grease · gifts",K,W,1.5)])
 +f'<div style="display:flex; gap:18px; flex:1; min-height:0">'
 +beats("Hero episode 4 · 90 sec","Organic social · draft beats",[("Intro + physical comedy","A backyard dig on a home build; Jack slips into the trench. Never reacts."),("Overstate + criticise","He talks slowly to the young tradies: &#39;Old trick.&#39;"),("Right way","Real operators, Ivan among them, show him the PRO Mat and the grease."),("Double down","He claims he taught them a thing or two."),("Gifting CTA","&#39;Too good to keep to yourself.&#39; Shop Christmas gifts, ends 1 Dec.")])
 +card("Paid ads to capture",["Gifting ads from 23 Nov: 13 all new (5 video, 5 image, 3 UGC)","&#39;Too good to keep to yourself&#39;: for your mates, your husband, your habibi","Operator reactions to the gear","Collab bundle stills: Titan Sox × DiggerLid × 3D Pro"],accent=Y,tsize=28,lsize=23)
 +f'<div style="flex:1; display:flex; flex-direction:column; gap:14px">'
 +f'<div style="display:flex; flex-direction:column; gap:8px; background:{Y}; border:2px solid {K}; padding:18px 20px"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">Note: Ivan on site</p><p style="font-size:23px; line-height:1.3">Ivan from Earthworks Hub joins the worksite day. Confirm his call time, a signed release and what he says on camera; brief him on Jack before rolling.</p></div>'
 +card("Props and product",["PRO Mat Plus, all four colours; grease","The collab gift bundle","Small covers; an excavator for the dig"],accent=K,tsize=28,lsize=23)+'</div></div>',
 gap=18,src="Shoot schedule, creative plan, gifting slide",notes="Day 4. The worksite carries Act 4 and the mid-sale gifting angle from 23 Nov, so this day feeds the gifting ads and UGC. Ivan from Earthworks Hub is on site. Location concept to be added.")

FROSTY_IMG="/_blob/f52b735f658c32c7ad7d13c3e321dbba"
frosty=[("01","Touchdown","0 to 7s","JACK: &#39;Time to check into the local for a few frosty cold ones.&#39;","Steps into a puddle; doesn&#39;t notice."),
        ("02","The locals","7 to 15s","JACK (VO): &#39;But looks like AI&#39;s already taken everyone&#39;s jobs.&#39;","At the bar, glancing round at the robot regulars."),
        ("03","The yarn","15 to 23s","ROBOT: &#39;Thiiis big.&#39;","A robot spins a yarn, arms wide; Jack sours."),
        ("04","The call","23 to 30s","JACK, on the flip phone: &#39;Boys. It&#39;s Jack.&#39;","Through the ute windscreen, calling the DiggerLid boys."),
        ("05","Keep it quiet","30 to 38s","BOYS: &#39;Keep it a secret. We&#39;re not talking about it yet.&#39;","Reverse shot; finger to lips at the speakerphone."),
        ("06","Pretty good","38 to 55s","VO: the sale summary. JACK: &#39;Gee, that&#39;s pretty good.&#39;","Covers, KAJO, PRO Mats; offer and end date on screen."),
        ("07","Card","55 to 60s","DiggerLid&#39;s Aussie Black Friday Adventure · [URL]","SUNG: &#39;...time to float her out.&#39;")]
S["concept-frosty"]=content("concept-frosty","Concept: &#39;Frosty Cold Ones&#39;",
 dstrip([("Shoot","Day 3 · red dirt + pub · Tue 27 Oct",Y,K,1.5),("Format","60 sec · 9:16",W,K,0.9),("Version","Launch version",W,K,0.9),("Storyboard","V2 · working title Red Dirt Robots",K,W,1.6)])
 +f'<img src="{FROSTY_IMG}" alt="Storyboard, seven frames: Jack steps out of his ute into a puddle outside a country pub; drinks at a bar staffed by robots in hi-vis; a robot tells a big yarn; Jack calls the DiggerLid boys from his ute; the boys shush on speakerphone; the sale summary over Jack in the ute; the DiggerLid Aussie Black Friday Adventure end card" style="width:1664px; height:352px; object-fit:cover; background:#f3efe6; border:2px solid {K}; flex-shrink:0">'
 +f'<div style="display:flex; gap:12px; flex:1; min-height:0">'
 +"".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; border-top:4px solid {K}; padding-top:6px"><p style="font-family:{HEAD}; font-size:24px; font-weight:700; text-transform:uppercase; line-height:1.05">{t}</p><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; color:{MUTE}">{tm}</p><p style="font-size:22px; font-weight:700; line-height:1.18">{d}</p><p style="font-size:22px; line-height:1.18; color:{K90}">{sh}</p></div>' for n,t,tm,d,sh in frosty)+'</div>',
 gap=14,src="Storyboard V2, 60s, 9:16",notes="Frame 1 full line: Been out bush a few weeks. Time to check into the local for a few frosty cold ones. Frame 5 full line: Yep... but keep it a secret. We are not talking about it yet. Concept name: Frosty Cold Ones (storyboard working title: Red Dirt Robots, launch). Frame 1 Touchdown: WS, low; Jack steps out of the ute straight into the puddle and does not notice; empty verandah. Frame 2 The locals: MS at the bar, beer halfway up. Frame 3 The yarn: a robot spins a big yarn to its mates, arms wide in time with the VO; Jack sours in the background. Frame 4 The call: MCU through the windscreen. Frame 5 Keep it quiet: the boys lean in to the speakerphone. Frame 6 Pretty good: dirty frame from beside the ute, past the muddy door and mirror, audio on; on-screen overlay Black Friday sale, up to [X]% off, ends [date]. To fill: up to 25% off, ends Tue 1 Dec. Frame 7 Card: DiggerLid's Aussie Black Friday Adventure, [URL]; sung line: time to float her out. Scheduled for day 3, red dirt and the pub, Tue 27 Oct.")

BUCKET_IMG="/_blob/b97d57b55fa0b6edb0b073c40eba6cc5"
bucket=[("Walk and talk","0 to 4s","JOEL: &#39;Now Jack, you remember everything in our huge Black Friday sale?&#39;","Side-on tracking; the audience sees the bucket first."),
        ("The claim","4 to 6s","JACK: &#39;Yep mate, it&#39;s all up here.&#39; (taps head)","Same shot, no cut. He points at the exact spot that&#39;s about to fail."),
        ("The hit","6 to 7s","SFX: CLANG. He drops out of frame.","Keep tracking a half-beat; suddenly just the brothers and the bucket."),
        ("The look","7 to 10s","The brothers stop, look down, then at each other. SFX: snoring.","Static wide from behind Jack&#39;s boots. Hold the silence."),
        ("The line","10 to 13s","JOEL (flat): &#39;We&#39;re having a huge sale.&#39; SUPER: HUGE BLACK FRIDAY SALE","Medium on the brothers, Jack&#39;s boots in front."),
        ("Card","13 to 15s","Fade to black. Campaign card + early-access sign-up.","Audio over black: a snore, then &#39;...all up here...&#39;")]
S["concept-bucket"]=content("concept-bucket","Concept: &#39;Bucket Head&#39;",
 dstrip([("Shoot","Day 1 · warehouse · Thu 1 Oct",Y,K,1.4),("Format","15 sec · 9:16",W,K,0.9),("Version","Hype version · early access",W,K,1.1),("Storyboard","V1 · working title All Up Here",K,W,1.5)])
 +f'<img src="{BUCKET_IMG}" alt="Storyboard, six frames: Joel, his brother and Jack walk past an excavator outside the warehouse; Jack taps his head; the yellow bucket clangs him out of frame; the brothers look down at Jack flat on his back; the brothers deliver the sale line; the Huge Black Friday Sale early-access card" style="width:1664px; height:350px; object-fit:cover; object-position:center 40%; background:#f3efe6; border:2px solid {K}; flex-shrink:0">'
 +f'<div style="display:flex; gap:14px; flex:1; min-height:0">'
 +"".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; border-top:4px solid {K}; padding-top:6px"><p style="font-family:{HEAD}; font-size:24px; font-weight:700; text-transform:uppercase; line-height:1.05">{t}</p><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; color:{MUTE}">{tm}</p><p style="font-size:22px; font-weight:700; line-height:1.18">{d}</p><p style="font-size:22px; line-height:1.18; color:{K90}">{sh}</p></div>' for t,tm,d,sh in bucket)+'</div>',
 gap=14,src="Storyboard V1, 15s, 9:16",notes="Frame 1 shot: side-on tracking; the bucket enters frame ahead of them, so the audience sees it first. Frame 5: medium on the brothers with Jack&#39;s boots in the foreground. Concept name: Bucket Head (storyboard working title: Jack, All Up Here). A 15-second hype ad shot on the warehouse day: Jack claims he remembers the whole sale, the excavator bucket knocks him out, and the brothers deliver the line flat. Ends on the early-access card: Huge Black Friday Sale, Get early access, sign up to shop the sale first. Needs a stunt plan for the bucket hit and the fall.")

def pcard(fmt,n,hint=""):
    top=f"border-top:10px solid {K};" if fmt in ("Video","UGC") else ""
    ph=lambda h,t: f'<div style="border:2px dashed #b5b1b2; padding:{8 if t else 6}px 10px; min-height:{h}px"><p style="font-size:22px; color:{GREY}; line-height:1.2">{t}</p></div>'
    return (f'<div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:10px; background:{W}; border:2px solid {K}; {top} padding:16px 18px">'
            f'<div style="display:flex; justify-content:space-between; align-items:center"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; background:{K}; color:{Y}; padding:2px 10px">{fmt}</p><p style="font-family:{DISP}; font-size:44px; line-height:1">{n}×</p></div>'
            f'<h3 style="font-family:{HEAD}; font-size:30px; font-weight:700; text-transform:uppercase; line-height:1.05; color:{GREY}">Concept TBC</h3>'
            f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; border-top:2px solid {K}; padding-top:8px; color:{GREY}">Role: TBC</p>'
            +ph(64,"Hook / copy")+ph(0,hint if hint else "Creative direction")+'</div>')
def pcheck(items):
    return (f'<div style="display:flex; gap:12px"><div style="flex:0 0 auto; display:flex; align-items:center; padding-right:6px"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">Plan</p></div>'
            +"".join(f'<div style="flex:1; display:flex; align-items:center; justify-content:space-between; background:{K if f!="Total" else W}; color:{Y if f!="Total" else K}; border:2px solid {K}; padding:10px 16px"><p style="font-family:{HEAD}; font-size:26px; font-weight:700; text-transform:uppercase">{f}</p><p style="font-family:{DISP}; font-size:30px">{v}</p></div>' for f,v in items)+'</div>')
def lcard(fmt,name,n,where,direction):
    top=f"border-top:8px solid {K};" if fmt in ("Video","UGC") else ""
    return (f'<div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:6px; background:{W}; border:2px solid {K}; {top} padding:10px 14px">'
            f'<div style="display:flex; justify-content:space-between; align-items:center"><p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; background:{K}; color:{Y}; padding:1px 10px">{fmt}</p><p style="font-family:{DISP}; font-size:34px; line-height:1">{n}×</p></div>'
            f'<h3 style="font-family:{HEAD}; font-size:25px; font-weight:700; text-transform:uppercase; line-height:1.05">{name}</h3>'
            f'<p style="font-family:{DISP}; font-size:22px; letter-spacing:1px; text-transform:uppercase; color:{MUTE}">{where}</p>'
            f'<p style="font-size:22px; line-height:1.22; color:{K90}">{direction}</p></div>')
def lrow(label,sub,cards,dark):
    return (f'<div style="display:flex; gap:12px; flex:1; min-height:0">'
            f'<div style="flex:0 0 140px; display:flex; flex-direction:column; justify-content:center; gap:6px; background:{K if dark else Y}; color:{Y if dark else K}; padding:12px 14px"><p style="font-family:{DISP}; font-size:28px; letter-spacing:1px; text-transform:uppercase; line-height:1.05">{label}</p><p style="font-size:22px; font-weight:700; color:{W if dark else K}; line-height:1.2">{sub}</p></div>'
            +"".join(lcard(*c) for c in cards)+'</div>')
launch_bfcm=[("Video","Infomercial #1","1","Warehouse","As per last year: whip cuts, quick script."),
             ("Video","Infomercial #2","1","Warehouse","Hook, then behind the demo table with B-roll."),
             ("Video","Usage: bundle + gift","1","Paddock","Bundle and free gift, PRO Mat and Pro Enclosure in use."),
             ("Image","Bundle images","2","Warehouse","The bundles with the offer."),
             ("Image","AI gen images","2","Generic","AI statics with the sale info."),
             ("GIF","BFCM GIFs","2","Offer-led","Offer and countdown."),
             ("UGC","UGC creatives","4","Creators","Customer and creator content.")]
launch_theme=[("Video","All Up Here infomercial","1","Warehouse","The All Up Here hook, then Jack out cold across the products."),
              ("Video","Look Earthmovers","1","Paddock","Infomercial #2: walk and talk, with the gear in use."),
              ("Image","Products + Jack out cold","1","Warehouse","Every product and bundle, Jack out cold among them."),
              ("GIF","Theme GIFs","2","Jack","Jack moments on loop."),
              ("Video","Fake Phone Call","1","Car near the paddock","Launch version with B-roll and offer overlays.")]
S["launch-ads"]=content("launch-ads","Launch ads &gt;from 19 Nov",
 lrow("BFCM style","13 ads · offer-led",launch_bfcm,False)
 +lrow("Theme style","6 ads · Jack",launch_theme,True)
 +f'<div style="display:flex; gap:12px"><div style="flex:0 0 auto; display:flex; align-items:center; padding-right:6px"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">Plan check</p></div>'
 +htally("Video",6,6)+htally("Image",5,6)+htally("GIF",4,4)+htally("UGC",4,4)+htally("Total",19,20)+'</div>',
 gap=14,src="Creative plan, 29 Sep 2026",notes="Launch line-up from Thu 19 Nov. BFCM style (13): infomercial #1 as per last year (warehouse, whip cuts, quick script); infomercial #2 (hook, then behind the demo table with B-roll, warehouse); a usage video with a bundle, the free gift, PRO Mat and Pro Enclosure (paddock); 2 bundle images (warehouse); 2 AI-generated images; 2 GIFs; 4 UGC creatives. Theme style (6): an infomercial from the All Up Here hook with Jack unconscious across different products (warehouse); a Look Earthmovers infomercial, walk and talk with usage (paddock); a photo of all products and bundles together with Jack unconscious; a Fake Phone Call launch version with B-roll and overlays; 2 GIFs. That is 6 video, 5 image, 4 GIF, 4 UGC: 19 against 20 on the creative volume slide (6 video, 6 image, 4 GIF, 4 UGC). Frosty Cold Ones and The Real Deal are not in this line-up yet. Offer line: up to 25% off + free gifts + huge bundles, ends 1 Dec.")
S["midsale-eos-ads"]=content("midsale-eos-ads","Mid-sale + ending soon ads &gt;23 Nov to 1 Dec",
 f'<div style="display:flex; gap:14px; align-items:center"><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; background:{Y}; padding:2px 12px">Mid-sale gifting · 23 to 28 Nov · 13 all new</p><div style="flex:1; height:3px; background:{K}"></div><p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase; background:{K}; color:{Y}; padding:2px 12px">Ending soon · 29 Nov to 1 Dec · 6</p></div>'
 +f'<div style="display:flex; gap:12px; flex:1; min-height:0">'
 +pcard("Video",5,"Too Good To Keep")+pcard("Image",5,"Gifting page, collab bundle")+pcard("UGC",3)
 +f'<div style="flex:0 0 4px; background:{K}"></div>'
 +pcard("Video",2,"Last Drinks")+pcard("Image",2)+pcard("GIF",1)+pcard("UGC",1)+'</div>'
 +pcheck([("Mid-sale",13),("Ending soon",6),("Total",19)]),
 gap=16,src="Creative plan, 24 Sep 2026",notes="Placeholder: concepts to be added. Mid-sale gifting from Mon 23 Nov: 13 all-new ads (5 video, 5 image, 3 UGC) to cold audiences in the gifting segment, driving to the Christmas gifting page and the Titan Sox × DiggerLid × 3D Pro collab bundle; Black Friday Fri 27 Nov sits here. Ending soon from Sun 29 Nov: 6 ads (2 video, 2 image, 1 GIF, 1 UGC), countdown to Last Drinks; Cyber Monday Mon 30 Nov sits here. Sale ends midnight Tue 1 Dec.")

S["deliverables"]=content("deliverables","Other deliverables (due dates TBC)",
 table(["Asset","Use","Count","Timing","Owner"],[
  ["Performance ads","Paid social, by phase","49: the list is slide 14","Hype from 17 Nov","Creative [name]"],
  ["Hero episodes, organic","One episode per location","4","Shot 1, 2, 27 and 28 Oct","Creative [name]"],
  ["Bundle and gift-tier stills","Bundle page, ads, emails","12","Shot Thu 1 Oct (warehouse)","Creative [name]"],
  ["Email and SMS templates","Launch, mid-sale, Black Friday, close","6","TBC","Email [name]"],
  ["Sale, bundle, collection, capture pages","Site","4 pages","Live and QA&#39;d by 13 Nov","Web [name]"],
  ["Christmas gifting landing page, gift guide, cut-off banner","Site, from 23 Nov","3","TBC","Web [name]"],
  ["Collab bundle: Titan Sox × DiggerLid × 3D Pro","Gifting page, gifting ads","1 bundle","Contents and price TBC","Growth [name]"]],[30,24,16,18,12],size=23),
 src="Creative plan, shoot schedule",notes="Slide 14 is the primary deliverables list for performance ads (49 across hype, launch, mid-sale and ending soon). This slide holds everything else. The EE tool (80% volume) sized creative at 48 to 60 assets, so 49 sits inside that range. Hard constraint: pages live and tracked by 13 November.")

# ------------------------------------------------------------------ 04 LOCK-UP
S["s-lockup"]=section("s-lockup","04","Lock-up","Timeline with hours, day-by-day sends, pages to build, stock and fulfilment, owners, risks and the decisions needed.")

tl=[("Mon 16 and Tue 17 Nov","Hype","Two hype sends to engaged segments; hype ads to a new, cold audience. All hype traffic to the first-access capture page. Pages live and tracked by close of day 17."),
    ("Wed 18 Nov, 12:00 PM AEDT","Launch (day 1)","Sale live at midday (2025 launched at 3:05 PM). Launch email and SMS at midday. 19% of sale revenue expected on day one, 31% by the end of day two."),
    ("Thu 19 to Sun 22 Nov","Days 2 to 5","Knock-off drop at 3:30 PM daily. Daily 8 AM scorecard and cut rules."),
    ("Mon 23 Nov","Mid-sale push (day 6)","New content drop and a PRO Mat gifting angle. Christmas gifting launches: gift collection, gift-buyer ads, gift guide email and SMS. About a third of the creative lands here."),
    ("Tue 24 to Thu 26 Nov","Days 7 to 9","Gift-led drops and social proof; ads rotate to gifting angles."),
    ("Fri 27 Nov","Black Friday (day 10)","Full-database send. Mystery Box as the drop. Extra creative."),
    ("Sat 28 to Mon 30 Nov","Days 11 to 13","Cyber Monday Mon 30 Nov: full-database send, last knock-off weekend, gifting continues."),
    ("Tue 1 Dec, closes 11:59 PM AEDT","Day 14","Last chance 7 AM and sale-ends-midnight 5 PM. No extension. Thank-you, gift guide and shipping cut-offs follow on 2 and 9 Dec.")]
S["timeline"]=content("timeline","Timeline: 2 hype days plus 14 sale days, 18 Nov to 1 Dec, all times AEDT",
 f'<div style="display:flex; flex-direction:column; gap:8px">'+"".join(f'<div style="display:flex; gap:20px; align-items:start; border-bottom:2px solid {K}; padding:0 0 8px 0"><p style="font-family:{HEAD}; font-size:25px; font-weight:700; width:330px; line-height:1.15">{d}</p><p style="font-family:{DISP}; font-size:24px; width:210px; letter-spacing:1px; text-transform:uppercase; line-height:1.2">{t}</p><p style="flex:1; font-size:23px; line-height:1.3; color:{K90}">{x}</p></div>' for d,t,x in tl)+'</div>'
 +note("Dates match the EE tool export, its email flow and the Meta plan. The shared calendar (23 Nov start) still needs updating. Hours from 2025: orders ran 85 to 100 an hour from 7 to 11 AM and 115 to 120 an hour from 6 to 9 PM.",size=22),
 src="Planning decision, EE tool, campaign calendar",notes="Black Friday lands on day 10 and Cyber Monday on day 13; the last-chance push is Tuesday 1 December, the day after Cyber Monday.")

comms=[("H1 Mon 16 Nov","Email","Engaged 250 days + window shoppers 14 days","Sale is coming: our biggest sale of the season starts soon"),
       ("H2 Tue 17 Nov","Email","Engaged 90 days + window shoppers","Hype 2, plain text: biggest sale of the year, first access tomorrow at midday"),
       ("D1 Wed 18 Nov 7:00 AM","Email + SMS","Full database; SMS list","Sale live: the whole offer, bundles, gift tiers"),
       ("D2 Thu 19 Nov","Email","Engaged 90 days","Top sale picks; first knock-off drop 3:30 PM"),
       ("D3 Fri 20 Nov","Email","Engaged 250 days","Founder favourites, plain text"),
       ("D6 Mon 23 Nov","Email + SMS","Engaged 250 days + window shoppers","Mid-sale push: new content drop, PRO Mat gifts; Christmas gifting launch"),
       ("D7 Tue 24 Nov","Email","Engaged 250 days","Product spotlight: gift sets"),
       ("D9 Thu 26 Nov","Email","Engaged 90 days","Social proof"),
       ("D10 Fri 27 Nov","Email + SMS","Full database","Black Friday: Mystery Box"),
       ("D12 Sun 29 Nov","Email","Engaged 250 days","Sale updates: what is left"),
       ("D13 Mon 30 Nov","Email + SMS","Full database","Cyber Monday: last knock-off weekend, gifts arrive before Christmas"),
       ("D14 Tue 1 Dec 7 AM / 5 PM","Email + SMS","Full database; engaged 250 days at 5 PM","Last chance; sale ends midnight")]
S["comms"]=content("comms","Sends, day by day (from the email flow, 16 Nov to 1 Dec)",
 table(["When","Channel","Audience","Message"],comms,[22,13,30,35],size=22)+note("Daily 3:30 PM drop by SMS and to the engaged segment. Cyber Monday send added (not in the tool flow): it was the best returning-customer day of 2025. Email drove $82k, 15% of the 2025 sale.",size=22),
 src="email-flow.csv, Klaviyo 2025 send log",notes="Four full-database sends: launch, Black Friday, Cyber Monday, last chance. Everything else is segmented.")

S["pages"]=content("pages","Pages and site work to build",
 table(["Item","What it does","Benchmark","Due","Owner"],[
  ["Sale landing page","Warm traffic home; grease and PRO Mat first, bundles, big tickets below","3.4% conversion, 10% add to cart, 5 pages per session","13 Nov","Web [name]"],
  ["Bundle page","Three hero bundles and existing bundles","","13 Nov","Web [name]"],
  ["Collection page","Everything on sale, sortable","","13 Nov","Web [name]"],
  ["Homepage takeover","Sale banner, drop of the day, gift entry","Homepage converted 8 to 10% in past sales","17 Nov","Web [name]"],
  ["First-access capture page","Where hype traffic lands: countdown, email and SMS capture","4,300 hype sessions last cycle","13 Nov","Web and Email [names]"],
  ["Sale popup","Early access or bonus gift; replaces the discount popup during the sale","Reach 50%+, submit 5%","13 Nov","Growth [name]"],
  ["Drop module","3:30 PM badge, countdown, today&#39;s deal","","13 Nov","Web [name]"],
  ["Tracking QA","Cart add, checkout, order events on every page","Cart adds must exceed orders","13 Nov","Web [name]"],
  ["Gift entry and cut-off banner","Gift path, delivery dates","","27 Nov","Web [name]"]],[22,36,22,10,10],size=23),
 src="Landing page review",notes="Nine items, one deadline. The capture page and the sale popup are the two pieces that did not exist last year.")

S["ops"]=content("ops","Stock, fulfilment and service (to confirm)",
 f'<div style="display:flex; gap:24px">{big("700","orders on day one at the $983k plan (19% of 3,691 sale orders), against 251 on launch day 2025: plan fulfilment, packaging and service for nearly three times last year&#39;s peak.",bg="#ffffff")}{big("$900k","stock at RRP against $983k: 128% sell-through after the 15% discount (109% by RRP in the tool), about $255k short. Gift units at the 2025 spread: about 1,070 wipes, 550 magnet mats and 210 drawbars.")}{big("[ ]","bundle kits pre-packed before launch: components for three hero bundles at the volumes the drops will drive.",bg="#ffffff")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("Stock and warehouse",["Gift stock reserved by 10 Nov: about 1,100 Digger Wipes, 550 magnet mats and 210 drawbar covers at the plan, more at stretch","Stock-out plan: which SKUs come off the sale first, and the substitute gift when magnet mats run out","Bundle components kitted; a stop rule when any component runs out","Drop-of-the-day stock confirmed the day before each drop","Warehouse shoot day (6 Nov) doubles as the stock check"],accent=Y)
 +card("Customer service",["Offer rules sheet to the service team by 13 Nov (mechanic, stacking, exclusions, price protection, returns)","Extended hours on launch day, Black Friday and Cyber Monday","Saved replies for the ten most likely questions","Delivery-date promise and shipping cut-offs on every gift surface"],accent=K80)+'</div>',
 src="Shopify order volumes",notes="Placeholders are deliberate: the ops numbers come from the offer decisions, and the team owns them.")

S["owners"]=content("owners","Owners and dates",
 table(["Role","Owner","Owns","Key date"],[
  ["Head of Growth","Matt","Target, budget, cut rules, daily scorecard, decisions","This week: six decisions"],
  ["Paid media","[name]","Audience and destination split, budget shape, test markets, kill rule","16 Nov: sets scheduled"],
  ["Email and SMS","[name]","Segments, twelve sends, drop SMS, capture page flow","12 Nov: templates; 16 Nov: scheduled"],
  ["Web","[name]","Sale, bundle, collection, capture pages; popup; drop module; tracking","13 Nov: live and QA&#39;d"],
  ["Creative","[name]","Shoot, hero film, cut-downs, teasers, stills, drop template","6 Nov shoot; 10 Nov edit lock; 12 Nov assets"],
  ["Finance","[name]","Bundle and DiggerShield margin, gift-tier cost, price integrity","30 Oct"],
  ["Operations and warehouse","[name]","GWP stock, bundle kitting, peak-day fulfilment, drop stock","10 Nov"],
  ["Customer service","[name]","Rules sheet, saved replies, extended hours","13 Nov"]],[22,14,44,20],size=24),
 src="",notes="Names to be filled in the room. Every owner has one date they are accountable for.")

S["lockup"]=content("lockup","Checklist and risks",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Pre-game checklist",["Popup reach above 50% on paid pages, weekly check · Growth · 15 Oct","Bundle, DiggerShield and gift-tier margins signed off · Finance · 30 Oct","Warehouse shoot; stock check · Creative, Ops · 6 Nov","Edit locked · Creative · 10 Nov","Pages live, tracking QA, sale popup, capture page · Web · 13 Nov","Rules sheet to customer service · Growth · 13 Nov","Ad sets and sends scheduled; cold to product pages · Paid, Email · 16 Nov","Hangover plan and new product launch briefed · Growth · 20 Nov"],accent=Y,lsize=24)
 +card("Risks from the notes, with the answer",["Gifting path: gift entry, tiers and finder on the sale page; Christmas collection from the mid-sale push, 23 Nov","Landing page late: 13 Nov deadline, built before hype, source-split traffic, 3.4% benchmark","Hangover: gift guide, new product, cut-off messaging; no December list buying","Overspending: 28% ceiling, 25% target, written cut rules, daily 8 AM check","Popup submit collapses in a sale (2.3% in June): sale-specific popup with early access or a bonus gift","Edit slips: Take Cover film as the fallback launch"],accent=K80,lsize=24)+'</div>',
 src="Planning notes p.9, 2025 sale review",notes="The four possible issues from the notes each have a mitigation; two more risks were added from the data.")

S["measure"]=content("measure","Measuring the sale: the 8 AM scorecard and the cut rules",
 table(["Row","Target or benchmark","Rule if missed","Source"],[
  ["Revenue against the daily shape","EE plan: day 1 28%, day 2 12%, day 3 10%, plateau 3 to 7%, Black Friday 5%, last day 7%; 2025 measured: 31% in 48h, 5% per day","Under 80% of plan for two days: review spend and creative","Shopify"],
  ["Meta spend to revenue","25% (EE plan 25% sale MER, 24.7% effective; 2025 actual 24%); ceiling 28%","Over 30% for two days: cut broad prospecting","Meta, Shopify"],
  ["Sale page conversion by source","3.4% blended; social over 2%; direct over 6%","Social under 1.5% by midday: pull the broad set","Shopify"],
  ["Popup reach and submits","Reach over 50%; submit about 5% of views","Reach under 40%: check triggers the same day","Alia, Shopify"],
  ["Returning-customer share","Over 25% on segmented-send days","Under 20%: check the segment and the send","Shopify"],
  ["Average order and bundle share","AOV over $315; bundles [ ]% of orders","AOV under $290: push bundles and gift tiers in the drops","Shopify"],
  ["Drop response","Orders 3:30 to 5:30 PM above the same window the day before","Flat two days running: change the drop type","Shopify"]],[26,30,30,14],size=23),
 src="",notes="One person reads this at 8 AM and makes the calls. The rules are written now so nobody argues them on the day.")

S["decisions"]=content("decisions","Decisions needed this week",
 f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; flex:1">'+"".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{"#ffffff" if i%2 else Y40}; padding:22px 24px; border:2px solid {K}"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate([
  ("Target","Plan $983k incl. GST (EE tool latest run, $90k base week) or stretch $1.27M on the current run rate; spend $243k (25%), ceiling 28%."),
  ("EE tool corrections","Still open: product cost 32%, gift uptake 43% / 15%, stock cover. Dates are settled at 18 Nov to 1 Dec; the shared calendar needs re-dating."),
  ("Offer","25% ex-grease, DiggerShield $150 / $200, gift tiers $399 / $599 / $799, bundles at 30 / 40 / 50% (Hardcore Tradie $777, Ultimate Earthmover $884, Ludicrous $1,058), shown as hero gear discounted and the rest free, stacking and exclusions."),
  ("Theme and fallback","All Aussie Adventure; Take Cover as the fallback film."),
  ("Test markets and price test","Budgets and kill rules for USA, NZ, TikTok, YouTube; DiggerShield price test yes or no."),
  ("Owners","Names against the eight roles, and who owns the popup reach fix due 15 Oct.")]))+'</div>',
 notes="Six decisions unblock the build. Everything else in the deck is execution against dates.")

# ------------------------------------------------------------------ APPENDIX
S["s-appendix"]=section("s-appendix","05","Appendix","The questions people ask after a plan like this, answered; and what the terms mean.")

S["faq-exec"]=content("faq-exec","Questions the exec will ask",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:1">'+qa([
  ("When does it run, and what are we targeting?","Wednesday 18 November 12:00 PM (midday) to Tuesday 1 December 11:59 PM AEDT, hype sends on 16 and 17 November. Plan $983k sale revenue incl. GST, the EE tool projection on a $90k week, at $243k of spend (25%). Floor $585k if we only repeat 2025; stretch $1.27M on the current run rate. Profit at the plan is $148k in the tool and about $110k after the product-cost and gift-uptake corrections."),
  ("Why 25% and not 30%?","Every point of discount lifts variable cost; 2025 delivered $535k at a sitewide discount with spend at 25.5%. Bundles and gift tiers do the work a deeper discount would, without cutting margin on everything."),
  ("Why exclude grease, and what does it cost?","Grease is the one product that repeats and the base for December reorders. But it was 33% of the 2025 sale and grease packs carried a 14% discount, so exclusion is a decision: either accept a smaller grease share or feature grease packs as a hero offer instead of a sitewide cut."),
  ("What stops us overspending?","A 28% ceiling on a 24% plan, spend shaped to the revenue curve rather than smoothed (with the 2025-shaped curve the tool no longer shows loss days, but plateau days clear only $3.5k), written cut rules, and one person reading the scorecard at 8 AM. Cold traffic no longer goes to the sale page.")],qsize=26,asize=23)+'</div><div style="flex:1">'+qa([
  ("Why All Aussie Adventure? Is the IP risk real?","It fits the audience and gives us a content series beyond the sale. The risk is managed by using our own character and format parody only, with a legal read before paid placement. Take Cover is the fallback."),
  ("Why spend in the USA and NZ at all?","International was 27% of 2025 sale revenue at a $570 average order, more than double Australia. The tests are capped with a day-4 kill rule; the aim is efficient international revenue, not less of it."),
  ("What if the film is not ready?","Edit lock is 10 Nov, three days before pages go live. If it slips, the Take Cover film (shot in July) launches and the Adventure episodes run mid-sale."),
  ("What happens after Cyber Monday?","Christmas gifting has run since the mid-sale push on 23 Nov and continues after the sale: gift guide, a new product launch, shipping cut-offs on 2 and 9 Dec. No further discounting and no December list buying.")],qsize=26,asize=23)+'</div></div>',
 notes="Answers use the numbers on the research and strategy slides; nothing here is new.")

S["faq-team"]=content("faq-team","Questions the team will ask",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:1">'+qa([
  ("What time does the sale start and end?","Thursday 19 November, 6:00 AM AEDT, to Wednesday 2 December, 11:59 PM AEDT: 14 days. Hype sends Tuesday 17 and Wednesday 18 November. Black Friday is day 9, Cyber Monday day 12."),
  ("Is it a code or automatic?","Proposal: automatic sitewide discount, bundles as fixed-price products, gift tiers added automatically at $299, $399 and $599. To be confirmed on the offer rules slide."),
  ("Do gifts stack with bundles?","Proposal: gift tiers apply to the discounted subtotal, bundles do not stack with the sitewide percentage, no code stacking. Confirm before 13 Nov."),
  ("What are the 3:30 PM drops?","One extra deal a day for 24 hours, announced by SMS and by email to the engaged segment. Draft calendar on the drops slide; the team sets the order.")],qsize=26,asize=23)+'</div><div style="flex:1">'+qa([
  ("Who gets which email?","Full database on launch, Black Friday, Cyber Monday and the last day. Everything else goes to engaged 90 or 250 day segments with window shoppers layered in, or the SMS list. Fourteen sends on the comms slide, plus the daily 3:30 PM drop."),
  ("Where do the ads send people?","Cold prospecting to grease and PRO Mat product pages. Retargeting, email-list audiences and anyone who has visited to the sale page."),
  ("What do I tell a customer who bought last week?","Price protection policy is a decision on the offer rules slide; the answer goes into the service rules sheet by 13 Nov."),
  ("Which products go in the ads and the drops?","Pro Enclosure and grease were 54% of last year&#39;s sale; PRO Mat and DiggerShield the next 19%. PRO Mat Plus and grease lead acquisition, the big tickets sit below, and the three hero bundles headline Black Friday weekend.")],qsize=26,asize=23)+'</div></div>',
 notes="If a question comes up that is not here, it becomes a row on the rules slide.")

S["defs"]=content("defs","Terms used in this deck",
 table(["Term","Meaning"],[
  ["Spend to revenue (MER)","Ad spend divided by revenue for the same period. Sale plan 24%, ceiling 28%."],
  ["Revenue incl. GST (calendar basis)","Total sales as the EE calendar records them, GST included. About 9% above Shopify net sales in November 2025 ($710k vs $651k)."],["Net revenue","Shopify net sales after discounts and returns, before GST; the basis for the research slides."],
  ["Margin after marketing (GPAM)","Revenue less product, shipping, packaging, transaction and advertising costs. Business target 26%; sale months run lower because discounts raise variable cost."],
  ["Popup reach","Share of site sessions in which the email popup was shown. 67 to 80% early in 2026; 23% in September."],
  ["Submit rate","Popup email submits divided by popup views. About 5% every month outside sales."],
  ["Returning-customer share","Share of revenue or orders from customers who had bought before. About 24% in a normal month."],
  ["Plateau","Days 3 to 12 of a sale, when daily revenue settles at about 5% of the sale total."],
  ["Engaged segment","Klaviyo profiles that opened or clicked in the last 30 or 90 days."]],[26,74],size=24),
 src="")

S["close"]=(f'<section id="close" data-transition="fade" style="background:{K}; color:{W}; font-family:{BODY}; padding:128px; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:40px">'
 f'{banner("BFCM 2026", bg=Y, fg=K, size=40)}'
 f'<h1 style="font-family:{DISP}; font-size:150px; line-height:1; text-align:center; color:{Y}; letter-spacing:2px">KEEP WORKING &amp;<br>KEEP EARNING!</h1>'
 f'<p style="font-size:30px; color:{GREY}; text-align:center">Six decisions this week. Pages live 13 November. Sale live Wednesday 18 November, midday.</p>'
 f'<aside>End on the decisions and the two dates.</aside></section>')

S["s-amend"]=section("s-amend","A","Amendment: concepts","Storyboards for the concepts so far. Each one is named, placed on its shoot day and marked as the hype or launch version.")
order=["cover","onepage","agenda",
       "scorecard","curve",
       "moves",
       "offer","bundles-alt","gifting","theme","jack","territories","journey","creative","hype-ads","launch-ads","midsale-eos-ads","shoot","shoot-warehouse","shoot-paddock","shoot-reddirt","shoot-worksite","deliverables","s-amend","concept-bucket","concept-frosty"]
S["scorecard"]=S["scorecard"].replace('text-transform:uppercase">The last three sales', 'text-transform:uppercase; background:#231f20; color:#fdfdfb; padding:14px 22px">The last three sales',1)
for n,k in enumerate(order,1):
    h=S[k].replace("{{N}}",str(n))
    assert h.count("<section")==1, k
    for m in re.findall(r'font-size:(\d+)px',h): assert int(m)>=22, (k,m)
    open(os.path.join(SL,f"{k}.html"),"w").write(h)
deck={"v":4,"attachments":{},"cover":"jack","createdOnFiles":{"v":1,"at":"2026-09-22T13:20:00Z"},"title":"DiggerLid BFCM 2026 Campaign Plan","order":order,
 "sections":{"intro":{"description":"The plan on one page and the agenda","start":"cover"},
  "research":{"description":"The last three sales side by side and the shape of a sale","start":"scorecard"},
  "strategy":{"description":"Eight moves for 2026","start":"moves"},
  "offer":{"description":"Offer, bundles, Christmas gifting, theme, creative deliverables","start":"offer"},
  "amendment":{"description":"Concept storyboards","start":"s-amend"}},
 "faces":{"roboto-condensed":{"family":"Roboto Condensed","href":"https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap"},
          "league-spartan":{"family":"League Spartan","href":"https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;600;700&display=swap"},
          "anton":{"family":"Anton","href":"https://fonts.googleapis.com/css2?family=Anton&display=swap"}},"designSystems":[]}
json.dump(deck,open(os.path.join(ROOT,"project","deck.json"),"w"),indent=1)
print("wrote",len(order),"slides")
