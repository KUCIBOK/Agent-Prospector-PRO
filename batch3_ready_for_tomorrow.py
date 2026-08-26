#!/usr/bin/env python
"""
📋 BATCH 3 - PRÉPARATION POUR DEMAIN
Les 10 derniers P1 prospects (positions 16-25)
À lancer demain 11:00 AM
"""
from datetime import datetime, timezone
from sqlmodel import create_engine, Session, select
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.prospect import Prospect, Priority

print("\n" + "="*80)
print("📋 BATCH 3 - PRÉPARATION POUR DEMAIN (11:00 AM)")
print("="*80 + "\n")

# Base de données
DATABASE_URL = "sqlite:///prospects.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Récupérer les P1 prospects #16-25 (skip 5 + 10)
print("1️⃣  SÉLECTION BATCH 3 PROSPECTS (#16-25)")
print("-"*80 + "\n")

try:
    with Session(engine) as session:
        statement = select(Prospect).where(
            Prospect.priority == Priority.P1
        ).order_by(Prospect.score.desc()).offset(10).limit(10)

        batch3_prospects = session.exec(statement).all()

        if not batch3_prospects:
            print("❌ Pas assez de P1 prospects!")
            sys.exit(1)

        print(f"✅ {len(batch3_prospects)} prospects sélectionnés:\n")

        batch3_list = []
        for i, prospect in enumerate(batch3_prospects, 16):
            print(f"{i:2d}. {prospect.name:25} | Score: {prospect.score:5.1f} | {prospect.city:15} | {prospect.specialty}")
            batch3_list.append({
                "rank": i,
                "name": prospect.name,
                "email": prospect.email,
                "score": prospect.score,
                "city": prospect.city,
                "specialty": prospect.specialty
            })

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Email template for Batch 3 (different angle - third personalization)
print("\n2️⃣  EMAIL TEMPLATE - BATCH 3 (Final P1 Angle)")
print("-"*80 + "\n")

email_template = """Subject: {prospect_name} — Exclusive African Artist Partnership

Dear {prospect_name},

Quick note: I've been following your gallery's curation in {city}, particularly your interest in {specialty}.

I represent a growing network of emerging African contemporary artists. What makes this different:

📍 Direct artist access (no middlemen)
🎨 Exclusive first pick on new works
🤝 Full partnership flexibility — long-term or project-based
💼 Complete logistics & documentation handled

We've facilitated works for galleries similar to yours. I think there's a genuine fit here.

Are you open to a brief conversation this week? No pressure — just exploring.

Best,
Kucibok Team
kucibok.com"""

print("✅ Template ready for 10 prospects\n")

# Email customization preview
print("3️⃣  PREVIEW - PERSONALIZED EMAILS")
print("-"*80 + "\n")

for prospect in batch3_list[:3]:  # Show first 3 as preview
    prospect_name = prospect["name"].split()[0]
    email_body = email_template.format(
        prospect_name=prospect_name,
        city=prospect["city"],
        specialty=prospect["specialty"].lower()
    )
    print(f"TO: {prospect['email']}")
    print(f"SUBJECT: {prospect_name} — Exclusive African Artist Partnership\n")
    print(email_body)
    print("\n" + "-"*80 + "\n")

print(f"[... + {len(batch3_list) - 3} more prospects with similar personalization]\n")

# Launch instructions
print("="*80)
print("✅ BATCH 3 READY FOR LAUNCH")
print("="*80 + "\n")

print("""
🎯 LAUNCH INSTRUCTIONS (Tomorrow 11:00 AM):

1. Run this command tomorrow at 11:00 AM:
   $ python send_batch3_emails.py

2. Expected results:
   ✅ 10 emails sent
   ✅ Will reach last 10 P1 prospects (all 25 P1 then contacted)
   ✅ Additional 3-4 opens expected (30-40%)
   ✅ Additional 0-1 replies expected

3. Timeline:
   • 11:00 AM: Send Batch 3
   • 12:00 PM: Check for opens
   • 1:00 PM: Continue monitoring Batch 1 & 2
   • 2:00 PM: Check Batch 3 engagement
   • 3:00 PM+: Prepare calls with interested prospects

4. Next phase (Day 4):
   ✅ All 25 P1 prospects contacted
   ✅ Schedule calls with interested parties
   ✅ Prepare discovery meeting agenda
   ✅ Research each prospect for talking points
""")

# Save batch 3 data for tomorrow
print("4️⃣  SAVING BATCH 3 DATA")
print("-"*80 + "\n")

batch3_data = {
    "batch": 3,
    "scheduled_send_time": "2026-08-27 11:00:00",
    "prospects_count": len(batch3_list),
    "prospects": batch3_list,
    "template": email_template,
    "success_criteria": {
        "opens_target": "3-4 (30-40%)",
        "clicks_target": "0-1 (5-8%)",
        "replies_target": "0-1 (0-20%)"
    }
}

try:
    with open("batch3_ready.json", "w", encoding="utf-8") as f:
        json.dump(batch3_data, f, indent=2, ensure_ascii=False)
    print("✅ Batch 3 data saved: batch3_ready.json")
except Exception as e:
    print(f"⚠️  Error: {e}")

# Campaign progression
print("\n" + "="*80)
print("📊 CAMPAIGN PROGRESSION")
print("="*80 + "\n")

print("""
TODAY (Aug 26):
  ✅ Batch 1: 5 emails (60% open rate!) 🔥
  ✅ Batch 2: 10 emails
  ✅ Martine Michel replied (1st deal prospect!)
  📊 Total: 15 emails sent

TOMORROW (Aug 27):
  ✅ Batch 3: 10 emails (scheduled 11:00 AM)
  ✅ Monitor Batch 1, 2, 3 engagement
  ✅ Prepare calls with interested prospects
  📊 Total: 25 P1 emails sent ✅

DAY 3 (Aug 28):
  ✅ All P1 prospects contacted
  ✅ Call scheduling with interested
  ✅ Discovery meetings begin
  ✅ Research for proposals

WEEK 2 (Sep 2-8):
  ✅ P1 calls in progress
  ✅ Proposals being prepared
  ✅ P2 nurture emails launched (51 emails)
  ✅ Build momentum

WEEK 3-4 (Sep 9-30):
  ✅ Proposal submissions
  ✅ Negotiations
  ✅ Deal closing
  ✅ Revenue target: €10,000-45,000 ✅
""")

print("\n" + "="*80)
print("🚀 BATCH 3 READY - LAUNCH TOMORROW 11:00 AM")
print("="*80 + "\n")

print("""
📌 IMPORTANT REMINDERS:

⏰ TIMING:
   • Batch 1 sent: 02:01 (Morning)
   • Batch 2 sent: 02:09 (Morning)
   • Batch 3 send: 11:00 (Morning, Next day)
   → Stagger sends to avoid spam patterns

📧 QUALITY:
   • All 3 batches use different subject lines
   • All 3 batches use different angles/templates
   • All prospects get personalized emails
   • No generic mass mailing (spam-like)

🎯 CONVERSION PATH:
   Email → Open → Click → Reply → Call → Proposal → Deal ✅

💡 KEY SUCCESS FACTORS:
   ✅ Quick responses (< 1h to replies)
   ✅ Professional follow-ups
   ✅ Personal relationship building
   ✅ Clear value proposition
   ✅ Easy call scheduling

📞 CALL STRATEGY:
   • Martine Michel: Tomorrow
   • Any other replies: Within 24h
   • Discovery focus: Problems, budget, timeline
   • Positioning: Partnership, not vendor

✅ YOU'RE ON TRACK:
   60% open rate (beating targets!)
   20% reply rate (excellent!)
   Batch 2 launched successfully
   Batch 3 ready for tomorrow
   30-day goal: 2-3 deals closed ✅
""")

print()
