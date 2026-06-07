"""
PHLX Semiconductor Index — 8.1% Single-Session Sell-Off
Date: June 3, 2026

Simulation of the full advisor workflow:
  market event → system alert → pre-call brief → live conversation → new graph nodes
"""

MARKET_EVENT = {
    "date":        "June 3, 2026",
    "time":        "09:31 AM EST",
    "index":       "PHLX Semiconductor Index (SOX)",
    "move":        "-8.1%",
    "catalyst":    (
        "US Commerce Department expands advanced chip export restrictions "
        "to 12 additional countries, including UAE, Saudi Arabia, Vietnam, "
        "and Malaysia. A100/H100-class GPUs and EUV lithography equipment included. "
        "Effective immediately."
    ),
    "movers": [
        ("NVDA",  "-11.2%", "$892 → $792"),
        ("AMD",   "-9.8%",  "$178 → $160"),
        ("AMAT",  "-7.4%",  "$212 → $196"),
        ("SOXX",  "-8.1%",  "ETF proxy for full sector"),
        ("INTC",  "-5.1%",  "$32 → $30"),
    ],
}

SYSTEM_ALERT = {
    "fired_at":    "09:34 AM EST",
    "client":      "Michael T.",
    "age":         55,
    "archetype":   "Sector Believer — Semiconductors",
    "priority":    3,
    "action":      "CALL THIS WEEK",
    "trigger_matched": "phlx_drop_8pct",
    "context": (
        "Michael holds ~$980k concentrated in NVDA, AMD, and SOXX. "
        "At today's prices that position is down approximately $98,000 in a single session. "
        "He acknowledged Taiwan/export tail risk explicitly in January 2025 — "
        "this is the exact scenario he described. "
        "His wife has raised concentration concerns twice. This event will likely resurface at home."
    ),
    "suggested_approach": (
        "Do not open with the market data — he already knows. "
        "Reference his own January 2025 words about export restriction risk. "
        "Frame rebalancing around the household decision, not the market move. "
        "The spouse concern is the real lever. "
        "Target outcome: schedule the rebalancing review he agreed to consider in April 2024."
    ),
}

PRE_CALL_BRIEF = {
    "prep_time": "2 min 14 sec",
    "graph_nodes_reviewed": 8,
    "key_beliefs": [
        ("deep_domain_conviction_semis",        "Core identity belief — 30 yrs in the industry. Do not challenge directly."),
        ("cycle_reasoning_under_stress",         "He has used this before (NVDA -65% in 2022). Stayed calm. Held."),
        ("geopolitical_risk_acknowledged_2025",  "HIS OWN WORDS: 'if something happens in the strait, semis get hit hard and fast.'"),
        ("first_flexibility_on_concentration_2024", "First time he signalled openness to rebalancing. Anchor to this."),
    ],
    "key_emotions": [
        ("calm_under_major_drawdown", "Remained composed through NVDA -65% in 2022. Expect similar today."),
    ],
    "household_flag": (
        "Wife (Susan) raised concentration concern twice — Nov 2022 and Apr 2024. "
        "April 2024: Michael agreed to 'think about' moving 15% to broader index. "
        "That conversation was never completed."
    ),
    "open_thread": "The 15% rebalancing discussion from April 2024 is unresolved. Today reopens it naturally.",
}

CONVERSATION = [
    {
        "time":    "10:17 AM",
        "speaker": "Advisor",
        "text": (
            "Hey Michael — got a minute? Wanted to check in, not because I'm worried, "
            "but because today's the kind of day where I like to be ahead of things rather than behind them."
        ),
        "graph_note": None,
    },
    {
        "time":    "10:17 AM",
        "speaker": "Michael",
        "text": (
            "Yeah, I saw it. Commerce Department expanding the export list. "
            "Honestly, I think this is being overplayed. These restrictions get walked back within "
            "six months — happened in 2023, happened in 2024. The street is reacting emotionally."
        ),
        "graph_note": "New belief emerging: 'export_controls_viewed_as_temporary' — consistent with cycle_reasoning_under_stress",
    },
    {
        "time":    "10:18 AM",
        "speaker": "Advisor",
        "text": (
            "You may well be right — and honestly, your read on how these things play out "
            "is better than mine. But I want to pull up something you said to me back in January last year. "
            "You told me: 'if something happens in the strait or with export controls, "
            "semis get hit hard and fast.' That's exactly what happened today. "
            "I wrote it down because it was a sharp call."
        ),
        "graph_note": "Advisor using geopolitical_risk_acknowledged_2025 node — Michael's own words, not advisor's opinion",
    },
    {
        "time":    "10:18 AM",
        "speaker": "Michael",
        "text": (
            "Hah. Yeah, I did say that. Look — I still believe in the long-term thesis. "
            "AI infrastructure isn't going away. NVDA is still the picks-and-shovels play. "
            "I'm not selling."
        ),
        "graph_note": "deep_domain_conviction_semis holding firm — expected",
    },
    {
        "time":    "10:19 AM",
        "speaker": "Advisor",
        "text": (
            "I'm not suggesting you sell. Your conviction on the sector has been right more "
            "than it's been wrong, and I respect that. What I do want to revisit is the "
            "conversation we started in April last year — the one about whether the *sizing* "
            "matches the *conviction*. You mentioned then that you'd been talking to Susan about it."
        ),
        "graph_note": "Advisor pivoting to first_flexibility_on_concentration_2024 + spouse_discomfort node",
    },
    {
        "time":    "10:20 AM",
        "speaker": "Michael",
        "text": (
            "Yeah... she's not going to love today's number. She checks the account balance "
            "more than I do now. I know what she's going to say tonight."
        ),
        "graph_note": "New emotion: 'household_tension_anticipated' — spouse concern becoming actionable",
    },
    {
        "time":    "10:20 AM",
        "speaker": "Advisor",
        "text": (
            "Then let's get ahead of that conversation too. Here's what I'd propose — "
            "not as a reaction to today, but as finishing something we already started: "
            "let's look at moving 15% of the semi position into a broader diversified core. "
            "You said you were open to thinking about it in April. "
            "Your thesis on semis doesn't change. Your position stays substantial. "
            "But Susan has a floor she can see, and you're not making a bet-the-farm call "
            "on a single sector anymore."
        ),
        "graph_note": "Reframing: rebalancing = completing an existing decision, not reacting to today",
    },
    {
        "time":    "10:22 AM",
        "speaker": "Michael",
        "text": (
            "That's... actually a fair point. I don't want to do anything today while "
            "everything's moving. But yeah — let's schedule something. "
            "Maybe next week when the dust settles."
        ),
        "graph_note": "New action node: 'agreed_to_schedule_rebalancing_review' — significant. First concrete commitment.",
    },
    {
        "time":    "10:22 AM",
        "speaker": "Advisor",
        "text": (
            "Perfect. I'll send a calendar invite for Thursday. We'll look at the numbers "
            "together — no rush, no pressure. And Michael — you called this scenario correctly "
            "in January. That's worth noting. The question was never whether you understand "
            "the industry. It's just about making sure the structure of the portfolio works "
            "for the whole household."
        ),
        "graph_note": "Closing on a strength affirmation — preserves the advisor relationship dynamic",
    },
    {
        "time":    "10:23 AM",
        "speaker": "Michael",
        "text": (
            "Yeah. Alright. Thanks for calling. "
            "Most advisors would have just sent an email."
        ),
        "graph_note": "Relationship signal: personal call valued over email — reinforce this pattern",
    },
]

CALL_OUTCOME = {
    "duration":        "6 minutes",
    "result":          "SUCCESS",
    "action_taken":    "No immediate trade. Rebalancing review scheduled for June 11, 2026.",
    "new_nodes": [
        {"type": "event",   "label": "phlx_8pct_selloff_jun2026",               "date": "2026-06-03"},
        {"type": "emotion", "label": "measured_composure_under_drawdown",        "date": "2026-06-03"},
        {"type": "belief",  "label": "export_controls_viewed_as_temporary",      "date": "2026-06-03"},
        {"type": "belief",  "label": "household_tension_anticipated",            "date": "2026-06-03"},
        {"type": "action",  "label": "agreed_to_rebalancing_review_jun11",       "date": "2026-06-03"},
    ],
    "new_edges": [
        ("measured_composure_under_drawdown",  "SHAPED_BY",      "cycle_reasoning_under_stress"),
        ("export_controls_viewed_as_temporary","TENSION_WITH",   "geopolitical_risk_acknowledged_2025"),
        ("agreed_to_rebalancing_review_jun11", "INFLUENCED_BY",  "spouse_discomfort_with_concentration"),
        ("agreed_to_rebalancing_review_jun11", "EVOLVED_FROM",   "first_flexibility_on_concentration_2024"),
        ("phlx_8pct_selloff_jun2026",          "TRIGGERED_BY",   "china_export_controls"),
    ],
    "rsi_signal": (
        "Alert fired for correct client. Suggested approach used (spouse angle). "
        "Outcome: scheduled rebalancing review. "
        "RSI weight update: phlx_drop_8pct → michael_t alert = CONFIRMED EFFECTIVE. "
        "Edge weight for spouse_discomfort_with_concentration → rebalancing_action: +0.15"
    ),
}
