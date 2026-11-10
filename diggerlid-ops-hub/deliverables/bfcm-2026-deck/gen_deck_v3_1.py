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
    th="".join(f'<th style="width:{w}%; text-align:{"left" if (i==0 or not align_first_left) else "left"}">{h}</th>' for i,(h,w) in enumerate(zip(headers,widths)))
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
 f'<p style="font-size:26px; color:{GREY}">Executive and team briefing · September 2026 · v3.1</p></div>'
 f'<div style="display:flex; flex-direction:column; gap:28px">'
 f'{banner("Black Friday · Cyber Monday", bg=Y, fg=K, size=36)}'
 f'<h1 style="font-family:{HEAD}; font-size:168px; font-weight:700; line-height:0.95; text-transform:uppercase; color:{W}">BFCM 2026<br>Sale Plan</h1>'
 f'<p style="font-size:38px; color:{Y70}; line-height:1.3">What we learned last time, what we are running, what we are selling, and what has to be locked before the hype starts.</p></div>'
 f'<div style="display:flex; justify-content:space-between; align-items:end">'
 f'<p style="font-size:26px; color:{GREY}">Prepared by Matt Bedwell, Head of Growth · Data to 22 September 2026 · Basis: revenue incl. GST (EE calendar) unless marked net</p>'
 f'<p style="font-family:{DISP}; font-size:32px; color:{Y}; letter-spacing:1px">KEEP WORKING &amp; KEEP EARNING!</p></div>'
 f'<aside>Four parts: research, strategy, offer and creative, lock-up. Two appendix sections answer the questions people usually ask afterwards. Research slides are measured numbers; strategy, offer and lock-up slides are the proposal for this room to decide.</aside></section>')

S["onepage"]=content("onepage","The plan on one page",
 f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; flex:1">'
 +"".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:22px 24px; border:2px solid {K}">'
   f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>'
   for t,d,bg in [
   ("When","Hype Tue 17 and Wed 18 Nov. Sale Thu 19 Nov 6:00 AM to Wed 2 Dec 11:59 PM AEDT: 14 days, Black Friday on day 9, Cyber Monday on day 12. Christmas gifting from 30 Nov.",Y40),
   ("Target (to confirm)","Plan: $1.04M sale revenue incl. GST (about $960k net), the EE tool projection of 23 Sep on a $95k week; the calendar plan of record for November is $990k. Floor: $585k (2025 repeated). Stretch: $1.27M on the Aug to Sep run rate. Spend $249k (24% of revenue), ceiling 28%.","#ffffff"),
   ("Offer","Up to 25% off, grease excluded. DiggerShield $150 / $200 off. Gift with purchase at $299, $399 (free shipping) and $599. Three hero bundles at 30 / 40 / 50% off.",Y40),
   ("Theme","All Aussie Adventure: our own outback expert, four locations, one film and cut-downs. Sale mechanic: a knock-off deal drops at 3:30 PM every day.","#ffffff"),
   ("Channels","Meta paid social for acquisition (cold traffic to product pages), email and SMS for the base (segmented sends), organic and creator content for the theme, site pages built before hype.",Y40),
   ("What must be true first","Popup reach back above 50% on paid pages by 15 Oct. Pages live and tracked by 13 Nov. Bundle, DiggerShield and gift margins signed off by 30 Oct. Stock: $950k at RRP is 128% sell-through at $1.04M once the 15% discount is applied; incoming stock or a trimmed hero list by 30 Oct. Six decisions this week.","#ffffff")]) + '</div>',
 notes="If someone reads only one slide, this is it. Target is a proposal with two options; the forecast on file currently assumes a lower November, so the number needs a decision, not an assumption.")

S["changes"]=content("changes","What changes from 2025",
 table(["","2025","2026"],[
  ["Launch","Tue 18 Nov, 3:05 PM: day one was nine hours long","Thu 19 Nov, 6:00 AM AEDT: a full first day, launch send 7:00 AM, 14 days to Wed 2 Dec"],
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
  ("Research","What the last three sales measured, and answers to the five questions the team asked.",Y40),
  ("Strategy","Target and budget, eight moves, channel plan, paid, email and SMS, test markets, reactivation.","#ffffff"),
  ("Offer and creative","Discount, gift tiers, bundles, offer rules, the drop calendar, gifting, theme, production.",Y40),
  ("Lock-up","Timeline with hours, day-by-day comms, pages to build, stock and fulfilment, owners, risks, decisions.","#ffffff"),
  ("Appendix","Questions the exec and the team will ask, answered; definitions of the terms used.",Y40)],1))+'</div>')

# ------------------------------------------------------------------ 01 RESEARCH
S["s-research"]=section("s-research","01","Research","What the last three sales measured, and the five questions the team asked for 2026.")

S["scorecard"]=content("scorecard","The last three sales, side by side",
 table(["Measure","BFCM 2025","EOFY 2026","Father&#39;s Day 2026"],[
  ["Net revenue over the sale (14 days)","$535k","$543k","not measured here"],["Orders","1,759","2,107","not measured here"],
  ["Share of sale revenue in the first 48 hours","31%","19%",""],["Mid-sale revenue per day (days 3 to 12)","5.3%","4.9%",""],
  ["Share of sale revenue in the last 48 hours","15%","32%",""],["Revenue from returning customers","22%","29%",""],
  ["Sale landing page conversion","2.09%","3.38%","2.33%"],["Orders from landing page sessions","373","382","104"],
  ["Meta spend as % of revenue, the month","25.5%","25%",""]],[40,20,20,20],size=25,hl=6)+
 note("Two sales of the same size with opposite shapes. BFCM front-loads because the urgency is the launch. EOFY back-loads because the urgency is 30 June. The middle ten days ran at about 5% of sale revenue per day in both."),
 src="Shopify analytics",notes="Father&#39;s Day totals were not part of this review; only its landing page was measured.")

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
def bars(vals,color):
    out=""
    for i,v in enumerate(vals,1):
        h=int(v/20.0*280)
        out+=(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px">'
              f'<p style="font-size:24px; color:{K90}">{v:.0f}%</p><div style="width:40px; height:{max(h,4)}px; background:{color}; border:2px solid {K}"></div><p style="font-size:24px; color:{MUTE}">{i}</p></div>')
    return out
S["curve"]=content("curve","The daily shape we are planning to",
 f'<div style="display:flex; gap:32px; flex:1">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700">BFCM 2025: share of sale revenue by day</h3><div style="display:flex; gap:6px; align-items:end; height:360px; border-bottom:2px solid {K}">{bars(bfcm,Y)}</div></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700">EOFY 2026: share of sale revenue by day</h3><div style="display:flex; gap:6px; align-items:end; height:360px; border-bottom:2px solid {K}">{bars(eofy,K80)}</div></div></div>'
 f'<div style="display:flex; gap:24px">{big("30%","of sale revenue in the first 48 hours at BFCM. On a $535k base target that is about $160k for the launch weekend.")}{big("5%","per day through the middle. The daily drops and the mid-sale send exist to lift this number.",bg="#ffffff")}{big("70%","of launch-day buyers were new customers. The launch is an acquisition play; keep prospecting on.")}</div>',
 src="Shopify analytics",notes="Plan spend and stock to the front for BFCM. The 30% and 5% figures are measured from 2025; the dollar figure follows from whichever target the room picks.")

reach=[("Jan","67"),("Feb","70"),("Mar","64"),("Apr","80"),("May","44"),("Jun","53"),("Jul","33"),("Aug","34"),("Sep","23")]
rb="".join(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px"><p style="font-size:26px; font-weight:700">{v}%</p><div style="width:88px; height:{int(int(v)/80*280)}px; background:{Y if int(v)>=50 else K80}; border:2px solid {K}"></div><p style="font-size:25px; color:{MUTE}">{m}</p></div>' for m,v in reach)
S["reach"]=content("reach","Before more traffic: the popup reaches a quarter of visitors",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:3; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700">Share of sessions that saw the email popup, 2026</h3><div style="display:flex; gap:10px; align-items:end; height:360px; border-bottom:2px solid {K}">{rb}</div></div>'
 f'<div style="flex:2; display:flex; flex-direction:column; gap:18px">{big("5%","of viewers submit, every month except during the EOFY sale. The popup itself is not the problem.",bg="#ffffff")}{big("921","signups in September. At January reach on September traffic the same month would have produced about 2,800.")}{big("$65","contribution per signup in the first year, before allowing for people who would have bought anyway. The most an extra email is worth.",bg="#ffffff")}</div></div>',
 src="Alia, Shopify, Klaviyo",notes="The first job of the traffic and email push: audit the popup trigger rules and page targeting on the paid landing pages, restore 50%+ reach on paid traffic by 15 October, and check it weekly.")

# ------------------------------------------------------------------ 02 STRATEGY
S["s-strategy"]=section("s-strategy","02","Strategy","Target and budget, eight moves, the channel plan, and how paid, email and SMS each earn their place.")

S["target"]=content("target","Target: three cases on one basis (revenue incl. GST, as the EE calendar)",
 table(["Case","Sale revenue (2 hype + 14 days)","How it is derived","Meta spend at 20% / 24% / 28%"],[
  ["Floor: 2025 repeated","$585k (net $535k)","2025 sale, 18 Nov to 1 Dec, restated on the calendar basis","$117k / $140k / $164k"],
  ["Plan: EE tool, 23 Sep run","$1.04M (net about $960k)","10.9× the weekly BAU of Sep to Oct 2025 gave Nov 2025; applied to a $95k week (July was $92.7k, August $119k) = $1,037,375. The calendar&#39;s preloaded plan for November is $990k","$207k / $249k / $290k"],
  ["Stretch: current run rate","$1.27M (net about $1.16M)","Same multiple on Aug to Sep 2026 BAU ($118k/wk)","$254k / $305k / $356k"]],[20,22,40,18],size=24)
 +f'<div style="display:flex; gap:24px">{big("1.72x","EOFY 2026 grew on EOFY 2025 while BAU grew 1.82x: the sale scales with BAU, which is why the multiple method holds.")}{big("$1.04M","is the tool&#39;s projection at a 25% sale MER (24% effective with conservative hype spend), 5% above the calendar&#39;s $990k plan of record. Profit in the tool: $166k, before the corrections on the next slides.",bg="#ffffff")}{big("$118k","weekly BAU in Aug to Sep 2026 against the $95k week in the tool. The base week is the difference between $1.04M and $1.27M; $95k is the conservative choice.")}</div>',
 src="EE calendar 2025 and 2026, Shopify, EE BFCM tool",notes="The EE multiple method is validated by EOFY 2026 and is the plan case. The tool uses a $95k base week, below the Aug to Sep run rate; the room confirms the base week and the spend ceiling.")

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

moves=[("1 · Start wider","Test USA, NZ, TikTok and YouTube with a fixed budget and a kill rule. More expansive hype, because 70% of launch buyers are new."),
       ("2 · 13-day sale, 2.5-day hype","Wed 18 Nov to Mon 30 Nov. Hype from Sat 14 Nov to a capture page, not a preview of the sale page."),
       ("3 · Stronger theme","All Aussie Adventure: one character, four locations, one shoot. Daily 3:30 PM knock-off drop as the sale mechanic."),
       ("4 · Cut and run","Written rules for stopping spend: a landing page under 1.5% by midday or two days over 30% spend-to-revenue. Decided in advance, not on the day."),
       ("5 · Mid-sale offer","A bonus-gift or collaboration moment mid-sale, sent to the engaged segment. Returning share was 43% when segmented and flat when blasted."),
       ("6 · Pre-game check","Pages built and tracked by 13 Nov. Popup reach above 50% on paid pages. Ad sets and sends scheduled before hype."),
       ("7 · Better reactivation","Email and SMS to the 12,745 first-time buyers of the last year; grease reorder nudges to grease buyers."),
       ("8 · Beat the hangover","A December plan that is not another discount: gift guide, new product launch, shipping cut-offs. July 2026 (after EOFY) was a loss month at 42% spend-to-revenue.")]
S["moves"]=content("moves","Eight moves for 2026",
 f'<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:18px; flex:1">'+"".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{"#ffffff" if i%2 else Y40}; padding:20px 22px; border:2px solid {K}"><h3 style="font-family:{HEAD}; font-size:27px; font-weight:700; line-height:1.1; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate(moves))+'</div>',
 src="Planning notes, 2025 sale review",notes="The eight moves from the strategy page of the notes, each with the number behind it.")

S["unit"]=content("unit","Profit per sale order: the tool&#39;s number and the corrected number",
 table(["Per sale order (with gift, 18% / 6% uptake in the tool)","EE tool, 23 Sep run","Corrected (product 32%, gift uptake 43% / 15%)"],[
  ["Revenue per order","$266.28","$266.28 (fewer, larger orders if AOV holds at 2025 sale levels)"],
  ["GST","$19.72 (7.4%)","$19.72: confirmed against Nov 2025"],
  ["Media at 24.1% MER","$64.04","$64.04"],
  ["Variable costs incl. gifts","$128.85 (48.4%)","about $139.20 (52.3%): +$5.33 product cost, +$5.03 gifts"],
  ["Fixed costs per order","$11.12","$11.12"],
  ["Profit per order","$42.55 (16.0%)","about $32 (12.1%)"],
  ["Total profit on 3,896 orders","$165,771 (after $20k of hype-day losses)","about $125k"]],[36,26,38],size=24)
 +note("Estimates: the tool&#39;s formula is not fully visible, so the corrected column moves each line by the input difference only. Last run of the tool showed $210k at a 20% MER and 25% product cost; the inputs have moved twice and the answer has moved with them. Sale MER at 24% matches November 2025."),
 src="EE BFCM tool section 7 (23 Sep), EE calendar drivers, Shopify 2025 order values",notes="The sale is profitable at about three quarters of what the tool shows. Product cost and gift uptake are the two open inputs.")

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
 +card("Budget (EE tool, 23 Sep run)",["Total $249,489 = 24.1% of $1.04M (sale MER 25%, conservative hype spend): Meta $219,550 (88%), TikTok $24,949 (10%), Google $4,990 (2%)","Hype days $7,391 each; sale days $16,765 each (smoothed)","Ceiling 28% = $290k; 2025 ran at 24%, so the plan holds at last year&#39;s efficiency","Test markets (USA, NZ, TikTok, YouTube) sit inside the 12% non-Meta share plus one TOF campaign, each with a day-4 kill rule"],accent=Y,lsize=24)
 +card("Meta structure (from the campaign plan)",["Sale campaigns $121.6k: TOF $46.1k (best-TOF duplicate, ASC broad, CIBS optional), TOM $42.4k (ASC excluding customers; no-exclusions for the mid-sale offers), MOF $21.6k, BOF $11.5k","Evergreen kept live $97.9k: TOF interest and broad $42.9k, Advantage+ $33.8k, MOF $15.5k, BOF $5.8k","Hype days $6,504 each on warm sale campaigns and evergreen only; sale TOF starts day 1 at $2,951 and settles at $3,319","Cold TOF lands on grease and PRO Mat product pages; TOM/MOF/BOF on the sale page"],accent=K80,lsize=24)
 +card("Shape it to the curve",["With the custom curve on, smoothed spend gives day-1 MER 8.5%, plateau days 32%, Black Friday 23%, the last two days 18 to 20%: no loss days, but plateau days clear only $3.5k","Shaped (&#39;clunky&#39;) spend from the tool: $47k day 1, $30k day 2, $12.5k plateau days, $17.5k Black Friday, $20k and $22k on the last two days","Recommendation: shaped spend; hold plateau days at $12.5k and only add to the last two days if day-12 MER is under 25%","Daily 8 AM check with the cut rules on the measurement slide"],accent=Y,lsize=24)+'</div>',
 src="EE BFCM tool sections 8 and 9 (23 Sep), meta-campaigns.csv",notes="The Meta plan file now matches the tool: $219,550 over two hype days and 14 sale days. Its dates still start 18 Nov; the amounts by day number carry over to the 19 Nov start unchanged.")

S["emailplan"]=content("emailplan","Email and SMS plan",
 f'<div style="display:flex; gap:24px">{big("29.4%","of popup signups buy; about 85% of that in the first month. Emails collected now pay now.")}{big("4 to 7%","of pre-sale signups who had not bought went on to buy during a sale. Capture is not a launch-day payload.",bg="#ffffff")}{big("43%","returning-customer share on Cyber Monday 2025 after a segmented send; blasts left it flat.")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("October to 13 November",["Restore popup reach on paid pages; then capture continuously","Split the welcome flow by the popup interest answer: grease offer and reorder cadence, or machine-fit guide","Reactivation to the 12,745 first-time buyers of the last year","Build the segments: engaged 30 and 90 days, grease buyers, SMS list"],accent=Y,lsize=24)
 +card("Hype and sale",["Hype sends to a first-access capture page with a countdown","Sale-specific popup (early access or bonus gift), not a discount","Full database on launch and last day only; engaged segments for everything else","3:30 PM drop by SMS daily and by email to the engaged segment"],accent=K80,lsize=24)
 +card("After the sale",["Thank-you and gift guide on 1 Dec; shipping cut-off on 2 and 9 Dec","New product launch send","No December list buying: December signups convert worst (21.7%)","Grease reorder nudge at about 90 days for sale buyers"],accent=Y,lsize=24)+'</div>',
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
 +card("Gift with purchase",["$299 spend: Magnet Tool Mat","$399 spend: free shipping","$599 spend: Drawbar Cover","Thresholds sit just above the $305 first-order average; the EE tool suggests $335 and $450 minimums; gift cost $14 (magnet mat) and $17 (drawbar)"],accent=K,tsize=32,lsize=26)
 +card("Bundles",["All existing bundles stay live at sale pricing","Three new hero bundles at 30 / 40 / 50% off (next slide)","Bundles are the basket-size lever; the sitewide percentage is the traffic lever"],accent=Y,tsize=32,lsize=26)+'</div>'
 +note("Excluding grease is a decision with a number attached: the grease system was 33% of the 2025 sale and grease packs carried a 14% discount. Options: exclude it and accept a smaller grease share, or run grease as knock-off drops (40-piece packs) instead of a sitewide cut. The $399 free-shipping tier matches the existing signup offer, which converts signups at 37%."),
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

S["bundles"]=content("bundles","Three new hero bundles",
 f'<div style="display:flex; gap:24px; flex:1">'
 +card("Ultimate Excavator Bundle · 30% off",["1× Pro Excavator Enclosure","1× Drawbar Cover","1× PRO Mat Plus","10× Digger Wipes","1× Keyring","1× Magnet Tool Mat"],accent=Y,tsize=30,lsize=26)
 +card("Hardcore Tradie Bundle · 40% off",["2× PRO Mat Plus","1× Drawbar Cover","1× Proper Thicc Hoodie","10× Digger Wipes","1× Boom Bottle Opener","1× Magnet Tool Mat"],accent=K,tsize=30,lsize=26)
 +card("Ludicrous Bundle · 50% off",["1× PRO Mat and 2× PRO Mat Plus","2× Magnet Tool Mat","1× Drawbar Cover","1× Quicky Cover","1× Hoodie and 1× Bottle Opener","20× Digger Wipes"],accent=Y,tsize=30,lsize=26)+'</div>'
 +note("Names and contents as drafted in the planning notes. Margin at 30 / 40 / 50% and stock for each component need a costing pass by 30 October. PRO Mat Plus anchors all three: 93.5% of its buyers are new to the brand."),
 src="Planning notes",notes="The 50% bundle is a headline as much as a product. Check it against cost before it goes on the page.")

drops=[("Thu 19","Launch day: whole offer live, no drop"),("Fri 20","Grease 40-piece pack deal (grease was a third of last year&#39;s sale)"),("Sat 21","PRO Mat Plus colour of the day"),("Sun 22","Offer 1, convert considerers: Quicky Cover"),("Mon 23","DiggerShield $200 day"),("Tue 24","Ultimate Excavator Bundle feature"),("Wed 25","Offer 2, increase AOV: gift-tier push"),
       ("Thu 26","Phone cradle and accessories kit"),("Fri 27","Black Friday: Mystery Box and the Ludicrous Bundle"),("Sat 28","Offer 3, drive repeat: grease reorder deal"),("Sun 29","Universal and engine covers"),("Mon 30","Cyber Monday: Hardcore Tradie Bundle"),("Tue 1 Dec","Pro Enclosure"),("Wed 2 Dec","Last knock-off of the year: free shipping on everything")]
S["drops"]=content("drops","Knock-off drop calendar (draft for the team)",
 f'<div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px 28px">'+"".join(f'<div style="display:flex; gap:16px; align-items:center; border-bottom:1px solid {K}; padding:0 0 8px 0"><p style="font-family:{DISP}; font-size:26px; width:120px; letter-spacing:1px">{d}</p><p style="font-size:25px; line-height:1.25; flex:1">{t}</p></div>' for d,t in drops)+'</div>'
 +note("One drop a day at 3:30 PM AEDT, 24 hours each; the EE mid-sale offers (convert considerers, increase AOV, Black Friday Mystery Box, drive repeat) sit on their tool dates re-based to the 19 Nov start. Timing checks out: the 6 to 9 PM block was the biggest buying window in 2025 (115 to 120 orders an hour). Order is a draft; stock and margin per drop to confirm."),
 src="Planning notes, concept board",notes="Thirteen days, twelve drops. The team owns the final order; the mechanic is the point.")

S["gifting"]=content("gifting","The gifting path (issue 1 from the notes)",
 f'<div style="display:flex; gap:24px">{big("34%","of PRO Mat Plus buyers are women, in practice gift buyers. The gift buyer exists; the site does not show them a path.")}{big("0.5%","of visitors to the Father&#39;s Day gift page ordered (999 viewers, 7% reached a product). A generic gift page did not work.",bg="#ffffff")}{big("30 Nov","Christmas gift collection and gift-buyer ad angles go live on Cyber Monday; gift guide email on 1 Dec.")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("Proposed gift path",["Gift entry on the sale page and in the navigation","Three gift tiers matching the gift-with-purchase thresholds: under $150 (grease kit, accessories), $299 (PRO Mat Plus with magnet mat), $599 (bundle)","A two-question machine finder for buyers who do not know the model","Gift note or gift card at checkout; delivery date shown on every gift surface"],accent=Y)
 +card("What not to repeat",["A standalone gift page with no product depth (2.3 pages per session on the FD gift page)","Sending gift traffic to the sale page, which leads with grease","Leaving the shipping cut-off implicit"],accent=K80)+'</div>',
 src="PostHog, Shopify, campaign calendar",notes="The gift buyer converts once they reach a product. Build the path to the product, not a page about gifts.")

S["theme"]=content("theme","Theme: All Aussie Adventure, with a daily knock-off drop",
 f'<div style="display:flex; gap:24px; flex:1">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{K}; color:{W}; padding:34px; border:2px solid {K}">{banner("Theme · All Aussie Adventure", bg=Y, fg=K, size=27)}'
 f'<p style="font-size:26px; line-height:1.35; color:{W}">A parody of the outback-bumbler format with our own character: a khaki-clad expert tours four locations, dispenses machinery wisdom, and wrecks everything except the covered gear. Every episode ends with the machine in trouble and the cover fine.</p>'
 f'<p style="font-size:25px; line-height:1.35; color:{Y70}">Strong for long-form social and shares. Weak on urgency, so every episode ends on an offer card and the drop mechanic does the urgency work.</p></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{Y40}; padding:34px; border:2px solid {K}">{banner("Mechanic · Knock-Off Deals", size=27)}'
 f'<p style="font-size:26px; line-height:1.35">A new deal drops at 3:30 PM sharp every day of the sale: genuine gear at knock-off prices. The 3:30 stamp is the daily mark in email, SMS and on the page.</p>'
 f'<p style="font-size:25px; line-height:1.35; color:{K90}">The middle ten days ran at about 5% of sale revenue per day in both big sales; the drops give people a reason to come back on those days. Fallback launch film if the Adventure edit slips: Take Cover, already shot in July.</p></div></div>',
 src="Planning notes pp.10 and 11, concept board",notes="The notes pair the Adventure theme with the four-location shoot. The concept board rated it strongest for brand love and weakest for urgency; the mechanic covers that.")

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

S["deliverables"]=content("deliverables","Creative deliverables and deadlines (proposal)",
 table(["Asset","Use","Count","Due","Owner"],[
  ["Adventure hero film (4 episodes)","Launch, organic, sale page","1 film, 4 episodes","10 Nov edit locked","Creative [name]"],
  ["Cut-downs 15s and 30s with offer end-cards","Paid social by episode","8","12 Nov","Creative [name]"],
  ["Hype teasers (video vibes, image offer)","Hype sends and ads 14 to 16 Nov","6","11 Nov","Creative [name]"],
  ["Bundle and gift-tier stills","Bundle page, ads, emails","12","6 Nov (warehouse day)","Creative [name]"],
  ["Knock-off drop template","Daily SMS, email, page module","1 template, 12 fills","12 Nov","Creative and Email [names]"],
  ["Email and SMS templates","Launch, drops, mid-sale, close","6","12 Nov","Email [name]"],
  ["Sale, bundle, collection, capture pages","Site","4 pages","13 Nov live and QA&#39;d","Web [name]"],
  ["Gift entry, gift guide, cut-off banner","Site, 30 Nov onward","3","27 Nov","Web [name]"]],[30,24,14,18,14],size=24),
 src="Planning notes, EE tool section 6",notes="The EE tool (23 Sep, 85% volume) sizes the creative at 53 to 65 assets (24 to 30 video, 29 to 35 static): 9 to 13 for hype, 13 to 17 live at launch, 17 across the mid-sale offers, 7 to 9 each for Black Friday and last chance. The counts above cover it. Hard constraint: 13 November.")

# ------------------------------------------------------------------ 04 LOCK-UP
S["s-lockup"]=section("s-lockup","04","Lock-up","Timeline with hours, day-by-day sends, pages to build, stock and fulfilment, owners, risks and the decisions needed.")

tl=[("Tue 17 and Wed 18 Nov","Hype","Two hype sends to engaged segments; warm-audience ads only (TOM, MOF, BOF). All hype traffic to the first-access capture page with a countdown."),
    ("Wed 18 Nov, by close of day","Pre-game","Pages live and QA&#39;d, tracking verified, popup firing on paid pages, ad sets and sends scheduled, gift and bundle stock confirmed."),
    ("Thu 19 Nov, 6:00 AM AEDT","Launch (day 1)","Sale live at 6:00 AM so day one is a full day (2025 launched at 3:05 PM). Launch email and SMS 7:00 AM. Cold traffic to product pages; 19% of sale revenue expected on day one and 31% by the end of day two (custom curve)."),
    ("Fri 20 to Thu 26 Nov, 3:30 PM daily","Days 2 to 8","Knock-off drop at 3:30 PM daily. Mid-sale offer 1 (convert considerers) Sun 22 Nov, offer 2 (increase AOV) Wed 25 Nov. Daily 8 AM scorecard and cut rules."),
    ("Fri 27 Nov","Black Friday (day 9)","Full-database send. Mystery Box as the drop. Extra creative. Highest-spend day of the plateau."),
    ("Sat 28 to Mon 30 Nov","Days 10 to 12","Offer 3 (drive repeat) Sat 28. Cyber Monday Mon 30 Nov: full-database send, last knock-off weekend. Christmas gift collection live the same day."),
    ("Tue 1 to Wed 2 Dec, closes 11:59 PM AEDT","Days 13 and 14","Last chance send 7 AM and sale-ends-midnight 5 PM on Wed 2 Dec. Optional one-day extension Thu 3 Dec to engaged non-buyers."),
    ("3 to 9 Dec","After","Thank-you and gift guide; shipping cut-off on site; new product launch; cut-off reminder 9 Dec.")]
S["timeline"]=content("timeline","Timeline: 2 hype days plus 14 sale days, 19 Nov to 2 Dec, all times AEDT",
 f'<div style="display:flex; flex-direction:column; gap:8px">'+"".join(f'<div style="display:flex; gap:20px; align-items:start; border-bottom:2px solid {K}; padding:0 0 8px 0"><p style="font-family:{HEAD}; font-size:25px; font-weight:700; width:330px; line-height:1.15">{d}</p><p style="font-family:{DISP}; font-size:24px; width:210px; letter-spacing:1px; text-transform:uppercase; line-height:1.2">{t}</p><p style="flex:1; font-size:23px; line-height:1.3; color:{K90}">{x}</p></div>' for d,t,x in tl)+'</div>'
 +note("Decision made: 14 days from Thu 19 Nov. The EE tool export of 23 Sep still runs Wed 18 Nov to Tue 1 Dec with hype on 16 and 17; its email flow and Meta plan carry the same dates, and the shared calendar shows 23 Nov. All four need the one-day shift, or the deck moves to 18 Nov. Hours from 2025: orders ran 85 to 100 an hour from 7 to 11 AM and 115 to 120 an hour from 6 to 9 PM.",size=22),
 src="Planning decision, EE tool export 23 Sep, campaign calendar",notes="Black Friday lands on day 9 and Cyber Monday on day 12; the last two days run into December, so the last-chance push is Wednesday 2 December, not Cyber Monday.")

comms=[("H1 Tue 17 Nov","Email","Engaged 250 days + window shoppers 14 days","Sale is coming: our biggest sale of the season starts soon"),
       ("H2 Wed 18 Nov","Email","Engaged 90 days + window shoppers","Hype 2, plain text: biggest sale of the year, first access tomorrow 6 AM"),
       ("D1 Thu 19 Nov 7:00 AM","Email + SMS","Full database; SMS list","Sale live: the whole offer, bundles, gift tiers"),
       ("D2 Fri 20 Nov","Email","Engaged 90 days","Top sale picks; first knock-off drop 3:30 PM"),
       ("D3 Sat 21 Nov","Email","Engaged 250 days","Product spotlight (episode two)"),
       ("D4 Sun 22 Nov","Email + SMS","Engaged 250 days + window shoppers","Mid-sale offer 1: convert considerers"),
       ("D6 Tue 24 Nov","Email","Engaged 250 days","Product spotlight"),
       ("D7 Wed 25 Nov","Email + SMS","Engaged 250 days + window shoppers","Mid-sale offer 2: increase AOV (bundle and gift tiers)"),
       ("D8 Thu 26 Nov","Email","Engaged 90 days","Social proof"),
       ("D9 Fri 27 Nov","Email + SMS","Full database","Black Friday: Mystery Box"),
       ("D10 Sat 28 Nov","Email + SMS","Engaged 250 days + window shoppers","Mid-sale offer 3: drive repeat (grease reorder)"),
       ("D12 Mon 30 Nov","Email + SMS","Full database","Cyber Monday: sale updates, last knock-off weekend"),
       ("D14 Wed 2 Dec 7 AM / 5 PM","Email + SMS","Full database; engaged 250 days at 5 PM","Last chance; sale ends midnight"),
       ("DX1 Thu 3 Dec","Email","Engaged 30 days, excluding sale buyers","Sale extended, today only (optional)")]
S["comms"]=content("comms","Sends, day by day (from the email flow, re-dated to the 19 Nov start)",
 table(["When","Channel","Audience","Message"],comms,[22,13,30,35],size=22)+note("Daily 3:30 PM knock-off drop by SMS and to the engaged-30-day segment on every sale day (not listed per row). Exclusions: bounces on every send; sale buyers on the extension. Attributed to email in 2025: $82k and 197 orders across six sends (15% of the sale); the launch send alone $37k. The EE email flow export (17 sends, 16 Nov to 1 Dec) has no Cyber Monday send and an empty Sat 28 Nov row; this table adds both and re-dates to the 19 Nov start.",size=22),
 src="email-flow.csv, Klaviyo 2025 send log",notes="Four full-database sends: launch, Black Friday, Cyber Monday, last chance. Everything else is segmented.")

S["pages"]=content("pages","Pages and site work to build",
 table(["Item","What it does","Benchmark","Due","Owner"],[
  ["Sale landing page","Warm traffic home; grease and PRO Mat first, bundles, big tickets below","3.4% conversion, 10% add to cart, 5 pages per session","13 Nov","Web [name]"],
  ["Bundle page","Three hero bundles and existing bundles","","13 Nov","Web [name]"],
  ["Collection page","Everything on sale, sortable","","13 Nov","Web [name]"],
  ["Homepage takeover","Sale banner, drop of the day, gift entry","Homepage converted 8 to 10% in past sales","18 Nov","Web [name]"],
  ["First-access capture page","Where hype traffic lands: countdown, email and SMS capture","4,300 hype sessions last cycle","13 Nov","Web and Email [names]"],
  ["Sale popup","Early access or bonus gift; replaces the discount popup during the sale","Reach 50%+, submit 5%","13 Nov","Growth [name]"],
  ["Drop module","3:30 PM badge, countdown, today&#39;s deal","","13 Nov","Web [name]"],
  ["Tracking QA","Cart add, checkout, order events on every page","Cart adds must exceed orders","13 Nov","Web [name]"],
  ["Gift entry and cut-off banner","Gift path, delivery dates","","27 Nov","Web [name]"]],[22,36,22,10,10],size=23),
 src="Landing page review",notes="Nine items, one deadline. The capture page and the sale popup are the two pieces that did not exist last year.")

S["ops"]=content("ops","Stock, fulfilment and service (to confirm)",
 f'<div style="display:flex; gap:24px">{big("740","orders on day one at the $1.04M plan (19% of 3,900 sale orders), against 251 on launch day 2025: plan fulfilment, packaging and service for three times last year&#39;s peak.",bg="#ffffff")}{big("$950k","stock at RRP against $1.04M: 128% sell-through after the 15% discount (109% by RRP in the tool), about $270k short. Gift units: about 1,675 magnet mats and 585 drawbars at the 2025 spread (tool: 700 and 235).")}{big("[ ]","bundle kits pre-packed before launch: components for three hero bundles at the volumes the drops will drive.",bg="#ffffff")}</div>'
 +f'<div style="display:flex; gap:24px; flex:1">'
 +card("Stock and warehouse",["Gift-with-purchase stock reserved by 10 Nov: about 1,700 magnet mats and 600 drawbar covers at the plan, more at stretch","Stock-out plan: which SKUs come off the sale first, and the substitute gift when magnet mats run out","Bundle components kitted; a stop rule when any component runs out","Drop-of-the-day stock confirmed the day before each drop","Warehouse shoot day (6 Nov) doubles as the stock check"],accent=Y)
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
 +card("Risks from the notes, with the answer",["Gifting path: gift entry, tiers and finder on the sale page; Christmas collection 30 Nov","Landing page late: 13 Nov deadline, built before hype, source-split traffic, 3.4% benchmark","Hangover: gift guide, new product, cut-off messaging; no December list buying","Overspending: 28% ceiling, 25% target, written cut rules, daily 8 AM check","Popup submit collapses in a sale (2.3% in June): sale-specific popup with early access or a bonus gift","Edit slips: Take Cover film as the fallback launch"],accent=K80,lsize=24)+'</div>',
 src="Planning notes p.9, 2025 sale review",notes="The four possible issues from the notes each have a mitigation; two more risks were added from the data.")

S["measure"]=content("measure","Measuring the sale: the 8 AM scorecard and the cut rules",
 table(["Row","Target or benchmark","Rule if missed","Source"],[
  ["Revenue against the daily shape","EE plan: day 1 28%, day 2 12%, day 3 10%, plateau 3 to 7%, Black Friday 5%, last day 7%; 2025 measured: 31% in 48h, 5% per day","Under 80% of plan for two days: review spend and creative","Shopify"],
  ["Meta spend to revenue","24% (EE plan 25% sale MER, 24% effective; 2025 actual 24%); ceiling 28%","Over 30% for two days: cut broad prospecting","Meta, Shopify"],
  ["Sale page conversion by source","3.4% blended; social over 2%; direct over 6%","Social under 1.5% by midday: pull the broad set","Shopify"],
  ["Popup reach and submits","Reach over 50%; submit about 5% of views","Reach under 40%: check triggers the same day","Alia, Shopify"],
  ["Returning-customer share","Over 25% on segmented-send days","Under 20%: check the segment and the send","Shopify"],
  ["Average order and bundle share","AOV over $315; bundles [ ]% of orders","AOV under $290: push bundles and gift tiers in the drops","Shopify"],
  ["Drop response","Orders 3:30 to 5:30 PM above the same window the day before","Flat two days running: change the drop type","Shopify"]],[26,30,30,14],size=23),
 src="",notes="One person reads this at 8 AM and makes the calls. The rules are written now so nobody argues them on the day.")

S["decisions"]=content("decisions","Decisions needed this week",
 f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; flex:1">'+"".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{"#ffffff" if i%2 else Y40}; padding:22px 24px; border:2px solid {K}"><h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate([
  ("Target","Plan $1.04M incl. GST (EE tool, 23 Sep run, $95k base week) or stretch $1.27M on the current run rate; spend $249k (24%), ceiling 28%."),
  ("EE tool corrections","Still open: product cost 32%, gift uptake 43% / 15%, stock cover; re-date the tool, email flow and Meta plan to 19 Nov to 2 Dec (or move the deck to 18 Nov)."),
  ("Offer","25% ex-grease, DiggerShield $150 / $200, gift tiers $299 / $399 / $599, bundles at 30 / 40 / 50%, stacking and exclusions."),
  ("Theme and fallback","All Aussie Adventure with the knock-off drops; Take Cover as the fallback film."),
  ("Test markets and price test","Budgets and kill rules for USA, NZ, TikTok, YouTube; DiggerShield price test yes or no."),
  ("Owners","Names against the eight roles, and who owns the popup reach fix due 15 Oct.")]))+'</div>',
 notes="Six decisions unblock the build. Everything else in the deck is execution against dates.")

# ------------------------------------------------------------------ APPENDIX
S["s-appendix"]=section("s-appendix","05","Appendix","The questions people ask after a plan like this, answered; and what the terms mean.")

S["faq-exec"]=content("faq-exec","Questions the exec will ask",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:1">'+qa([
  ("What are we targeting and what does it cost?","Plan $1.04M sale revenue incl. GST, the EE tool projection on a $95k week, at $249k of spend (24%). Floor $585k if we only repeat 2025; stretch $1.27M on the current run rate. Profit at the plan is $166k in the tool and about $125k after the product-cost and gift-uptake corrections."),
  ("Why 25% and not 30%?","Every point of discount lifts variable cost; 2025 delivered $535k at a sitewide discount with spend at 25.5%. Bundles and gift tiers do the work a deeper discount would, without cutting margin on everything."),
  ("Why exclude grease, and what does it cost?","Grease is the one product that repeats and the base for December reorders. But it was 33% of the 2025 sale and grease packs carried a 14% discount, so exclusion is a decision: either accept a smaller grease share or run grease as knock-off drops instead of a sitewide cut."),
  ("What stops us overspending?","A 28% ceiling on a 24% plan, spend shaped to the revenue curve rather than smoothed (with the 2025-shaped curve the tool no longer shows loss days, but plateau days clear only $3.5k), written cut rules, and one person reading the scorecard at 8 AM. Cold traffic no longer goes to the sale page.")],qsize=26,asize=23)+'</div><div style="flex:1">'+qa([
  ("Why All Aussie Adventure? Is the IP risk real?","It fits the audience and gives us a content series beyond the sale. The risk is managed by using our own character and format parody only, with a legal read before paid placement. Take Cover is the fallback."),
  ("Why spend in the USA and NZ at all?","International was 27% of 2025 sale revenue at a $570 average order, more than double Australia. The tests are capped with a day-4 kill rule; the aim is efficient international revenue, not less of it."),
  ("What if the film is not ready?","Edit lock is 10 Nov, three days before pages go live. If it slips, the Take Cover film (shot in July) launches and the Adventure episodes run mid-sale."),
  ("What happens after Cyber Monday?","Christmas gifting from 30 Nov, gift guide 1 Dec, a new product launch, shipping cut-offs on 2 and 9 Dec. No further discounting and no December list buying.")],qsize=26,asize=23)+'</div></div>',
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
 f'<p style="font-size:30px; color:{GREY}; text-align:center">Six decisions this week. Pages live 13 November. Sale live Thursday 19 November, 6:00 AM.</p>'
 f'<aside>End on the decisions and the two dates.</aside></section>')

order=["cover","onepage","changes","agenda",
       "s-research","scorecard","mix","wellpoorly","lpresults","repeat","questions","curve","reach",
       "s-strategy","target","eeinputs","unit","moves","channels","paid","emailplan","tests","hangover",
       "s-offer","offer","rules","bundles","drops","gifting","theme","production","character","deliverables",
       "s-lockup","timeline","comms","pages","ops","owners","lockup","measure","decisions",
       "s-appendix","faq-exec","faq-team","defs","close"]
for n,k in enumerate(order,1):
    h=S[k].replace("{{N}}",str(n))
    assert h.count("<section")==1, k
    for m in re.findall(r'font-size:(\d+)px',h): assert int(m)>=22, (k,m)
    open(os.path.join(SL,f"{k}.html"),"w").write(h)
deck={"v":4,"createdOnFiles":{"v":1,"at":"2026-09-22T13:20:00Z"},"title":"DiggerLid BFCM 2026 Campaign Plan","order":order,
 "sections":{"intro":{"description":"The plan on one page, what changes from 2025, agenda","start":"cover"},
  "research":{"description":"What the last three sales measured and the five questions answered","start":"s-research"},
  "strategy":{"description":"Target, eight moves, channels, paid, email and SMS, tests, reactivation","start":"s-strategy"},
  "offer":{"description":"Offer, rules, bundles, drops, gifting, theme, production, deliverables","start":"s-offer"},
  "lockup":{"description":"Timeline, sends, pages, ops, owners, risks, measurement, decisions","start":"s-lockup"},
  "appendix":{"description":"Exec and team questions answered; definitions","start":"s-appendix"}},
 "faces":{"roboto-condensed":{"family":"Roboto Condensed","href":"https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap"},
          "league-spartan":{"family":"League Spartan","href":"https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;600;700&display=swap"},
          "anton":{"family":"Anton","href":"https://fonts.googleapis.com/css2?family=Anton&display=swap"}},"designSystems":[]}
json.dump(deck,open(os.path.join(ROOT,"project","deck.json"),"w"),indent=1)
print("wrote",len(order),"slides")
