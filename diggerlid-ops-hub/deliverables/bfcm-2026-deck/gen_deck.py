#!/usr/bin/env python3
"""Generate the DiggerLid BFCM 2026 campaign deck files (Slides artifact format)."""
import os, json, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(ROOT, "project", "slides"); os.makedirs(SL, exist_ok=True)

K="#231f20"; K90="#3a3637"; K80="#4f4b4c"; Y="#f5eb19"; Y70="#f8f163"; Y40="#fbf7a3"; W="#fdfdfb"; MUTE="#4f4b4c"
HEAD="'Roboto Condensed', 'Arial Narrow', Arial, sans-serif"
BODY="'League Spartan', Arial, sans-serif"
DISP="'Anton', Impact, 'Arial Narrow', sans-serif"

def banner(text, bg=K, fg=Y, size=28, w=None):
    """Parallelogram banner (brand device) as a rotated pill — top edge flat-ish, slight slope."""
    return (f'<div style="display:flex; align-items:center; background:{bg}; padding:10px 28px; '
            f'transform:skewX(-8deg); align-self:start">'
            f'<p style="font-family:{DISP}; font-size:{size}px; color:{fg}; text-transform:uppercase; letter-spacing:1px; transform:skewX(8deg)">{text}</p></div>')

def foot(n, src=""):
    return (f'<div style="position:absolute; left:128px; right:128px; bottom:64px; display:flex; justify-content:space-between; align-items:center">'
            f'<p style="font-size:24px; color:{MUTE}">DiggerLid · BFCM 2026 Sale Plan{(" · " + src) if src else ""}</p>'
            f'<p style="font-size:24px; color:{MUTE}">{n}</p></div>')

def content(id_, title, body, n, src="", notes="", kicker=None):
    kick = banner(kicker, size=26) if kicker else ""
    return (f'<section id="{id_}" data-transition="fade" style="background:{W}; color:{K}; font-family:{BODY}; '
            f'padding:112px 128px 160px; display:flex; flex-direction:column; gap:36px">'
            f'{kick}<h2 style="font-family:{HEAD}; font-size:64px; font-weight:700; line-height:1.05; text-transform:uppercase">{title}</h2>'
            f'{body}{foot(n, src)}{("<aside>"+notes+"</aside>") if notes else ""}</section>')

def section(id_, num, title, sub, n):
    return (f'<section id="{id_}" data-transition="push" style="background:{K}; color:{W}; font-family:{BODY}; '
            f'padding:128px; display:flex; flex-direction:column; justify-content:center; gap:40px">'
            f'<p style="font-family:{DISP}; font-size:44px; color:{Y}; letter-spacing:2px">{num}</p>'
            f'<h1 style="font-family:{HEAD}; font-size:120px; font-weight:700; line-height:1; text-transform:uppercase; color:{W}">{title}</h1>'
            f'<p style="font-size:36px; color:{Y70}; line-height:1.3">{sub}</p>'
            f'<div style="position:absolute; left:128px; right:128px; bottom:64px; display:flex; justify-content:space-between">'
            f'<p style="font-size:24px; color:#9a9697">DiggerLid · BFCM 2026 Sale Plan</p><p style="font-size:24px; color:#9a9697">{n}</p></div></section>')

def card(title, lines, bg="#ffffff", accent=Y, tsize=30, lsize=26, flex="1"):
    lis="".join(f'<li>{l}</li>' for l in lines)
    return (f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:14px; background:{bg}; padding:28px 30px; border:2px solid {K}; border-top:12px solid {accent}">'
            f'<h3 style="font-family:{HEAD}; font-size:{tsize}px; font-weight:700; line-height:1.1; text-transform:uppercase">{title}</h3>'
            f'<ul style="font-size:{lsize}px; line-height:1.35; color:{K90}">{lis}</ul></div>')

def big(num, label, bg=Y40):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:28px 30px; border:2px solid {K}">'
            f'<p style="font-family:{HEAD}; font-size:72px; font-weight:700; line-height:1">{num}</p>'
            f'<p style="font-size:26px; line-height:1.3; color:{K90}">{label}</p></div>')

def table(headers, rows, widths, size=26, hl=None):
    th="".join(f'<th style="width:{w}%; text-align:{"left" if i==0 else "right"}">{h}</th>' for i,(h,w) in enumerate(zip(headers,widths)))
    trs=""
    for ri,r in enumerate(rows):
        bg=f' style="background:{Y40}"' if hl is not None and ri==hl else ""
        trs+=f'<tr{bg}>'+"".join(f'<td style="text-align:{"left" if i==0 else "right"}">{c}</td>' for i,c in enumerate(r))+'</tr>'
    return f'<table style="font-size:{size}px; font-family:{BODY}; border:1px solid {K}"><tr style="background:{K}; color:{W}">{th}</tr>{trs}</table>'

slides={}

# 1 cover
slides["cover"]=(f'<section id="cover" data-transition="push" style="background:{K}; color:{W}; font-family:{BODY}; padding:128px; display:flex; flex-direction:column; justify-content:space-between">'
 f'<div style="display:flex; justify-content:space-between; align-items:center">'
 f'<p style="font-family:{HEAD}; font-size:40px; font-weight:700; letter-spacing:1px; color:{W}">DiggerLid</p>'
 f'<p style="font-size:26px; color:#9a9697">Executive &amp; team briefing · September 2026</p></div>'
 f'<div style="display:flex; flex-direction:column; gap:28px">'
 f'{banner("Black Friday · Cyber Monday", bg=Y, fg=K, size=36)}'
 f'<h1 style="font-family:{HEAD}; font-size:168px; font-weight:700; line-height:0.95; text-transform:uppercase; color:{W}">BFCM 2026<br>Sale Plan</h1>'
 f'<p style="font-size:38px; color:{Y70}; line-height:1.3">What we learned, how we run it, what we sell, and what has to be locked before the hype starts.</p></div>'
 f'<div style="display:flex; justify-content:space-between; align-items:end">'
 f'<p style="font-size:26px; color:#9a9697">Prepared by the Chief of Staff system for Matt, Head of Growth · Data to 22 Sep 2026</p>'
 f'<p style="font-family:{DISP}; font-size:32px; color:{Y}; letter-spacing:1px">KEEP WORKING &amp; KEEP EARNING!</p></div>'
 f'<aside>Open with the four-part structure from the planning notes: research, strategy, offer, lock-up. Everything on the research slides is measured, not assumed; the offer slides are the proposal for discussion.</aside></section>')

# 2 agenda
agenda="".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{bg}; padding:36px 32px; border:2px solid {K}">'
 f'<p style="font-family:{DISP}; font-size:64px; color:{col}; line-height:1">{i}</p>'
 f'<h3 style="font-family:{HEAD}; font-size:40px; font-weight:700; text-transform:uppercase; line-height:1.05">{t}</h3>'
 f'<p style="font-size:26px; line-height:1.35; color:{K90}">{d}</p></div>'
 for i,(t,d,bg,col) in enumerate([
  ("Research questions","What went well and poorly across EOFY 26, BFCM 25 and Father's Day 26, and the five questions for 2026.",Y40,K),
  ("Sale strategy","Eight moves for 2026, the budget guardrails, and the daily revenue curve we are planning to.","#ffffff",K),
  ("Sale offer","Up to 25% off, value bundles, gift-with-purchase tiers and three new hero bundles.",Y40,K),
  ("Sale lock-up","Format and timeline, the pre-game checklist, risks, and the decisions needed this week.","#ffffff",K)],1))
slides["agenda"]=content("agenda","Agenda",f'<div style="display:flex; gap:28px; flex:1">{agenda}</div>',2,notes="Four parts, mirroring the planning notes. Research is where the data lives; the rest is proposal.")

# 3 section research
slides["s-research"]=section("s-research","01","Research questions","What the last three sales measured, and the five questions the team asked for 2026.",3)

# 4 scorecard of last sales
rows=[["Net revenue (14 days)","$535k","$543k","—"],["Orders","1,759","2,107","—"],["Launch 48h share of sale","31%","19%","—"],
      ["Mid-sale plateau (per day)","5.3%","4.9%","—"],["Last 48h share of sale","15%","32%","—"],["Returning-customer revenue share","22%","29%","—"],
      ["Sale landing page conversion","2.09%","3.38%","2.33%"],["Landing page orders","373","382","104"],["Month MER (Meta spend ÷ net)","25.5%","25%","—"]]
slides["scorecard"]=content("scorecard","The last three sales, side by side",
 table(["Measure","BFCM 2025","EOFY 2026","Father's Day 2026"],rows,[40,20,20,20],size=27,hl=6)+
 f'<p style="font-size:26px; color:{K90}; line-height:1.35">Two $540k sales with the same total, the same mid-sale plateau and opposite skews: BFCM front-loads on launch urgency, EOFY back-loads on the 30 June deadline. Father&#39;s Day shown for the landing page only; its sale totals were not part of this research.</p>',
 4,"Shopify analytics, RP-004 / RP-005",notes="Both big sales landed within $10k of each other. The difference is where the urgency sits. FD is a smaller gift-driven sale; only the landing page was measured.")

# 5 went well / poorly
well=card("What went well",["EOFY landing page converted 3.38% and out-delivered BFCM's on 37% fewer sessions","Segmented sends to the engaged base moved returning share to 42-43% (Cyber Monday, EOFY day 9)","Launch and deadline spikes each delivered ~30% of sale revenue","Grease-first page ordering on the EOFY page: 5.7 pages per session","Email and Alia signup data held up: ~30% of signups buy, every cohort"],accent=Y,lsize=25)
poor=card("What went poorly",["BFCM day 2: 4,628 cold-social sessions at 0.99% dragged the page to 2.09%","Pre-launch hype traffic sent to a page with nothing to buy: 4,300 sessions, 25 orders, no capture","Father's Day page went live four days after the sale started","BFCM cart-add tracking was broken (fewer adds than orders)","In-sale popup: seen by 53% of sessions, submitted by 2.3%","Mid-sale offer engagement was hard; promo broke even at best"],accent=K80,lsize=25)
slides["wellpoorly"]=content("wellpoorly","What went well, what went poorly",f'<div style="display:flex; gap:28px; flex:1">{well}{poor}</div>',5,"RP-004, RP-005, RP-006, planning notes",
 notes="Design, landing page, ads, email, budget allocation, sale performance, creative output, tactics: this is the honest split from the research register. The right column is the lock-up list in disguise.")

# 6 five questions
qs=[("Do we ramp spend now?","Not on traffic. The popup reaches 23% of sessions (was 70%). Fix reach, then email capture pays within weeks: ~30% of signups buy in month one."),
    ("Dial up UGC?","Yes, and wider. Launch buyers are 70% new customers; creative that qualifies cold traffic is the constraint, not budget."),
    ("Low repeat or Hybrid?","Low repeat: 17.7% lifetime, 21.4% last 12 months. Ex-grease 14-16%. The sale curve is Hybrid-shaped anyway, because urgency acts on new customers."),
    ("Price rises now, e.g. DiggerShield?","Candidate: 3.5% repeat, $1,063 contribution per acquisition, 622 buyers ever. A pre-hype price test is low risk; decide by mid-October."),
    ("Mid-sale offer: continue?","Continue as a segmented engaged-base send with a real reason (early access, bonus gift), not a full-database blast. Blasts did not move returning share; segments did.")]
qhtml="".join(f'<div style="display:flex; gap:24px; align-items:start; border-bottom:2px solid {K}; padding:0 0 18px 0">'
 f'<p style="font-family:{DISP}; font-size:36px; color:{K}; width:60px">{i}</p>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:6px"><h3 style="font-family:{HEAD}; font-size:32px; font-weight:700; line-height:1.1">{q}</h3>'
 f'<p style="font-size:25px; line-height:1.3; color:{K90}">{a}</p></div></div>' for i,(q,a) in enumerate(qs,1))
slides["questions"]=content("questions","Five questions for 2026, answered by the data",f'<div style="display:flex; flex-direction:column; gap:16px">{qhtml}</div>',6,"RP-003, RP-005, RP-006",
 notes="These are the five questions from the planning notes. Each answer cites a measured number; the price question is the only one that needs a test rather than a read.")

# 7 sale curve
bfcm=[17.9,13.5,7.6,6.4,5.4,5.4,4.1,5.5,5.4,4.3,4.0,5.2,5.6,9.7]; eofy=[12.6,6.8,5.7,4.1,5.2,4.7,4.0,5.4,4.9,4.7,3.7,6.7,11.6,20.0]
def bars(vals,color):
    mx=20.0; out=""
    for i,v in enumerate(vals,1):
        h=int(v/mx*300)
        out+=(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px">'
              f'<p style="font-size:24px; color:{K90}">{v:.0f}%</p>'
              f'<div style="width:44px; height:{max(h,4)}px; background:{color}; border:2px solid {K}"></div>'
              f'<p style="font-size:24px; color:{MUTE}">{i}</p></div>')
    return out
chart=(f'<div style="display:flex; gap:32px; flex:1">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:30px; font-weight:700">BFCM 2025, % of sale revenue by day</h3>'
 f'<div style="display:flex; gap:6px; align-items:end; height:380px; border-bottom:2px solid {K}">{bars(bfcm,Y)}</div></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:30px; font-weight:700">EOFY 2026, % of sale revenue by day</h3>'
 f'<div style="display:flex; gap:6px; align-items:end; height:380px; border-bottom:2px solid {K}">{bars(eofy,K80)}</div></div></div>')
slides["curve"]=content("curve","The curve we are planning to: Hybrid-shaped",chart+
 f'<div style="display:flex; gap:28px">{big("~30%","of sale revenue in the first 48 hours (BFCM). Budget the launch weekend at about $180k on the $605k November plan.")}'
 f'{big("~5%","per day through the middle. That plateau is the upside: daily drops and mid-sale segment sends are plateau-lifters.")}'
 f'{big("70%+","of launch-day buyers are new customers. The launch is an acquisition play; do not starve prospecting to protect retargeting.")}</div>',
 7,"Shopify analytics, RP-004",notes="Ecommerce Equation calls this the Hybrid curve. Ours has the shape but the mechanism is urgency on cold traffic, not the base returning. Plan spend and stock to the front for BFCM.")

# 8 popup reach
reach=[("Jan","67%"),("Feb","70%"),("Mar","64%"),("Apr","80%"),("May","44%"),("Jun","53%"),("Jul","33%"),("Aug","34%"),("Sep","23%")]
rb=""
for m,v in reach:
    h=int(float(v.strip('%'))/80*300); col=Y if float(v.strip('%'))>=50 else K80
    rb+=(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:end; gap:6px">'
         f'<p style="font-size:26px; font-weight:700">{v}</p><div style="width:92px; height:{h}px; background:{col}; border:2px solid {K}"></div><p style="font-size:26px; color:{MUTE}">{m}</p></div>')
slides["reach"]=content("reach","Before any traffic spend: the popup is reaching a quarter of visitors",
 f'<div style="display:flex; gap:32px; flex:1"><div style="flex:3; display:flex; flex-direction:column; gap:10px"><h3 style="font-family:{HEAD}; font-size:30px; font-weight:700">Share of sessions that see the email popup, 2026</h3>'
 f'<div style="display:flex; gap:10px; align-items:end; height:380px; border-bottom:2px solid {K}">{rb}</div></div>'
 f'<div style="flex:2; display:flex; flex-direction:column; gap:20px">{big("~5%","of viewers submit, every month. The popup converts as well as it ever did.",bg="#ffffff")}{big("3x","the signups available on today&#39;s traffic at January&#39;s reach: ~2,800 a month instead of 921.")}{big("$65","contribution per signup in year one. That is the ceiling for what an incremental email is worth.",bg="#ffffff")}</div></div>',
 8,"Alia, Shopify, Klaviyo · RP-006",notes="The first job of the traffic-and-emails push. Audit Alia trigger rules and page targeting on the paid landing pages; target 50% reach on paid traffic by mid-October; check weekly.")

# 9 section strategy
slides["s-strategy"]=section("s-strategy","02","Sale strategy","Eight moves for 2026, each with the number that justifies it, and the guardrails that keep November profitable.",9)

# 10 eight moves
moves=[("1 · Start wider","Targeted experiments on USA, NZ, TikTok and YouTube with a kill rule. More expansive hype: the sale is an acquisition play (70% new at launch)."),
       ("2 · 13-day sale, 2.5-day hype","Front-loaded curve: ~30% in 48h, ~5%/day, Cyber Monday close. Hype traffic goes to a capture page, not a preview."),
       ("3 · Stronger theme","Open with Take Cover (paintball ambush film); run the week on Knock-Off Deals, a new drop at 3:30 PM every day to lift the plateau."),
       ("4 · Cut and run","Stop spend faster: day-2 cold-social floods at 0.99% are the single biggest drag. Daily MER watch, sale ceiling 28%."),
       ("5 · Mid-sale offer","A strong collab or bonus-gift moment mid-sale, sent to the engaged segment (returning share 43% when segmented, flat when blasted)."),
       ("6 · Pre-game check","Landing, bundle and collection pages built and QA'd before the hype sends; cart tracking verified; popup reach ≥50% on paid pages."),
       ("7 · Better reactivation","Email and SMS to the 12,745 first-time buyers from the last year; grease reorder nudges (the one repeat lever, ~27% product repeat)."),
       ("8 · Beat the hangover","A strong post-sale offer and a new product launch into December; the Christmas gift transition on 30 Nov. December signups are the weakest cohort (21.7%).")]
grid="".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{"#ffffff" if i%2 else Y40}; padding:22px 24px; border:2px solid {K}">'
 f'<h3 style="font-family:{HEAD}; font-size:28px; font-weight:700; line-height:1.1; text-transform:uppercase">{t}</h3><p style="font-size:24px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate(moves))
slides["moves"]=content("moves","Eight moves for 2026",f'<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; flex:1">{grid}</div>',10,"Planning notes, research register",
 notes="Straight from the strategy page of the notes, each paired with the evidence. Move 6 is where most of the value sits: it is the fix for last year's avoidable losses.")

# 11 budget & guardrails
slides["budget"]=content("budget","November plan and guardrails",
 f'<div style="display:flex; gap:28px">{big("$605k","November net revenue (ex-GST) in the H2 forecast; BFCM 2025 did $651k net in the month.")}{big("≤28%","MER ceiling for a sale month. BFCM 2025 ran 25.5% ($166k Meta on $651k). At 25% MER, GPAM lands ~24% in November.")}{big("$68.6k","November net profit under MER discipline; $32.3k on the current trajectory. The gap is spend efficiency, not revenue.")}</div>'
 +table(["Rule","What it means in the sale"],[["Front-load, then hold","Launch weekend ≈ $180k; plateau ≈ $30k/day; Cyber Monday close 10-15%."],
   ["Cut and run","Any day where cold-social landing conversion is under 1.5% by midday: pull the broad set, keep retargeting and email."],
   ["Test markets on a leash","USA, NZ, TikTok, YouTube: fixed test budget, pass/fail on MER by day 4, else stop."],
   ["AOV defence","Percentage plus gift, never flat dollars. Bundles do the AOV work; target $315+."],
   ["Reach before spend","Popup reach ≥50% on paid pages by mid-October, or the traffic is buying fewer emails than it should."]],[30,70],size=26),
 11,"data/FORECAST.md, OBJECTIVES.md, RP-001, RP-005",notes="GPAM% = (1 - VCR) - MER; sale-month VCR is 0.503, so 26% GPAM is not reachable in November; 23.7% is the disciplined case. MER is the only lever that moves the profit number.")

# 12 section offer
slides["s-offer"]=section("s-offer","03","Sale offer","Up to 25% off, value bundles and gift-with-purchase tiers, built to defend AOV while the discount does the acquisition work.",12)

# 13 offer architecture
slides["offer"]=content("offer","Offer architecture",
 f'<div style="display:flex; gap:28px; flex:1">'
 f'{card("Sitewide discount",["Up to 25% off everything except grease","DiggerShield: $150 / $200 off instead of a percentage","Percentage plus gift, never a flat-dollar sitewide offer (AOV defence)"],accent=Y,tsize=32,lsize=27)}'
 f'{card("Gift with purchase tiers",["$299 spend: Magnet Tool Mat","$399 spend: free shipping","$599 spend: Drawbar Cover","Tiers sit just above the $305 first-order AOV to pull baskets up"],accent=K,tsize=32,lsize=27)}'
 f'{card("Value bundles",["All existing bundles stay live at sale pricing","Three new hero bundles at 30 / 40 / 50% off (next slide)","Bundles carry the AOV; the sitewide % carries the traffic"],accent=Y,tsize=32,lsize=27)}</div>'
 f'<p style="font-size:26px; color:{K90}; line-height:1.35">Grease is excluded from the sitewide percentage on purpose: it is the one consumable and the only repeat lever, and it converts social traffic at full price. Confirm the DiggerShield dollar-off amounts against margin before lock-up.</p>',
 13,"Planning notes, RP-003, EOFY and FD learnings",notes="From the sale format page of the notes. The GWP thresholds map onto the AOV target; the free-shipping tier at $399 mirrors the existing free-shipping-over-$399 offer that converts signups at 37%.")

# 14 bundles
b1=card("Ultimate Excavator Bundle · 30% off",["1× Pro Excavator Enclosure","1× Drawbar Cover","1× PRO Mat Plus","10× Digger Wipes","1× Keyring","1× Magnet Tool Mat"],accent=Y,tsize=30,lsize=27)
b2=card("Hardcore Tradie Bundle · 40% off",["2× PRO Mat Plus","1× Drawbar Cover","1× Proper Thicc Hoodie","10× Digger Wipes","1× Boom Bottle Opener","1× Magnet Tool Mat"],accent=K,tsize=30,lsize=27)
b3=card("Ludicrous Bundle · 50% off",["1× PRO Mat + 2× PRO Mat Plus","2× Magnet Tool Mat","1× Drawbar Cover","1× Quicky Cover","1× Hoodie + 1× Bottle Opener","20× Digger Wipes"],accent=Y,tsize=30,lsize=27)
slides["bundles"]=content("bundles","Three new hero bundles",f'<div style="display:flex; gap:28px; flex:1">{b1}{b2}{b3}</div>'
 f'<p style="font-size:26px; color:{K90}; line-height:1.35">Bundle names and contents as drafted in the planning notes. Bundle-level margin at 30/40/50% and the DiggerShield dollar-off still need a costing pass; PRO Mat Plus is the anchor in all three because it is the strongest acquisition product (93.5% of its buyers are new to the brand).</p>',
 14,"Planning notes, RP-003",notes="Three tiers of ambition. The 50% bundle is a headline piece as much as a product; check it against COGS before it goes on the page.")

# 15 theme
slides["theme"]=content("theme","Theme: All Aussie Adventure, with a daily knock-off drop",
 f'<div style="display:flex; gap:28px; flex:1">'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{K}; color:{W}; padding:36px; border:2px solid {K}">{banner("Master theme · All Aussie Adventure", bg=Y, fg=K, size=28)}'
 f'<p style="font-size:27px; line-height:1.35; color:{W}">A loving parody of the outback-bumbler format: our own khaki-clad expert tours four locations dispensing machinery wisdom and wrecking everything except the covered gear. Every segment ends in disaster around the machine while the cover shrugs it off.</p>'
 f'<p style="font-size:25px; line-height:1.35; color:{Y70}">Best for long-form social, virality and brand love. Weakest on pure urgency, so every episode ends on a hard offer card, and the sale mechanic does the urgency work.</p></div>'
 f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{Y40}; padding:36px; border:2px solid {K}">{banner("Sale mechanic · Knock-Off Deals", size=28)}'
 f'<p style="font-size:27px; line-height:1.35">A new deal drops at 3:30 PM sharp every day of the sale: genuine gear at knock-off prices. The 3:30 stamp is the daily-drop mark in email, SMS and on the page.</p>'
 f'<p style="font-size:25px; line-height:1.35; color:{K90}">Why: the mid-sale plateau ran ~5% a day in both big sales. Daily drops give the plateau a reason to come back. Alternative launch film if the Adventure edit slips: Take Cover (paintball ambush, shoots already in the can).</p></div></div>',
 15,"Planning notes pp.10-11, concept board",notes="The notes pair the Adventure theme with the four-location shoot. The concept board rated it strongest for brand love and weakest for urgency; the Knock-Off mechanic covers the urgency gap.")

# 15b creative production
locs=[("Paddock","Excavator; focus DiggerShield and the big dog; practical, authentic; Ivan (Earthworks Hub) cameo?","Talk slow for earthmovers","Pro Enclosure · DiggerShield"),
      ("Worksite","Building an A-frame; backyard with the excavator; translating for tradies","How you might have done it: a history lesson","PRO Mat · small covers"),
      ("Red dirt","Dust trail; camping out; doors; night; campfire","Show these city boys how it is done","PRO Mat · small covers"),
      ("Warehouse","Bundles and offer shots; forklift","Straight product proof","Grease · accessories")]
lh="".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{"#ffffff" if i%2 else Y40}; padding:24px 26px; border:2px solid {K}; border-top:12px solid {Y if i%2==0 else K}">'
 f'<h3 style="font-family:{HEAD}; font-size:32px; font-weight:700; text-transform:uppercase">{n}</h3>'
 f'<p style="font-size:24px; line-height:1.3; color:{K90}">{sh}</p>'
 f'<p style="font-family:{DISP}; font-size:24px; letter-spacing:1px; text-transform:uppercase">{ang}</p>'
 f'<p style="font-size:24px; line-height:1.3"><b>Products:</b> {pr}</p></div>' for i,(n,sh,ang,pr) in enumerate(locs))
slides["production"]=content("production","Creative production: four locations, 2.5 shoot days, one safety",
 f'<div style="display:flex; gap:22px; flex:1">{lh}</div>'
 f'<div style="display:flex; gap:28px">{big("4","locations, one character, one arc: each episode is a location, each location owns a product.",bg="#ffffff")}{big("2.5","shoot days plus one safety day. Connected hype assets cut from the same footage: video vibes and image-offer teasers.")}{big("Nov 13","hard deadline for the edit: pages and hype assets must be live before the 14 Nov hype sends (last year the FD page went live four days late).",bg="#ffffff")}</div>',
 16,"Planning notes p.10",notes="Shot list per location from the notes. The Warehouse day doubles as the bundle and offer stills day; do it first so the page build is never waiting on creative.")

# 15c the character
traits=["G'day, I'm [name], and this is my backyard: the Aussie outback","Dumb physical comedy: reverses over the esky, falls off the machine","Overstated knowledge of land and conditions","Criticises city folk and early settlers alike","Tries to help, wrecks it; the covered gear is the only competent thing on screen","Shoddy recreations and bad history lessons"]
slides["character"]=content("character","The character: our own outback expert",
 f'<div style="display:flex; gap:28px; flex:1">'
 f'{card("Character bible (from the notes)",traits,accent=Y,tsize=32,lsize=26)}'
 f'{card("IP guardrails (from the concept board)",["Build our own recurring character, e.g. Gravel Grant: khaki, hat, moustache energy","Parody the format and the archetype only","Never the show&#39;s name, the actor&#39;s name or likeness, specific scenes or logos in paid media","Own catchphrases, own episode titles (Ep 3: The Pilbara Incident)","Legal read on the edit before the first paid placement"],accent=K80,tsize=32,lsize=26)}</div>'
 f'<p style="font-size:26px; color:{K90}; line-height:1.35">How it becomes part of the brand story: the character is a recurring content vehicle beyond the sale (grease how-not-tos, cover fit guides, tutorial content with Ivan from Earthworks Hub), so the BFCM edit is season one, not a one-off.</p>',
 17,"Planning notes p.11, concept board",notes="The notes' character traits are the comedy engine. The guardrails keep the homage safe in paid media.")

# 15d landing page results
lp_rows=[["Landing sessions","17,870","11,304","4,464"],["Session conversion","2.09%","3.38%","2.33%"],["Orders from those sessions","373","382","104"],["Direct share of traffic","16%","28%","—"],["Social conversion on the page","1.37%","2.04%","—"],["Reached checkout","2.8%","4.7%","—"],["Pages per session (PostHog)","—","5.7","5.4"],["Went live","before hype","before hype","4 days after launch"]]
slides["lpresults"]=content("lpresults","Landing pages: EOFY's page converted 62% better",table(["Measure","BFCM 25 /pages/blackfriday","EOFY 26 /pages/eofy-2026","FD 26 /pages/fathers-day-2026"],lp_rows,[34,22,22,22],size=26,hl=1)+
 f'<div style="display:flex; gap:28px">{big("0.99%","conversion on 19 Nov 2025: 4,628 cold-social sessions in one day, a quarter of the page&#39;s traffic.")}{big("3-4x","the homepage out-converts both sale pages, because it gets the warm traffic. Judge the page on source-matched conversion.",bg="#ffffff")}{big("0.6%","conversion of pre-launch hype traffic sent to the sale page: 4,300 sessions, 25 orders, no email capture.")}</div>',
 18,"Shopify analytics, PostHog · RP-005",notes="Answers the design and landing page research questions. The fix list: build before hype, split cold from warm, capture the hype traffic, verify tracking.")

# 15e repeat classification
slides["repeat"]=content("repeat","Are we low repeat or hybrid? Low, on the Hybrid line",
 f'<div style="display:flex; gap:28px">{big("21.4%","of last-12-month customers had bought before (Shopify returning-customer rate). Lifetime: 17.7%. EE bands: Low 0-19, Hybrid 20-39.")}{big("16.4%","the same measure without grease. Grease is the only consumable (~27% product repeat); every durable is under 11%.",bg="#ffffff")}{big("93.5%","of PRO Mat buyers were new to the brand. It is the purest acquisition product in the range, and it repeats at 2-8%.")}</div>'
 +table(["Set","Repeat orders per buyer","What it means for the sale"],[["Grease system","31%","Exclude from the sitewide %; it sells at full price and is the reorder base"],["Whole store","27%",""],["Covers","11%","Multi-machine buyers, not replacements"],["Machine protection (all durables)","10%","One-and-done: first-order economics only"],["PRO Mat","2.6%","Lead with it for acquisition; bundle it for AOV"]],[34,26,40],size=25),
 19,"Shopify analytics · RP-003",notes="Run the sale on first-order economics: AOV, first-order GPAM, day-one payback. There is no retention layer to protect except grease.")

# 15f email plan
slides["emailplan"]=content("emailplan","Emails: capture now, segment by intent, keep capturing in the sale",
 f'<div style="display:flex; gap:28px">{big("29.4%","of popup signups buy (4,998 of 17,011); ~85% of that inside the first month via the welcome flow.")}{big("4-7%","of pre-sale signups who had not bought went on to buy during the sale. Emails pay now; they do not bank for BFCM.",bg="#ffffff")}{big("35%","conversion for grease-intent signups vs 28% for cover-intent. The popup&#39;s interest question is a usable qualifier.")}</div>'
 +f'<div style="display:flex; gap:28px; flex:1">'
 +card("Oct to mid-Nov",["Fix popup reach on paid pages (≥50%), then capture continuously","Welcome flow split by interest: grease offer + reorder cadence vs machine-fit guide","One-month popup holdout to price incrementality","Reactivation to the 12,745 first-time buyers of the last year"],accent=Y,tsize=30,lsize=25)
 +card("Hype and sale",["Hype traffic to a first-access capture page with countdown","Sale-specific popup: early access or bonus gift, not a discount (June: seen by 53%, submitted by 2.3%)","Launch, mid-sale and close sends to the engaged segment; full-database only for launch and last day","3:30 PM knock-off drop as the daily SMS moment"],accent=K80,tsize=30,lsize=25)
 +card("After",["Hangover offer 1-9 Dec and the new product launch","Gift guide 1 Dec; shipping cut-off 2 and 9 Dec","Do not buy list growth in December: weakest cohort, 21.7%","Giveaways are not acquisition: entrants convert 3-4%"],accent=Y,tsize=30,lsize=25)+'</div>',
 20,"RP-001, RP-002, RP-006",notes="Answers the email research question. The value of a signup is ~$120 net revenue, ~$65 contribution in year one; that is the ceiling for any lead campaign.")

# 15g test markets (inferred)
slides["tests"]=content("tests","Start wider, on a leash: the test-market design",
 table(["Test","Budget cap","Runs","Pass rule","Fail rule"],[["USA prospecting","[$__]","Hype + first 4 sale days","MER ≤ 35% and CPA ≤ $120 by day 4","Stop at day 4; keep only retargeting"],["New Zealand prospecting","[$__]","Same","Same","Same"],["TikTok (AU)","[$__]","Hype + first 4 sale days","Landing conversion ≥ 1.5% and MER ≤ 35%","Stop at day 4"],["YouTube (AU)","[$__]","Same","Same","Stop at day 4"]],[26,14,22,20,18],size=25)
 +f'<p style="font-size:26px; color:{K90}; line-height:1.35">Inferred from the notes (start wider, cut and run more aggressively). Budgets are placeholders for the team to set; the pass and fail thresholds follow the sale MER ceiling (28% blended) with headroom for a test cell. International was 18% of sessions last year, led by the US, UK and NZ.</p>',
 21,"Planning notes p.6, Big Fish data sheet",notes="Suggested slide. The point is that every test has a kill rule written down before it starts, so cut-and-run is a decision already made.")

# 15h reactivation & hangover (inferred)
slides["hangover"]=content("hangover","Reactivation and beating the hangover",
 f'<div style="display:flex; gap:28px; flex:1">'
 +card("Reactivation before the sale",["12,745 first-time buyers in the last 12 months; most have never had a reason to return","Grease reorder nudge at ~90 days and a 40-piece upsell: the stickiest variants (14-15% repeat)","Second-machine angle for cover buyers (universal covers repeat 9%: they cover more machines)","Segment sends only; full-database sends did not move returning share"],accent=Y,tsize=30,lsize=25)
 +card("Beating the hangover (Dec)",["July 2026 was the post-EOFY hangover: MER 42%, a loss month. December must not repeat it","Hangover offer that is not a discount: the new product launch, the Christmas gift guide, last knock-off of the year","December signups are the weakest cohort (21.7%): spend on buyers, not list growth","Shipping cut-off messaging 2 and 9 Dec; gift proof content 7 Dec"],accent=K80,tsize=30,lsize=25)+'</div>',
 22,"Planning notes p.6, FORECAST.md, RP-003, RP-006",notes="Suggested slide combining moves 7 and 8 with the numbers behind them.")

# 15i gifting path (inferred from issue 1)
slides["gifting"]=content("gifting","Issue 1: no clear path for gifting",
 f'<div style="display:flex; gap:28px">{big("~34%","of PRO Mat Plus buyers are women, i.e. gift buyers. The gift path exists in the data; the site does not show it.")}{big("0.5%","of visitors to the Father&#39;s Day gift page ordered (999 viewers, 7% went on to a product). A generic gift page is not the answer.",bg="#ffffff")}{big("30 Nov","Christmas gift collection and gift-buyer ad angles go live on Cyber Monday; gift guide email 1 Dec.")}</div>'
 +f'<div style="display:flex; gap:28px; flex:1">'
 +card("What a gift path looks like",["Gift entry on the sale page and in the nav: For the operator in your life","Three gift tiers that match the GWP thresholds: under $150 (grease kit, accessories), $299 (PRO Mat Plus + magnet mat), $599 (bundle)","Machine-fit help for the buyer who does not know the model: a two-question finder","Gift wrap or gift card option at checkout; delivery date promise on the page"],accent=Y,tsize=30,lsize=25)
 +card("What we learned not to do",["A standalone gift landing page with no product depth (FD gift page: 2.3 pages per session)","Sending gift traffic to the sale page (the EOFY page pushed grease first)","Leaving the shipping cut-off implicit: say the date on every gift surface"],accent=K80,tsize=30,lsize=25)+'</div>',
 23,"Concept board context, RP-005 (EXP-005), calendar",notes="Suggested slide answering the first possible issue in the notes. The gift buyer converts; the gift page did not.")

# 15j measurement plan (inferred)
slides["measure"]=content("measure","Measuring the sale: the daily scorecard",
 table(["Row","Target / benchmark","Source","Cadence"],[["Net revenue vs the Hybrid curve","Launch 48h ≈ 30%; plateau ≈ 5%/day; close 10-15%","Shopify","Daily 8am"],["MER","≤ 28% sale month; cut-and-run trigger 30% for 2 days","Meta live spend ÷ net","Daily"],["Sale page conversion by source","≥ 3.4% blended; social ≥ 2%; direct ≥ 6%","Shopify landing page","Daily"],["Popup reach and signups","Reach ≥ 50%; submit ≈ 5% of views","Alia + Shopify","Weekly, daily in sale"],["Returning-customer share","≥ 25% on segmented-send days","Shopify new vs returning","Daily"],["AOV and bundle share","AOV ≥ $315; bundles ≥ [__]% of orders","Shopify","Daily"],["Knock-off drop response","Orders in the 3:30-5:30 PM window vs baseline","Shopify hourly","Daily"]],[30,34,20,16],size=25),
 24,"DAILY-SCORECARD-FORMAT.md, RP-004/005/006",notes="Suggested slide: the scorecard the Chief of Staff runs each morning of the sale, with the thresholds that trigger a decision.")
# 16 section lockup
slides["s-lockup"]=section("s-lockup","04","Sale lock-up","Format and timeline, the pre-game checklist, the risks we already know about, and the decisions needed this week.",16)

# 17 format & timeline
tl=[("Sat 14 – Mon 16 Nov","2.5-day hype","Connected hype assets: video vibes and image-offer teasers. Hype traffic lands on a first-access capture page with a countdown, not the sale page."),
    ("Tue 17 Nov","Pre-game check","Landing, bundle and collection pages live and QA'd; cart tracking verified; popup firing on paid pages; ad sets and sends scheduled."),
    ("Wed 18 Nov","Launch","Take Cover film + launch sends. Expect ~30% of sale revenue in 48h. Cold prospecting to grease and PRO Mat product pages; sale page for warm traffic."),
    ("Thu 19 – Sun 29 Nov","The week","Knock-Off drop at 3:30 PM daily. Engaged-segment send mid-sale with the collab / bonus-gift moment. Daily MER and cut-and-run."),
    ("Mon 30 Nov","Cyber Monday close","Last knock-off of the year. Engaged-segment close send (43% returning share last year). Christmas gift transition goes live the same day."),
    ("1 – 9 Dec","Beat the hangover","Hangover offer and new product launch; gift guide email 1 Dec; shipping cut-off messaging 2 and 9 Dec.")]
tlh="".join(f'<div style="display:flex; gap:24px; align-items:start; border-bottom:2px solid {K}; padding:0 0 14px 0">'
 f'<p style="font-family:{HEAD}; font-size:28px; font-weight:700; width:300px; line-height:1.15">{d}</p>'
 f'<p style="font-family:{DISP}; font-size:26px; width:280px; color:{K}; letter-spacing:1px; text-transform:uppercase; line-height:1.2">{t}</p>'
 f'<p style="flex:1; font-size:24px; line-height:1.3; color:{K90}">{x}</p></div>' for d,t,x in tl)
slides["timeline"]=content("timeline","Format and timeline: 13 days, Cyber Monday close",f'<div style="display:flex; flex-direction:column; gap:12px">{tlh}</div>'
 f'<p style="font-size:24px; color:{K90}; line-height:1.3">Dates proposed to match the notes (13-day sale, 2.5-day hype) and last year&#39;s window. The shared calendar currently shows a 23 Nov start with launch sends on 27 Nov; reconcile before the hype assets are briefed.</p>',
 17,"Planning notes, campaign calendar, RP-004/005",notes="Thirteen days ending on Cyber Monday reproduces last year's shape. If the team prefers the calendar's 23 Nov start, the sale is eight days and the plateau math changes.")

# 18 pre-game checklist + risks
chk=card("Pre-game checklist (owner, due)",["Landing, bundle, collection pages built and QA'd before hype sends · Web · 13 Nov","Cart-add and checkout tracking verified on the sale page · Web · 13 Nov","Popup reach ≥50% on paid landing pages; weekly Alia check · Growth · 15 Oct","Pre-launch capture page with countdown · Web/Email · 13 Nov","Cold prospecting → PDP/collection; sale page for warm · Paid · 16 Nov","Engaged-segment sends built: mid-sale and close · Email · 16 Nov","Bundle and DiggerShield margin pass · Finance · 30 Oct","Hangover offer + new product launch briefed · Growth · 20 Nov"],accent=Y,tsize=30,lsize=24)
risk=card("Known risks and mitigations",["No clear path for gifting: Christmas gift collection and gift-buyer ad angles go live 30 Nov; 34% of PRO Mat Plus buyers are gift buyers","Landing page: built late last time; this time built before hype, source-split traffic, 3.4% benchmark","Hangover: December signups convert worst (21.7%); a real post-sale offer and a launch, not more discount","Overspending: sale MER ceiling 28%, daily watch, cut-and-run rule at 1.5% landing conversion","Popup submit collapses in a sale (2.3% in June): sale-specific popup with early access or bonus gift, not a discount"],accent=K80,tsize=30,lsize=24)
slides["lockup"]=content("lockup","Lock-up: the checklist and the risks",f'<div style="display:flex; gap:28px; flex:1">{chk}{risk}</div>',18,"Planning notes (possible issues), RP-005, RP-006",
 notes="The four possible issues from the notes each have a mitigation from the research. Owners and dates are proposals for the team to confirm.")

# 19 decisions
dec=[("Sale dates","18-30 Nov (13 days, Cyber Monday close) vs the calendar's 23 Nov start."),
     ("Theme","Take Cover launch + Knock-Off Deals week, or the Covers On! alternative."),
     ("Offer","25% sitewide ex-grease, DiggerShield $150/$200, GWP tiers $299/$399/$599, bundles at 30/40/50%."),
     ("Test markets","Fixed budget and kill rule for USA, NZ, TikTok, YouTube."),
     ("Price rise","DiggerShield price test in the pre-hype window, yes or no."),
     ("Reach fix","Who owns the popup trigger and page-targeting audit, due 15 Oct.")]
dh="".join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{"#ffffff" if i%2 else Y40}; padding:24px 26px; border:2px solid {K}">'
 f'<h3 style="font-family:{HEAD}; font-size:30px; font-weight:700; text-transform:uppercase">{t}</h3><p style="font-size:25px; line-height:1.3; color:{K90}">{d}</p></div>' for i,(t,d) in enumerate(dec))
slides["decisions"]=content("decisions","Decisions needed this week",f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:22px; flex:1">{dh}</div>',19,notes="Six decisions unblock the build. Everything else in the deck is execution.")

# 20 close
slides["close"]=(f'<section id="close" data-transition="fade" style="background:{K}; color:{W}; font-family:{BODY}; padding:128px; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:40px">'
 f'{banner("BFCM 2026", bg=Y, fg=K, size=40)}'
 f'<h1 style="font-family:{DISP}; font-size:150px; line-height:1; text-align:center; color:{Y}; letter-spacing:2px">KEEP WORKING &amp;<br>KEEP EARNING!</h1>'
 f'<p style="font-size:30px; color:#9a9697; text-align:center">DiggerLid · Research: RP-003 to RP-006 in the ops hub · Concept board: deliverables/bfcm-2026-concept-board.md</p>'
 f'<aside>Close on the tagline. Next step is the six decisions; the build starts the day they are made.</aside></section>')

order=["cover","agenda","s-research","scorecard","wellpoorly","lpresults","repeat","questions","curve","reach","s-strategy","moves","budget","emailplan","tests","hangover","s-offer","offer","bundles","gifting","theme","production","character","s-lockup","timeline","lockup","measure","decisions","close"]
import re
for n,k in enumerate(order,1):
    h=slides[k]
    h=re.sub(r'(color:#4f4b4c">|color:#9a9697">)(\d{1,2})(</p></div>)', lambda m: m.group(1)+str(n)+m.group(3), h)
    open(os.path.join(SL,f"{k}.html"),"w").write(h)
deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"},
 "title":"DiggerLid BFCM 2026 Campaign Plan","order":order,
 "sections":{"intro":{"description":"Why we are here and the four-part plan","start":"cover"},
             "research":{"description":"What the last three sales measured and the five questions for 2026","start":"s-research"},
             "strategy":{"description":"Eight moves, the November guardrails and the curve we plan to","start":"s-strategy"},
             "offer":{"description":"Discount, gift tiers, bundles and theme","start":"s-offer"},
             "lockup":{"description":"Timeline, checklist, risks and decisions","start":"s-lockup"}},
 "faces":{"roboto-condensed":{"family":"Roboto Condensed","href":"https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap"},
          "league-spartan":{"family":"League Spartan","href":"https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;600;700&display=swap"},
          "anton":{"family":"Anton","href":"https://fonts.googleapis.com/css2?family=Anton&display=swap"}},
 "designSystems":[]}
json.dump(deck,open(os.path.join(ROOT,"project","deck.json"),"w"),indent=1)
print("wrote",len(order),"slides")
