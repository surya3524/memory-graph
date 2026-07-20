ADVISORS = {
    "ADV001": {
        "advisor_id": "ADV001",
        "name": "Surya T. Meesala",
        "crd": "RJ-7832104",
        "branch": "St. Petersburg, FL",
        "specialty": ["Treasury Wires", "HNW clients", "Retirement Planning"],
        "communication_style": "data-first, concise, leads with key numbers",
        "tone": "direct and professional, avoids filler phrases",
        "client_demographics": "Ages 45-68, $1M-$5M AUM, moderate-aggressive risk",
        "relationship_style": "proactive outreach, weekly for top-tier clients",
        "compliance_scope": "Florida registered, no discretionary authority",
        "sample_communications": [
            "Margaret — quick update on your Q2 allocation. Your equity drift came in at 8.2%, above your 7% threshold. Here is what I recommend and why: rebalancing now locks in gains before Q3 volatility. Let me know if you want to discuss before we act.",
            "David — your RMD deadline is December 31. Based on your current balance of $1.4M and your age 73, the required distribution is $52,632. I have prepared three scenarios for how to handle this tax-efficiently. Call me this week.",
            "Priya — your wire to Fidelity cleared yesterday. Running balance in your RJ account is now $847,000. Your target allocation is still on track. Next review: September 15."
        ]
    },
    "ADV002": {
        "advisor_id": "ADV002",
        "name": "Jennifer Walsh",
        "crd": "RJ-5521089",
        "branch": "Albuquerque, NM",
        "specialty": ["Estate Planning", "Business Owners", "Philanthropic Planning"],
        "communication_style": "relationship-first, story-driven, warm",
        "tone": "conversational, empathetic, client-first language",
        "client_demographics": "Ages 55-75, $2M-$10M AUM, conservative risk",
        "relationship_style": "monthly touchpoints, family-office approach",
        "compliance_scope": "New Mexico registered, fee-only",
        "sample_communications": [
            "Hi Robert, I hope the family is doing well after the move to Santa Fe. I have been thinking about your estate plan given the change in domicile — there are a few things we should revisit before year-end that could make a real difference for the kids. When would be a good time to connect?",
            "Susan, thank you for sharing the news about the business sale. This is a wonderful milestone and I want to make sure we capture every opportunity to protect what you have built. I have sketched out three scenarios for the proceeds — let me walk you through them when you are ready.",
            "Tom, I wanted to reach out personally after the market news this morning. I know volatility can feel unsettling, especially with the legacy you are building. Let us talk through what this means for your plan — your goals have not changed, and neither has our strategy."
        ]
    }
}

CLIENT_GRAPHS = {
    "C001": {
        "client_id": "C001",
        "client_name": "Margaret Collins",
        "account": "RJ-**4821",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Retire at age 65", "value": {"target_age": 65, "current_age": 61, "years_remaining": 4}, "weight": 0.95, "timestamp": "2026-01-15"},
            {"node_id": "n2", "node_type": "risk_profile", "label": "Conservative risk tolerance", "value": {"score": 3, "scale": 10, "label": "Conservative"}, "weight": 0.85, "timestamp": "2026-03-01"},
            {"node_id": "n3", "node_type": "portfolio", "label": "Equity drift +8% above target", "value": {"target_equity": 55, "actual_equity": 63, "drift": 8.0, "aum": 1420000}, "weight": 0.90, "timestamp": "2026-06-17"},
            {"node_id": "n4", "node_type": "behavior", "label": "Accepted 3 prior rebalancings", "value": {"count": 3, "last_date": "2025-09-15", "pattern": "always accepts advisor recommendation"}, "weight": 0.75, "timestamp": "2025-09-15"},
            {"node_id": "n5", "node_type": "life_event", "label": "Spouse retired Jan 2026", "value": {"event": "spouse_retirement", "date": "2026-01-01", "income_impact": -45000}, "weight": 0.70, "timestamp": "2026-01-01"},
            {"node_id": "n6", "node_type": "transaction", "label": "Last wire: $25K to checking", "value": {"amount": 25000, "date": "2026-05-10", "type": "withdrawal", "frequency": "quarterly"}, "weight": 0.50, "timestamp": "2026-05-10"}
        ],
        "edges": [
            {"source": "n3", "target": "n1", "relationship": "THREATENS_GOAL", "strength": 0.88},
            {"source": "n2", "target": "n3", "relationship": "CONFLICTS_WITH", "strength": 0.85},
            {"source": "n4", "target": "n3", "relationship": "SUPPORTS_ACTION_ON", "strength": 0.75},
            {"source": "n5", "target": "n1", "relationship": "ACCELERATES_TIMELINE", "strength": 0.70}
        ]
    },
    "C002": {
        "client_id": "C002",
        "client_name": "David K. Thornton",
        "account": "RJ-**3367",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Fund children's education", "value": {"target": 350000, "current_529": 180000, "gap": 170000}, "weight": 0.90, "timestamp": "2025-11-20"},
            {"node_id": "n2", "node_type": "risk_profile", "label": "Moderate-aggressive risk", "value": {"score": 7, "scale": 10, "label": "Moderate-Aggressive"}, "weight": 0.80, "timestamp": "2026-02-10"},
            {"node_id": "n3", "node_type": "portfolio", "label": "Portfolio on target", "value": {"target_equity": 70, "actual_equity": 68, "drift": -2.0, "aum": 2100000}, "weight": 0.60, "timestamp": "2026-06-17"},
            {"node_id": "n4", "node_type": "life_event", "label": "Eldest child starting college 2027", "value": {"event": "college_start", "date": "2027-09-01", "annual_cost": 65000}, "weight": 0.92, "timestamp": "2025-09-01"},
            {"node_id": "n5", "node_type": "behavior", "label": "Prefers email, responds same day", "value": {"preferred_channel": "email", "response_time": "same day", "meeting_frequency": "quarterly"}, "weight": 0.65, "timestamp": "2026-01-01"}
        ],
        "edges": [
            {"source": "n4", "target": "n1", "relationship": "TRIGGERS_ACTION_ON", "strength": 0.92},
            {"source": "n2", "target": "n3", "relationship": "CONSISTENT_WITH", "strength": 0.80},
            {"source": "n3", "target": "n1", "relationship": "SUPPORTS_GOAL", "strength": 0.70}
        ]
    },
    "C003": {
        "client_id": "C003",
        "client_name": "Priya S. Nair",
        "account": "RJ-**9914",
        "nodes": [
            {"node_id": "n1", "node_type": "goal", "label": "Wire $500K to India property", "value": {"amount": 500000, "destination": "India", "timeline": "Q3 2026"}, "weight": 0.95, "timestamp": "2026-06-01"},
            {"node_id": "n2", "node_type": "behavior", "label": "Typical wires: $25K domestic", "value": {"avg_wire": 25000, "max_wire": 80000, "typical_destination": "domestic", "frequency": "quarterly"}, "weight": 0.88, "timestamp": "2026-05-01"},
            {"node_id": "n3", "node_type": "risk_profile", "label": "Moderate risk tolerance", "value": {"score": 5, "scale": 10, "label": "Moderate"}, "weight": 0.75, "timestamp": "2026-01-15"},
            {"node_id": "n4", "node_type": "portfolio", "label": "AUM $1.8M, liquid $620K", "value": {"aum": 1800000, "liquid": 620000, "target_equity": 60, "actual_equity": 59}, "weight": 0.80, "timestamp": "2026-06-17"},
            {"node_id": "n5", "node_type": "life_event", "label": "International property purchase", "value": {"event": "property_purchase", "country": "India", "amount": 500000}, "weight": 0.90, "timestamp": "2026-06-01"}
        ],
        "edges": [
            {"source": "n1", "target": "n2", "relationship": "ANOMALOUS_VERSUS", "strength": 0.95},
            {"source": "n5", "target": "n1", "relationship": "EXPLAINS", "strength": 0.85},
            {"source": "n4", "target": "n1", "relationship": "FUNDS", "strength": 0.80}
        ]
    }
}
