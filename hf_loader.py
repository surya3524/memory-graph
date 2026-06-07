"""
HuggingFace Data Loader — Conv-FinRe + Financial Advisor Datasets

In production (internet access): loads live from HuggingFace.
In demo/offline mode: uses bundled sample rows that mirror Conv-FinRe structure.

Conv-FinRe: TheFinAI/conv-finre
  — Conversational, longitudinal benchmark for financial recommendation
  — Has onboarding interview (client profile), multi-turn advisory dialogues,
    risk preference profiling, and longitudinal investment tracking.
"""

# ─────────────────────────────────────────────────────────────────────────────
# BUNDLED SAMPLE DATA — mirrors Conv-FinRe / hub24 schema
# These are representative rows from the dataset structure.
# Pre-encoded nodes included so demo works without API key.
# ─────────────────────────────────────────────────────────────────────────────

HF_SAMPLE_CLIENTS = [
    {
        "source":       "Conv-FinRe · TheFinAI/conv-finre",
        "user_id":      "CFR_0041",
        "risk_profile": "Conservative",
        "age_bracket":  "55–65",
        "onboarding": {
            "background": (
                "Retired schoolteacher. Husband passed away two years ago. "
                "Sole manager of household finances for the first time. "
                "Primary concern: not running out of money. Secondary concern: leaving something for two adult children."
            ),
            "stated_risk_tolerance": "I cannot afford to lose what I have.",
            "investment_horizon":    "10–15 years",
            "prior_experience":     "Savings accounts and one mutual fund through husband's employer plan.",
        },
        "conversations": [
            {
                "turn": 1,
                "role": "advisor",
                "text": "What keeps you up at night when you think about your finances?",
            },
            {
                "turn": 2,
                "role": "client",
                "text": (
                    "Honestly? I look at the news and I see the market going up and down "
                    "and I just... I don't understand it. My husband handled all of this. "
                    "I have $340,000 in a savings account right now because I didn't know what else to do with it. "
                    "I know that's probably wrong but it feels safe."
                ),
            },
            {
                "turn": 3,
                "role": "advisor",
                "text": "That's not wrong — it's a very understandable response to uncertainty. What would 'safe' feel like for you?",
            },
            {
                "turn": 4,
                "role": "client",
                "text": (
                    "Knowing the number won't go below a certain point. Like if I could see a floor. "
                    "My mother lived to 94. I'm 61. That's a long time to make money last."
                ),
            },
        ],
        "encoded_nodes": [
            {"type": "emotion", "label": "grief_driven_financial_paralysis",
             "summary": "Client overwhelmed after husband's passing; holding $340k in cash as emotional safety response."},
            {"type": "belief",  "label": "needs_visible_floor_not_returns",
             "summary": "Client defines safety as a guaranteed minimum, not growth. Longevity awareness (mother lived to 94) is active."},
            {"type": "belief",  "label": "husband_was_financial_decision_maker",
             "summary": "Client has no prior investment experience; husband managed all finances. First-time solo decision-maker."},
            {"type": "action",  "label": "parked_340k_in_savings_account",
             "summary": "Entire liquid wealth in savings account — emotional safety response, not financial strategy."},
        ],
        "encoded_edges": [
            ("grief_driven_financial_paralysis",  "LED_TO",      "parked_340k_in_savings_account"),
            ("needs_visible_floor_not_returns",   "REFLECTS_ON", "husband_was_financial_decision_maker"),
            ("parked_340k_in_savings_account",    "DRIVEN_BY",   "grief_driven_financial_paralysis"),
        ],
        "advisor_alert": {
            "action":   "GENTLE CHECK-IN",
            "trigger":  "Any market volatility — even positive — may feel threatening",
            "context":  (
                "Client is a first-time solo financial decision-maker following spouse's death. "
                "$340k sitting in cash. Longevity risk is real (mother 94, client 61). "
                "She needs a visible floor — a bucket strategy or floor/upside structure will resonate more than portfolio theory."
            ),
            "suggested_approach": (
                "Never use market performance language. Use 'floor' and 'protected income' framing. "
                "Show her a specific number she will never go below. "
                "Reference her mother's longevity as a planning horizon, not a fear factor."
            ),
        },
    },

    {
        "source":       "Conv-FinRe · TheFinAI/conv-finre",
        "user_id":      "CFR_0117",
        "risk_profile": "Aggressive",
        "age_bracket":  "30–40",
        "onboarding": {
            "background": (
                "Software engineer at a mid-size tech company. "
                "Has $280k in 401k (company match, mostly index funds) and $95k in a personal brokerage "
                "he manages himself. Follows r/investing and listens to two finance podcasts weekly."
            ),
            "stated_risk_tolerance": "I'm young. I can take risk. I want to beat the market.",
            "investment_horizon":    "25–30 years",
            "prior_experience":     "Self-directed for 6 years. Beat S&P in 2020 and 2021, lost 38% in 2022.",
        },
        "conversations": [
            {
                "turn": 1,
                "role": "advisor",
                "text": "Tell me about 2022 — what happened and how did you handle it?",
            },
            {
                "turn": 2,
                "role": "client",
                "text": (
                    "I was heavy in ARK and some individual tech names. COIN, HOOD, SKLZ. "
                    "I held through the whole thing because I believed in the thesis. "
                    "Lost about $52,000 on paper. Most of it came back except SKLZ — that's basically zero. "
                    "If I'm honest, I held because I didn't want to admit I was wrong. "
                    "But I also think if I'd sold I would have missed the 2023 recovery."
                ),
            },
            {
                "turn": 3,
                "role": "advisor",
                "text": "Do you think conviction and stubbornness felt the same from the inside in that moment?",
            },
            {
                "turn": 4,
                "role": "client",
                "text": (
                    "...Yeah. Probably. I told my girlfriend it was a long-term position. "
                    "I'm not sure I fully believed that at the time."
                ),
            },
        ],
        "encoded_nodes": [
            {"type": "belief",  "label": "can_beat_market_through_research",
             "summary": "Client believes informed retail investor can outperform index — validated by 2020/2021 wins."},
            {"type": "emotion", "label": "loss_aversion_masked_as_conviction",
             "summary": "Held ARK/speculative names through -38% year; self-identifies holding as 'conviction' but acknowledges it may have been stubbornness."},
            {"type": "action",  "label": "held_ark_tech_through_2022_drawdown",
             "summary": "Did not sell during 38% loss year. SKLZ position went to near-zero. Most other positions recovered in 2023."},
            {"type": "belief",  "label": "first_moment_of_self_doubt_on_process",
             "summary": "First time client acknowledged the line between conviction and denial may be blurry. Significant opening."},
        ],
        "encoded_edges": [
            ("loss_aversion_masked_as_conviction", "LED_TO",      "held_ark_tech_through_2022_drawdown"),
            ("first_moment_of_self_doubt_on_process","EVOLVES_FROM","can_beat_market_through_research"),
            ("held_ark_tech_through_2022_drawdown", "REFLECTS_ON","loss_aversion_masked_as_conviction"),
        ],
        "advisor_alert": {
            "action":   "MONITOR",
            "trigger":  "Portfolio underperforms S&P by >5% in a quarter",
            "context":  (
                "Client is a confident self-directed investor who has had both big wins and a painful loss. "
                "He showed a rare moment of self-reflection about holding = denial. "
                "That opening is valuable — do not push it, but remember it."
            ),
            "suggested_approach": (
                "Don't try to convert him from self-directed to fully managed. "
                "Position yourself as a sounding board and risk framework, not a replacement for his judgment. "
                "When he brings a new position idea, ask: 'Is this conviction or is this SKLZ?' "
                "That question will land because he coined the distinction himself."
            ),
        },
    },

    {
        "source":       "hub24 · jsonfin17/hub24-financial-conversation-sample1",
        "user_id":      "HUB_2893",
        "risk_profile": "Moderate",
        "age_bracket":  "45–55",
        "onboarding": {
            "background": (
                "Small business owner. Dental practice with 4 employees. "
                "Business is the primary asset. No succession plan. "
                "Wife works part-time, two kids in high school. College in 3–5 years."
            ),
            "stated_risk_tolerance": "Moderate. I can't afford a big loss but I need growth.",
            "investment_horizon":    "15–20 years personal, 5–7 years for college funding",
            "prior_experience":     "SEP-IRA through accountant. Hasn't reviewed it in 3 years.",
        },
        "conversations": [
            {
                "turn": 1,
                "role": "advisor",
                "text": "If I asked you what your net worth is today, what would you say?",
            },
            {
                "turn": 2,
                "role": "client",
                "text": (
                    "Honestly I don't know exactly. The practice is probably worth $800k to $1.2M "
                    "if I sold it, but I've never gotten a formal valuation. "
                    "The SEP has maybe $380k. House equity is around $300k. "
                    "But the practice IS my retirement. I don't have anything else really."
                ),
            },
            {
                "turn": 3,
                "role": "advisor",
                "text": "What happens to your retirement plan if you can't practice for 12 months?",
            },
            {
                "turn": 4,
                "role": "client",
                "text": (
                    "I... haven't thought about that. I have disability insurance through the ADA. "
                    "But if the practice had to close... that's a different question. "
                    "I need to think about that."
                ),
            },
        ],
        "encoded_nodes": [
            {"type": "belief",  "label": "practice_is_retirement_plan",
             "summary": "Client's primary retirement asset is his dental practice — illiquid, unsold, no succession plan."},
            {"type": "belief",  "label": "net_worth_not_precisely_known",
             "summary": "Client has never formally valued his practice. Estimates range $800k–$1.2M."},
            {"type": "emotion", "label": "first_awareness_of_concentration_risk",
             "summary": "Client had not considered practice closure scenario until asked. Showed visible pause. Said 'I need to think about that.'"},
            {"type": "action",  "label": "sep_ira_unreviewed_three_years",
             "summary": "SEP-IRA ($380k) not reviewed in 3 years. Set by accountant, not advisor. May be misallocated."},
        ],
        "encoded_edges": [
            ("practice_is_retirement_plan",       "LED_TO",      "sep_ira_unreviewed_three_years"),
            ("first_awareness_of_concentration_risk","REFLECTS_ON","practice_is_retirement_plan"),
            ("net_worth_not_precisely_known",     "TENSION_WITH","practice_is_retirement_plan"),
        ],
        "advisor_alert": {
            "action":   "PROACTIVE EMAIL",
            "trigger":  "Any news about dental industry headwinds / DSO consolidation / disability events",
            "context":  (
                "Client's entire retirement is a single illiquid asset with no succession plan. "
                "The disability question landed — he'd never considered it. "
                "College funding window opens in 3 years."
            ),
            "suggested_approach": (
                "Lead with the practice valuation conversation — get a formal number. "
                "Introduce succession planning as an asset protection conversation, not an exit conversation. "
                "On the disability question: plant the seed now, don't push. He said 'I need to think about that' — follow up in 60 days."
            ),
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# RAW SAMPLE ROWS — exact schema from the HuggingFace dataset viewer
# Columns: id, user_id, step, date, messages, labels, meta, prompt
# These mirror what you actually see at huggingface.co/datasets/TheFinAI/conv-finre
# ─────────────────────────────────────────────────────────────────────────────

HF_RAW_ROWS = [
    {
        "id":      "User_4_step_9",
        "user_id": "User_4",
        "step":    9,
        "date":    "2025-08-27",
        "messages": [
            {
                "role":    "advisor",
                "content": (
                    "Thanks for making the time today. I'm going to ask you to look at "
                    "a set of stocks and tell me which ones feel right for your portfolio "
                    "given where we are in the market right now."
                ),
            },
            {
                "role":    "client",
                "content": (
                    "Sure. I've been watching energy lately. XOM has been holding up well "
                    "and I like the dividend. TSLA feels volatile but there's upside. "
                    "I'm less sure about the consumer staples right now."
                ),
            },
            {
                "role":    "advisor",
                "content": (
                    "Given your profile and what you've just said, how would you rank "
                    "TSLA, XOM, MMM, AMZN, and JPM for the next two weeks?"
                ),
            },
            {
                "role":    "client",
                "content": "XOM first, then TSLA, then JPM. I'd leave MMM and AMZN for now.",
            },
        ],
        "labels": {
            "momentum_rank":      ["TSLA", "XOM", "MMM", "JPM", "AMZN"],
            "utility_rank":       ["XOM", "JPM", "MMM", "AMZN", "TSLA"],
            "user_choice_rank":   ["XOM", "TSLA", "JPM", "AMZN", "MMM"],
        },
        "meta": {
            "candidate_tickers":  ["AMZN", "JPM", "LIN", "MMM", "TSLA", "XOM", "SPG", "PG", "VZ", "MRK"],
            "user_risk_profile":  "Moderate",
            "horizon_days":       14,
        },
        "prompt": (
            "[ADVISOR] Thanks for making the time today. I'm going to ask you to look at "
            "a set of stocks and tell me which ones feel right for your portfolio. "
            "Candidate stocks: AMZN, JPM, LIN, MMM, TSLA, XOM, SPG, PG, VZ, MRK. "
            "[CLIENT PROFILE] Moderate risk. 45–55. Self-directed with advisor oversight. "
            "Prefers dividend payers. Concerned about rate sensitivity."
        ),
    },
    {
        "id":      "User_4_step_10",
        "user_id": "User_4",
        "step":    10,
        "date":    "2025-08-28",
        "messages": [
            {
                "role":    "advisor",
                "content": (
                    "Thanks for making the time today. Yesterday XOM pulled back slightly "
                    "after the EIA inventory report. TSLA bounced on delivery rumours. "
                    "How are you thinking about the same set today?"
                ),
            },
            {
                "role":    "client",
                "content": (
                    "Still like XOM long term. TSLA bounce feels speculative to me — "
                    "I'm not chasing it. JPM earnings are next week so I'd move that up."
                ),
            },
            {
                "role":    "advisor",
                "content": "Given that, how would you rank the candidates today?",
            },
            {
                "role":    "client",
                "content": "XOM, JPM, then TSLA. Same bottom two.",
            },
        ],
        "labels": {
            "momentum_rank":      ["TSLA", "XOM", "JPM", "AMZN", "MMM"],
            "utility_rank":       ["XOM", "JPM", "MMM", "AMZN", "TSLA"],
            "user_choice_rank":   ["XOM", "JPM", "TSLA", "AMZN", "MMM"],
        },
        "meta": {
            "candidate_tickers":  ["AMZN", "JPM", "LIN", "MMM", "TSLA", "XOM", "SPG", "PG", "VZ", "MRK"],
            "user_risk_profile":  "Moderate",
            "horizon_days":       14,
        },
        "prompt": (
            "[ADVISOR] Thanks for making the time today. Yesterday XOM pulled back slightly. "
            "TSLA bounced on delivery rumours. "
            "Candidate stocks: AMZN, JPM, LIN, MMM, TSLA, XOM, SPG, PG, VZ, MRK. "
            "[CLIENT PROFILE] Moderate risk. 45–55. Dividend focus. Rate sensitive."
        ),
    },
    {
        "id":      "User_4_step_11",
        "user_id": "User_4",
        "step":    11,
        "date":    "2025-08-29",
        "messages": [
            {
                "role":    "advisor",
                "content": (
                    "Thanks for making the time today. AMZN is up 3% pre-market on AWS figures. "
                    "XOM flat. JPM upgraded by two analysts this morning."
                ),
            },
            {
                "role":    "client",
                "content": (
                    "Okay that changes things a bit. JPM upgrade is meaningful. "
                    "I'd move it to number one today. AMZN — I don't trust cloud multiples right now. "
                    "I'll keep XOM second."
                ),
            },
            {
                "role":    "advisor",
                "content": "Full ranking for today?",
            },
            {
                "role":    "client",
                "content": "JPM, XOM, TSLA, MMM, AMZN.",
            },
        ],
        "labels": {
            "momentum_rank":      ["TSLA", "XOM", "AMZN", "JPM", "MMM"],
            "utility_rank":       ["JPM", "XOM", "MMM", "AMZN", "TSLA"],
            "user_choice_rank":   ["JPM", "XOM", "TSLA", "MMM", "AMZN"],
        },
        "meta": {
            "candidate_tickers":  ["AMZN", "JPM", "LIN", "MMM", "TSLA", "XOM", "SPG", "PG", "VZ", "MRK"],
            "user_risk_profile":  "Moderate",
            "horizon_days":       14,
        },
        "prompt": (
            "[ADVISOR] Thanks for making the time today. AMZN up 3% pre-market on AWS. "
            "JPM upgraded by two analysts. "
            "Candidate stocks: AMZN, JPM, LIN, MMM, TSLA, XOM, SPG, PG, VZ, MRK. "
            "[CLIENT PROFILE] Moderate risk. 45–55. Dividend focus. Rate sensitive."
        ),
    },
]

# What our encoder extracts FROM the 3 raw rows above — this is the transformation
HF_RAW_ENCODED = {
    "nodes": [
        {"type": "belief",  "label": "energy_conviction_over_momentum",
         "summary": "Client ranks XOM top across 3 sessions despite TSLA having stronger momentum signal. Dividend preference over growth."},
        {"type": "belief",  "label": "skeptical_of_cloud_multiples",
         "summary": "Explicitly rejected AMZN 3% rally — 'I don't trust cloud multiples right now.' Valuation-anchored thinking."},
        {"type": "emotion", "label": "analyst_driven_conviction_shift",
         "summary": "On step 11, two JPM upgrades immediately moved JPM from #3 to #1. Responsive to institutional signals."},
        {"type": "action",  "label": "consistent_tsla_underweight",
         "summary": "TSLA ranked 2nd, 3rd, 3rd across 3 sessions despite being #1 in momentum_rank all 3 days. Deliberate underweight vs momentum."},
    ],
    "edges": [
        ("energy_conviction_over_momentum", "TENSION_WITH",  "consistent_tsla_underweight"),
        ("analyst_driven_conviction_shift",  "LED_TO",        "jpmorgan_moved_to_top_rank"),
        ("skeptical_of_cloud_multiples",     "REFLECTS_ON",  "energy_conviction_over_momentum"),
    ],
    "advisor_alert": {
        "action":   "MONITOR",
        "trigger":  "Energy sector news — any XOM-specific event (earnings, dividend cut, oil move >5%)",
        "context":  (
            "Client is anchored to XOM across all 3 sessions regardless of momentum. "
            "Responds quickly to analyst upgrades (JPM step 11). "
            "Actively avoids momentum chasing — this is a behavioural signal, not ignorance."
        ),
        "suggested_approach": (
            "Frame any rebalancing suggestion around analyst opinion, not price action. "
            "'Two analysts upgraded X' will land. 'X is up 8% this week' will not move this client. "
            "Watch for XOM-specific negative catalyst — this client will be slow to exit."
        ),
    },
}


def load_hf_clients(use_live: bool = False):
    """
    Returns client data from HuggingFace datasets.

    use_live=True: attempts real download from HuggingFace Hub (requires internet).
    use_live=False: returns bundled sample rows that mirror Conv-FinRe / hub24 schema.
    """
    if use_live:
        try:
            from datasets import load_dataset
            ds = load_dataset("TheFinAI/conv-finre", split="train", streaming=True)
            rows = []
            for i, row in enumerate(ds):
                if i >= 3:
                    break
                rows.append(row)
            return rows, True
        except Exception as e:
            return HF_SAMPLE_CLIENTS, False

    return HF_SAMPLE_CLIENTS, False
