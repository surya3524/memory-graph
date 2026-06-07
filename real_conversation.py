"""
Real Conversation Simulation — PHLX Sell-Off · June 3, 2026
Michael T. (Sector Believer — Semiconductors) · Advisor: David R.

This is a realistic reconstruction of the full day's communication:
  1. Voicemail Michael left at 9:52 AM (he called first)
  2. Advisor's internal prep notes before calling back
  3. Phone call at 10:17 AM (18 turns, 9 minutes)
  4. Follow-up email sent at 11:45 AM
  5. Text exchange at 6:14 PM (after Michael spoke to Susan)
  6. Thursday meeting opening (June 11)
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. VOICEMAIL — Michael called first (9:52 AM)
# ─────────────────────────────────────────────────────────────────────────────
VOICEMAIL = {
    "time": "9:52 AM EST",
    "from": "Michael T.",
    "duration": "0:41",
    "transcript": (
        "Hey David, it's Michael. Uh — I'm sure you're getting slammed today. "
        "Look, I saw the Commerce announcement this morning. I'm not panicking, I'm not selling. "
        "I've been through NVDA down sixty-five percent — this is not that. "
        "But I just... wanted to touch base. Susan saw the account balance this morning "
        "and she texted me three times before nine o'clock, so... "
        "anyway. I'm fine. Call me when you get a chance. "
        "I'm free after ten."
    ),
    "advisor_read": (
        "He called ME first. He says he's fine but he left a 41-second voicemail "
        "and mentioned Susan twice. The 'I'm not panicking' tells me he's at least thinking about it. "
        "He wants reassurance, not a sales call."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. ADVISOR PREP NOTES — Before calling back (internal, 3 minutes)
# ─────────────────────────────────────────────────────────────────────────────
ADVISOR_PREP = {
    "time": "10:14 AM EST",
    "duration": "3 min",
    "notes": [
        "Position: ~$980k in NVDA, AMD, SOXX. At today's prices, down ~$98k on paper.",
        "He's been through NVDA -65% in 2022 and held. This is -11%. He can handle the number.",
        "BUT: Susan is already texting him. That's new. She wasn't in the loop in 2022.",
        "KEY: January 2025 — he said 'if something happens with export controls, semis get hit hard and fast.' "
        "He called this scenario. Use his own words, not mine.",
        "OPEN THREAD: April 2024 — he agreed to 'think about' moving 15% to broader index. "
        "That conversation went nowhere. Today reopens it without me forcing it.",
        "DO NOT: Open with the portfolio number. He knows. Let him bring it up.",
        "DO NOT: Challenge his thesis. He's right that semis are a secular growth story.",
        "TARGET: Get him to commit to a specific date to finish the April conversation. Thursday?",
        "TONE: Peer to peer, not advisor to client. He respects expertise, not hand-holding.",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. PHONE CALL — 10:17 AM EST (9 minutes)
# ─────────────────────────────────────────────────────────────────────────────
PHONE_CALL = [
    {
        "time":    "10:17",
        "speaker": "David (Advisor)",
        "text": (
            "Michael — got your message. Thanks for calling. How are you doing?"
        ),
        "subtext": "Open with a genuine question. Don't lead with markets.",
    },
    {
        "time":    "10:17",
        "speaker": "Michael",
        "text": (
            "I'm good, I'm good. Look, I know what you're going to say. "
            "I've already gotten three texts from Susan and I haven't even left the house yet. "
            "The Commerce thing is real but it's being wildly overplayed by the market. "
            "These guys don't understand how the supply chain actually works."
        ),
        "subtext": "Defensive immediately. Projecting what he thinks David will say. Susan front-of-mind.",
    },
    {
        "time":    "10:18",
        "speaker": "David (Advisor)",
        "text": (
            "You know more about how the supply chain works than anyone I talk to — "
            "so help me understand something. The restriction is on H100-class GPUs and EUV systems "
            "going to UAE, Saudi, Vietnam, Malaysia. "
            "In your read, how much of NVDA's actual data center revenue is exposed there?"
        ),
        "subtext": (
            "Admitting ignorance as a strategy. Forces Michael to explain, "
            "which puts him in expert mode — less defensive. Also genuinely useful information."
        ),
    },
    {
        "time":    "10:19",
        "speaker": "Michael",
        "text": (
            "That's — okay, that's actually a good question. Honestly? "
            "Direct revenue exposure is maybe four, five percent of data center. "
            "The UAE contracts were already getting routed through partners anyway. "
            "What the market is really pricing in is the signal — that this is the beginning "
            "of a broader decoupling. Which is a real risk. I'm not going to pretend it isn't. "
            "But NVDA still sells eighty percent of its chips to US hyperscalers. "
            "That doesn't change today."
        ),
        "subtext": "He just gave a nuanced, credible analysis. And admitted the risk is real. Important moment.",
    },
    {
        "time":    "10:20",
        "speaker": "David (Advisor)",
        "text": (
            "That's helpful. So the market is pricing a tail risk scenario, not the base case. "
            "That tracks with what you told me back in January — you said "
            "'if something happens with the strait or export controls, semis get hit hard and fast.' "
            "You saw this coming. The question is what it means for the position."
        ),
        "subtext": "Anchoring to his own January 2025 words. Not 'I think the risk is real' — 'YOU said the risk is real.'",
    },
    {
        "time":    "10:21",
        "speaker": "Michael",
        "text": (
            "I did say that. Yeah. "
            "Look — I'm down about a hundred grand on paper right now. I've looked at it. "
            "I'm not going to lie and say that doesn't sting a little. "
            "But I've made three hundred thousand on NVDA over the last four years. "
            "If I'd sold every time someone told me the risk was too high, I'd have missed all of it."
        ),
        "subtext": (
            "Significant: he brought up the number himself ($100k). And he's contextualizing it "
            "against gains. He's not irrational — he's doing real math. "
            "He's also slightly defending himself preemptively."
        ),
    },
    {
        "time":    "10:21",
        "speaker": "David (Advisor)",
        "text": (
            "That's absolutely true. And that three hundred thousand is real — "
            "that's not on paper, that's gains you've earned by having conviction "
            "when other people didn't. I'm not here to argue with that track record. "
            "Can I ask you something different?"
        ),
        "subtext": "Validate the wins before pivoting. Never argue with results.",
    },
    {
        "time":    "10:22",
        "speaker": "Michael",
        "text": (
            "Sure."
        ),
        "subtext": "Short answer. He's listening now.",
    },
    {
        "time":    "10:22",
        "speaker": "David (Advisor)",
        "text": (
            "You mentioned Susan texted you three times before nine. "
            "Last April when we talked, you said she'd been bringing up the concentration at dinner. "
            "Is this the kind of day where that conversation gets harder at home?"
        ),
        "subtext": (
            "The spouse question landed here — not as a financial argument "
            "but as a genuine human question about his home life."
        ),
    },
    {
        "time":    "10:23",
        "speaker": "Michael",
        "text": (
            "...Yeah. Yeah, it probably does. "
            "She's not wrong, honestly. She's been saying for two years that we have too much in one sector. "
            "I know she's right. I just — I keep thinking I'll rebalance after the next catalyst. "
            "There's always a reason to wait."
        ),
        "subtext": (
            "Most honest thing he's said. He knows Susan is right. "
            "He's been delaying a decision he's already made internally. "
            "This is the opening."
        ),
    },
    {
        "time":    "10:23",
        "speaker": "David (Advisor)",
        "text": (
            "Michael — that's a really important thing you just said. "
            "'I keep thinking I'll rebalance after the next catalyst.' "
            "Here's what I want to point out: there will always be a next catalyst. "
            "In semis, there's always something happening — earnings, geopolitics, a new architecture. "
            "If we wait for a quiet moment to have this conversation, it never happens."
        ),
        "subtext": "Naming the pattern directly. Not judging it — just naming it.",
    },
    {
        "time":    "10:24",
        "speaker": "Michael",
        "text": (
            "No, you're — that's fair. That's a fair point. "
            "What would you even do? Like what does fifteen percent moved out look like practically?"
        ),
        "subtext": (
            "He asked 'what would you even do' — he's now thinking about mechanics, not whether. "
            "This is a shift. He's moved from defending the position to planning the rebalance."
        ),
    },
    {
        "time":    "10:25",
        "speaker": "David (Advisor)",
        "text": (
            "So you'd go from roughly eighty percent semi exposure to sixty-five. "
            "We'd move about a hundred and forty thousand into a broad-market core — "
            "something like VTI, or a factor tilt if you want. "
            "Your NVDA and AMD positions stay. The thesis stays. "
            "You just have a floor that isn't entirely dependent on one sector's geopolitical weather. "
            "And honestly — Susan gets to see a plan on paper."
        ),
        "subtext": "Concrete numbers. Kept the thesis intact. Included Susan as a stakeholder, not a problem.",
    },
    {
        "time":    "10:26",
        "speaker": "Michael",
        "text": (
            "I don't want to do it today. Not while everything's moving."
        ),
        "subtext": "Reasonable objection. Not resistance — legitimate market timing concern.",
    },
    {
        "time":    "10:26",
        "speaker": "David (Advisor)",
        "text": (
            "Completely agree. I'm not suggesting we touch anything today. "
            "Let the dust settle. But can we book Thursday? "
            "I'll have the specific numbers ready — what the move looks like, "
            "tax implications if any, what the new allocation statement would say. "
            "Forty-five minutes. You bring Susan if she wants to be there."
        ),
        "subtext": "Specific day. Specific agenda. Including Susan is key — it's a household decision.",
    },
    {
        "time":    "10:26",
        "speaker": "Michael",
        "text": (
            "Thursday works. I've got golf in the morning but I'm free after two. "
            "Actually — yeah, bring Susan in. She'll feel better hearing it from you. "
            "She thinks I just dismiss everything you say too."
        ),
        "subtext": (
            "He's joking but it's true. He's also just committed. "
            "And he wants Susan there — this is the household alignment moment."
        ),
    },
    {
        "time":    "10:27",
        "speaker": "David (Advisor)",
        "text": (
            "Ha — I'll try to be more persuasive. I'll send the invite now: "
            "Thursday at two, you and Susan, forty-five minutes. "
            "Michael — for what it's worth, the way you called this scenario in January? "
            "That's why these conversations are worth having. "
            "You understand this sector better than I do. "
            "My job is just to make sure the portfolio structure doesn't work against you."
        ),
        "subtext": "Closing on genuine respect. No condescension. Roles clearly defined.",
    },
    {
        "time":    "10:27",
        "speaker": "Michael",
        "text": (
            "Alright. Thanks David. "
            "And hey — sorry for the early voicemail. "
            "I know you've got a hundred people calling today."
        ),
        "subtext": (
            "Apologizing for calling. Shows he values the advisor's time. "
            "Strong relationship signal — the relationship is working."
        ),
    },
    {
        "time":    "10:27",
        "speaker": "David (Advisor)",
        "text": (
            "You're literally the first call I made. Talk Thursday."
        ),
        "subtext": "True — and he knows it. Small moment. Big relationship signal.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 4. FOLLOW-UP EMAIL — 11:45 AM
# ─────────────────────────────────────────────────────────────────────────────
FOLLOW_UP_EMAIL = {
    "time": "11:45 AM EST",
    "from": "David R. (Advisor)",
    "to":   "Michael T.",
    "subject": "Thursday 2pm — Rebalancing Review",
    "body": """Michael,

Calendar invite sent for Thursday, June 11 at 2:00 PM. 45 minutes.
Susan is welcome — happy to walk through everything together.

I'll prepare:
  • Current allocation breakdown (NVDA / AMD / SOXX / cash)
  • What a 15% rebalance into broad market looks like in dollar terms
  • Tax implications (if any — depends on lot selection)
  • A one-page summary Susan can refer back to

One thought I didn't mention on the call: when you think about what you're building
here — the portfolio, the plan — the concentration question isn't just about volatility.
It's about making sure this works for both of you, not just as an investor thesis
but as a household. You've done the hard work building it. Let's make sure the
structure reflects that.

See you Thursday.

David""",
}

# ─────────────────────────────────────────────────────────────────────────────
# 5. TEXT EXCHANGE — 6:14 PM (after Michael spoke to Susan)
# ─────────────────────────────────────────────────────────────────────────────
TEXT_EXCHANGE = [
    {
        "time":    "6:14 PM",
        "from":    "Michael",
        "text":    "Hey — Susan wants to know if we can do the thursday meeting at your office instead of zoom. She prefers in person for this kind of thing",
    },
    {
        "time":    "6:16 PM",
        "from":    "David (Advisor)",
        "text":    "Absolutely. Office at 2pm Thursday. I'll have everything printed.",
    },
    {
        "time":    "6:17 PM",
        "from":    "Michael",
        "text":    "Good. She's actually looking forward to it I think. First time she's been involved in any of this in a while.",
    },
    {
        "time":    "6:18 PM",
        "from":    "David (Advisor)",
        "text":    "That's a good sign. See you both Thursday.",
    },
    {
        "time":    "6:19 PM",
        "from":    "Michael",
        "text":    "Market closed down what, 3% overall? NVDA closed at 801. I'll take it.",
    },
    {
        "time":    "6:20 PM",
        "from":    "David (Advisor)",
        "text":    "You called the scenario correctly in January. That's worth something.",
    },
    {
        "time":    "6:21 PM",
        "from":    "Michael",
        "text":    "Ha. Good night David.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 6. THURSDAY MEETING — June 11, 2026 (opening)
# ─────────────────────────────────────────────────────────────────────────────
THURSDAY_MEETING = {
    "date":     "June 11, 2026 · 2:04 PM EST",
    "location": "Advisor's office",
    "attendees": ["Michael T.", "Susan T.", "David R. (Advisor)"],
    "opening_exchange": [
        {
            "speaker": "Susan",
            "text": (
                "I told Michael — I've been wanting to have this conversation for two years. "
                "He kept saying 'not yet, the timing isn't right.' "
                "So I'm glad we're finally here."
            ),
        },
        {
            "speaker": "Michael",
            "text": (
                "I know, I know. David, she's been very patient with me."
            ),
        },
        {
            "speaker": "David (Advisor)",
            "text": (
                "Susan — thank you for being here. And I want to say something upfront: "
                "the instinct Michael had to stay concentrated in semiconductors has been right "
                "more than it's been wrong. That's not nothing. "
                "What we're here to talk about today is how to build a structure around that "
                "conviction that works for your whole household — not just Michael's portfolio thesis. "
                "Let me show you what that looks like on paper."
            ),
        },
    ],
    "agenda": [
        "Current allocation: $980k concentrated position breakdown",
        "Proposed move: 15% (~$147k) into VTI broad market core",
        "What changes, what stays the same",
        "Tax lot analysis for the rebalance",
        "New allocation policy statement — both spouses sign",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# WHAT THE MEMORY GRAPH CAPTURES FROM THIS DAY
# ─────────────────────────────────────────────────────────────────────────────
NEW_GRAPH_NODES = [
    {"type": "event",   "label": "phlx_8pct_selloff_jun2026",
     "summary": "PHLX drops 8.1% on US export restriction expansion. Michael's position -$98k intraday."},
    {"type": "emotion", "label": "measured_composure_public_private_contrast",
     "summary": "Said 'I'm fine' publicly but left 41-sec voicemail and mentioned Susan twice. Privately more affected."},
    {"type": "belief",  "label": "direct_revenue_exposure_overstated",
     "summary": "Michael assessed true NVDA exposure to restricted markets at 4-5% of data center revenue."},
    {"type": "belief",  "label": "always_a_reason_to_wait_acknowledged",
     "summary": "Self-identified pattern: delays rebalancing by waiting for next catalyst. First time stated aloud."},
    {"type": "action",  "label": "committed_to_thursday_rebalancing_meeting",
     "summary": "Agreed to June 11 meeting with Susan present. First concrete household alignment step."},
    {"type": "belief",  "label": "susan_acknowledged_as_right_on_concentration",
     "summary": "Michael said 'she's not wrong, honestly' — first time he verbally validated Susan's position."},
]

NEW_GRAPH_EDGES = [
    ("phlx_8pct_selloff_jun2026",               "TRIGGERED_BY", "china_export_controls"),
    ("measured_composure_public_private_contrast","EVOLVED_FROM", "calm_under_major_drawdown"),
    ("always_a_reason_to_wait_acknowledged",     "REFLECTS_ON",  "first_flexibility_on_concentration_2024"),
    ("committed_to_thursday_rebalancing_meeting","INFLUENCED_BY","spouse_discomfort_with_concentration"),
    ("committed_to_thursday_rebalancing_meeting","EVOLVED_FROM", "first_flexibility_on_concentration_2024"),
    ("susan_acknowledged_as_right_on_concentration","LED_TO",    "committed_to_thursday_rebalancing_meeting"),
]
