"""
Client Financial Memory Graph — Sample Client Data
Eight synthetic client archetypes built from behavioral finance research
(Dalbar QAIB, Morningstar Mind the Gap, Vanguard Advisor's Alpha)
"""

CLIENTS = [
    {
        "id": "john_m",
        "name": "John M.",
        "age": 58,
        "archetype": "Regretful Seller",
        "alert_priority": 1,
        "trigger_conditions": ["market_drop_5pct", "market_drop_10pct"],
        "meetings": [
            {
                "date": "2020-03-18",
                "note": "Client called with concerns. Markets down 30% from peak. "
                        "Requested to move all equity positions to cash immediately. "
                        "Advisor counseled against it. Client insisted.",
                "nodes": [
                    {"type": "emotion", "label": "heightened_concern_under_drawdown"},
                    {"type": "action",  "label": "sold_100pct_equities"},
                    {"type": "event",   "label": "covid_market_crash_mar2020"},
                ],
                "edges": [
                    ("sold_100pct_equities", "TRIGGERED_BY", "covid_market_crash_mar2020"),
                    ("heightened_concern_under_drawdown", "LED_TO", "sold_100pct_equities"),
                ],
            },
            {
                "date": "2020-09-10",
                "note": "Client re-engaged after missing most of the recovery. "
                        "Said selling in March was his biggest financial mistake. "
                        "Asked how to avoid repeating it. Agreed to a volatility plan.",
                "nodes": [
                    {"type": "belief", "label": "regrets_march_2020_sale"},
                    {"type": "belief", "label": "wants_behavioral_guardrails"},
                ],
                "edges": [
                    ("regrets_march_2020_sale", "REFLECTS_ON", "sold_100pct_equities"),
                ],
            },
            {
                "date": "2022-06-15",
                "note": "Markets down 20% YTD. Client called asking 'should I do anything?' "
                        "Referenced 2020 unprompted — said he did not want to repeat it. "
                        "Held position. No action taken.",
                "nodes": [
                    {"type": "emotion", "label": "caution_resurfaced_2022"},
                    {"type": "action",  "label": "held_position_2022"},
                ],
                "edges": [
                    ("caution_resurfaced_2022", "CONTAINED_BY", "regrets_march_2020_sale"),
                    ("held_position_2022", "INFORMED_BY", "regrets_march_2020_sale"),
                ],
            },
            {
                "date": "2025-01-20",
                "note": "Annual review. Portfolio recovered fully. Client satisfied. "
                        "Reiterated: 'Promise me you will call me before I do something I'll regret "
                        "if the market drops again.'",
                "nodes": [
                    {"type": "belief", "label": "explicitly_requested_proactive_outreach"},
                ],
                "edges": [
                    ("explicitly_requested_proactive_outreach", "EVOLVED_FROM", "regrets_march_2020_sale"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "S&P 500 down >5% in a session",
            "action": "CALL FIRST",
            "context": (
                "John sold everything in March 2020 and later called it his biggest financial mistake. "
                "He has explicitly asked to be contacted before he acts during a downturn. "
                "A >5% drop matches the exact conditions of that prior decision."
            ),
            "suggested_approach": (
                "Acknowledge the drop directly. Reference his own words from 2020. "
                "Remind him of the volatility plan you built together. "
                "Do not wait for him to call you."
            ),
        },
    },

    {
        "id": "sarah_k",
        "name": "Sarah K.",
        "age": 61,
        "archetype": "Capital Preserver",
        "alert_priority": 2,
        "trigger_conditions": ["recession_language", "fed_rate_decision", "market_drop_5pct"],
        "meetings": [
            {
                "date": "2019-04-03",
                "note": "New client onboarding. Lost 45% of portfolio in 2008 before selling. "
                        "Took five years to re-enter the market. "
                        "States her primary goal is to never experience that again. "
                        "Currently holds 40% in cash/money market.",
                "nodes": [
                    {"type": "event",  "label": "2008_financial_crisis_loss"},
                    {"type": "belief", "label": "capital_preservation_primary_goal"},
                    {"type": "action", "label": "holds_40pct_cash_position"},
                ],
                "edges": [
                    ("capital_preservation_primary_goal", "SHAPED_BY", "2008_financial_crisis_loss"),
                    ("holds_40pct_cash_position", "DRIVEN_BY", "capital_preservation_primary_goal"),
                ],
            },
            {
                "date": "2021-03-15",
                "note": "Discussed reducing cash position given inflation eroding purchasing power. "
                        "Client acknowledged the logic but said she would rather lose to inflation "
                        "than risk another 2008. Cash position unchanged at 38%.",
                "nodes": [
                    {"type": "belief", "label": "inflation_loss_preferable_to_market_loss"},
                ],
                "edges": [
                    ("inflation_loss_preferable_to_market_loss", "REINFORCES", "capital_preservation_primary_goal"),
                ],
            },
            {
                "date": "2023-09-20",
                "note": "Third conversation about cash drag. Client now earning 5% on money market. "
                        "Said 'finally my cash is doing something.' Less urgency to deploy it. "
                        "Cash position now 42% — slightly increased.",
                "nodes": [
                    {"type": "belief", "label": "high_rate_environment_validates_cash_thesis"},
                    {"type": "action", "label": "increased_cash_to_42pct_2023"},
                ],
                "edges": [
                    ("high_rate_environment_validates_cash_thesis", "REINFORCES", "holds_40pct_cash_position"),
                ],
            },
            {
                "date": "2025-02-10",
                "note": "Annual review. Discussed sequence-of-returns risk as she approaches 65. "
                        "Client receptive for the first time to a glide-path conversation. "
                        "Agreed to review a model with 30% cash floor instead of 40%.",
                "nodes": [
                    {"type": "belief", "label": "first_openness_to_reducing_cash_floor"},
                ],
                "edges": [
                    ("first_openness_to_reducing_cash_floor", "EVOLVED_FROM", "capital_preservation_primary_goal"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Recession coverage in major news / Fed signals rate cuts",
            "action": "EMAIL TODAY",
            "context": (
                "Sarah's 2008 experience is the defining event in her financial life. "
                "She has held 40%+ in cash for six years. "
                "In February 2025 she showed the first openness to reducing that floor — "
                "a volatile market may close that window quickly."
            ),
            "suggested_approach": (
                "Send a calm, factual market context note before she sees the headlines. "
                "Reference her 2025 conversation about the 30% cash floor. "
                "This is not the moment to push change — it is the moment to hold the ground already gained."
            ),
        },
    },

    {
        "id": "michael_t",
        "name": "Michael T.",
        "age": 55,
        "archetype": "Sector Believer — Semiconductors",
        "alert_priority": 3,
        "trigger_conditions": ["taiwan_strait_news", "china_export_controls", "nvda_earnings_miss", "soxx_drop_10pct"],
        "meetings": [
            {
                "date": "2022-01-10",
                "note": "Retirement rollover — $1.2M from Intel 401k. "
                        "Client has 30 years in semiconductor industry. "
                        "Wants heavy allocation to NVDA, AMD, SOXX. "
                        "Said 'I know this industry better than any fund manager.'",
                "nodes": [
                    {"type": "belief", "label": "deep_domain_conviction_semis"},
                    {"type": "action", "label": "concentrated_semi_allocation_2022"},
                ],
                "edges": [
                    ("concentrated_semi_allocation_2022", "DRIVEN_BY", "deep_domain_conviction_semis"),
                ],
            },
            {
                "date": "2022-11-15",
                "note": "NVDA down 65% from peak. Client calm — 'I've seen cycles. This is temporary.' "
                        "No changes made. Noted that his wife is uncomfortable with the volatility.",
                "nodes": [
                    {"type": "emotion", "label": "calm_under_major_drawdown"},
                    {"type": "belief",  "label": "cycle_reasoning_under_stress"},
                    {"type": "belief",  "label": "spouse_discomfort_with_concentration"},
                ],
                "edges": [
                    ("calm_under_major_drawdown", "SUPPORTED_BY", "deep_domain_conviction_semis"),
                    ("spouse_discomfort_with_concentration", "TENSION_WITH", "deep_domain_conviction_semis"),
                ],
            },
            {
                "date": "2024-04-08",
                "note": "Client said wife brought up concentration again at dinner. "
                        "He agreed to 'think about' moving 15% to broader index. "
                        "First time he has acknowledged the household dimension of this decision.",
                "nodes": [
                    {"type": "belief", "label": "first_flexibility_on_concentration_2024"},
                ],
                "edges": [
                    ("first_flexibility_on_concentration_2024", "INFLUENCED_BY", "spouse_discomfort_with_concentration"),
                ],
            },
            {
                "date": "2025-01-14",
                "note": "Discussed Taiwan geopolitical risk. Client aware and watching closely. "
                        "Said 'if something happens in the strait, semis get hit hard and fast.' "
                        "Did not change allocation but acknowledged the tail risk for the first time.",
                "nodes": [
                    {"type": "belief", "label": "geopolitical_risk_acknowledged_2025"},
                ],
                "edges": [
                    ("geopolitical_risk_acknowledged_2025", "MODIFIES", "deep_domain_conviction_semis"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Taiwan Strait tensions / China semiconductor export controls",
            "action": "CALL THIS WEEK",
            "context": (
                "Michael holds a concentrated semiconductor position (~$980k across NVDA, AMD, SOXX). "
                "He acknowledged Taiwan risk explicitly in January 2025. "
                "His wife has raised concentration concerns twice — this event may bring it up again at home. "
                "He has shown first signs of flexibility on rebalancing."
            ),
            "suggested_approach": (
                "Acknowledge his industry expertise — do not talk down to it. "
                "Reference his own January 2025 comment about Taiwan tail risk. "
                "Frame any rebalancing conversation around the household decision, not the market move. "
                "The spouse concern is the real lever here."
            ),
        },
    },

    {
        "id": "bobby_h",
        "name": "Robert 'Bobby' H.",
        "age": 63,
        "archetype": "Sector Believer — Oil & Gas",
        "alert_priority": 3,
        "trigger_conditions": ["oil_price_drop_15pct", "energy_policy_news", "opec_decision"],
        "meetings": [
            {
                "date": "2019-06-12",
                "note": "Third-generation oil family. Has royalty income from two producing wells in Permian. "
                        "Holds XOM, CVX, and pipeline MLPs. "
                        "Said 'my daddy made his money in oil. I will too. "
                        "These green energy mandates are political, not economic.'",
                "nodes": [
                    {"type": "belief", "label": "generational_energy_sector_identity"},
                    {"type": "belief", "label": "skepticism_of_energy_transition_thesis"},
                    {"type": "action", "label": "concentrated_og_and_royalty_income"},
                ],
                "edges": [
                    ("concentrated_og_and_royalty_income", "DRIVEN_BY", "generational_energy_sector_identity"),
                ],
            },
            {
                "date": "2020-04-28",
                "note": "WTI briefly went negative. Client called. "
                        "Said 'that was futures manipulation, not the real market.' "
                        "Held all positions. Added to XOM at the low.",
                "nodes": [
                    {"type": "belief", "label": "dismisses_negative_oil_event_as_anomaly"},
                    {"type": "action", "label": "added_xom_at_2020_low"},
                ],
                "edges": [
                    ("dismisses_negative_oil_event_as_anomaly", "REINFORCES", "generational_energy_sector_identity"),
                ],
            },
            {
                "date": "2022-09-14",
                "note": "Energy sector up 60% YTD. Client called to add more pipeline exposure. "
                        "Advisor flagged concentration risk. Client said 'I told you so' and added anyway. "
                        "Position now ~70% energy.",
                "nodes": [
                    {"type": "action", "label": "increased_concentration_at_cycle_peak_2022"},
                    {"type": "belief", "label": "2022_rally_reinforces_og_thesis"},
                ],
                "edges": [
                    ("increased_concentration_at_cycle_peak_2022", "DRIVEN_BY", "2022_rally_reinforces_og_thesis"),
                ],
            },
            {
                "date": "2024-11-05",
                "note": "Post-election meeting. Client relieved by election outcome for energy policy. "
                        "Said 'drilling permits will open up, this is good for us.' "
                        "First time he mentioned policy risk as a factor — previously dismissed it.",
                "nodes": [
                    {"type": "belief", "label": "political_environment_now_a_factor_2024"},
                ],
                "edges": [
                    ("political_environment_now_a_factor_2024", "MODIFIES", "skepticism_of_energy_transition_thesis"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Oil price drops >15% / adverse energy policy announcement",
            "action": "CALL THIS WEEK",
            "context": (
                "Bobby holds ~70% energy concentration including royalty income, XOM, CVX, and MLPs. "
                "He added at the 2022 cycle peak. He has a history of dismissing negative signals as anomalies. "
                "His identity is deeply tied to the sector — direct challenges to the thesis are counterproductive."
            ),
            "suggested_approach": (
                "Never challenge the sector identity directly. "
                "Frame diversification as protecting the O&G income, not replacing it. "
                "Ask about his royalty income stability first — that is the emotional anchor. "
                "A cyclical softening conversation lands better than a transition narrative."
            ),
        },
    },

    {
        "id": "linda_p",
        "name": "Linda P.",
        "age": 52,
        "archetype": "Inflation Hedge Seeker — Gold & Hard Assets",
        "alert_priority": 4,
        "trigger_conditions": ["fed_money_printing", "inflation_data_high", "dollar_weakness", "gold_price_drop"],
        "meetings": [
            {
                "date": "2020-06-18",
                "note": "Client opened account after COVID stimulus announcements. "
                        "Said 'when they printed $6 trillion I knew the dollar was being debased.' "
                        "Wants 25% in gold ETF, 5% in silver. Reads Austrian economics. "
                        "Mentioned she also has physical gold stored at home — amount unspecified.",
                "nodes": [
                    {"type": "belief", "label": "inflation_protection_thesis"},
                    {"type": "belief", "label": "gold_as_primary_store_of_value"},
                    {"type": "action", "label": "25pct_gold_etf_5pct_silver_allocation"},
                    {"type": "belief", "label": "holds_undisclosed_physical_gold"},
                ],
                "edges": [
                    ("25pct_gold_etf_5pct_silver_allocation", "DRIVEN_BY", "inflation_protection_thesis"),
                    ("holds_undisclosed_physical_gold", "REFLECTS", "gold_as_primary_store_of_value"),
                ],
            },
            {
                "date": "2022-06-10",
                "note": "CPI hit 9.1%. Client called — 'I told you.' "
                        "Wants to increase gold to 35%. Advisor discussed diversified inflation hedges "
                        "(TIPS, commodities, real estate). Client receptive to TIPS but not others.",
                "nodes": [
                    {"type": "belief", "label": "inflation_peak_2022_validates_thesis"},
                    {"type": "belief", "label": "open_to_tips_not_other_inflation_hedges"},
                ],
                "edges": [
                    ("inflation_peak_2022_validates_thesis", "REINFORCES", "gold_as_primary_store_of_value"),
                ],
            },
            {
                "date": "2023-08-22",
                "note": "Gold flat while equities rallied. Client frustrated. "
                        "Said 'paper gold is being suppressed by the banks.' "
                        "Beginning to discuss Bitcoin as 'digital gold.' Not yet in portfolio.",
                "nodes": [
                    {"type": "belief", "label": "paper_gold_suppression_theory"},
                    {"type": "belief", "label": "bitcoin_as_digital_gold_emerging_interest"},
                ],
                "edges": [
                    ("bitcoin_as_digital_gold_emerging_interest", "EVOLVES_FROM", "gold_as_primary_store_of_value"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Gold price drops significantly / Fed signals more stimulus",
            "action": "PROACTIVE EMAIL",
            "context": (
                "Linda holds 30%+ in gold and silver instruments plus undisclosed physical gold. "
                "She has expressed interest in Bitcoin as a hard asset extension. "
                "When gold underperforms she attributes it to market manipulation — "
                "data-only conversations are less effective with her."
            ),
            "suggested_approach": (
                "Work with the inflation thesis, not against it. "
                "Present a diversified hard-asset basket (gold + TIPS + commodities) as stronger than gold alone. "
                "On Bitcoin — if she raises it, do not dismiss it. Discuss position sizing and custody risk. "
                "Ask about the physical gold at home — insurance and estate planning angles are useful here."
            ),
        },
    },

    {
        "id": "carol_jim_b",
        "name": "Carol & Jim B.",
        "age": "Jim: 62, Carol: 61",
        "archetype": "Near-Retiree Couple — Divergent Risk Profiles",
        "alert_priority": 2,
        "trigger_conditions": ["market_drop_5pct", "recession_news", "within_24mo_of_retirement"],
        "meetings": [
            {
                "date": "2023-03-08",
                "note": "Joint review. Jim ready to retire this year. Carol wants to work 2 more years. "
                        "Jim: 'We have enough, I want to golf and travel.' "
                        "Carol: 'What if the market drops right when we retire? "
                        "My mother ran out of money at 82. I think about that a lot.'",
                "nodes": [
                    {"type": "belief", "label": "jim_retirement_ready_optimistic"},
                    {"type": "belief", "label": "carol_sequence_of_returns_concern"},
                    {"type": "belief", "label": "carol_anchored_to_mothers_experience"},
                    {"type": "belief", "label": "carol_working_for_healthcare_not_just_income"},
                ],
                "edges": [
                    ("carol_sequence_of_returns_concern", "ROOTED_IN", "carol_anchored_to_mothers_experience"),
                    ("carol_working_for_healthcare_not_just_income", "DRIVEN_BY", "carol_sequence_of_returns_concern"),
                    ("jim_retirement_ready_optimistic", "TENSION_WITH", "carol_sequence_of_returns_concern"),
                ],
            },
            {
                "date": "2024-01-17",
                "note": "Separate conversations requested. "
                        "Jim (alone): 'Can we retire sooner? Carol is being too conservative.' "
                        "Carol (alone): 'I need to know we have a plan if things go wrong in year one.' "
                        "Household alignment is the core work here, not portfolio allocation.",
                "nodes": [
                    {"type": "belief", "label": "couple_divergence_requires_separate_conversations"},
                    {"type": "belief", "label": "carol_needs_downside_scenario_plan_documented"},
                ],
                "edges": [
                    ("couple_divergence_requires_separate_conversations", "REFLECTS", "jim_retirement_ready_optimistic"),
                    ("carol_needs_downside_scenario_plan_documented", "EVOLVES_FROM", "carol_sequence_of_returns_concern"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Market drops >5% / Recession coverage / Within 24 months of retirement date",
            "action": "CALL CAROL FIRST, THEN JIM",
            "context": (
                "Carol and Jim have meaningfully different risk outlooks. "
                "Carol's caution is anchored to her mother's experience running out of money. "
                "Jim is optimistic and ready to stop working. "
                "A market event will affect them differently — Carol needs reassurance, Jim needs reframing."
            ),
            "suggested_approach": (
                "Call Carol first. Reference the downside scenario plan built in January 2024 — "
                "show her the plan exists and it covers this. "
                "Then call Jim separately. Acknowledge the market move without amplifying it. "
                "Do not do a joint call in a volatile moment — their reactions will conflict."
            ),
        },
    },

    {
        "id": "marcus_w",
        "name": "Marcus W.",
        "age": 38,
        "archetype": "Sudden Wealth — Inheritance",
        "alert_priority": 5,
        "trigger_conditions": ["market_drop_5pct", "12mo_inaction_flag", "market_rally_10pct"],
        "meetings": [
            {
                "date": "2024-02-14",
                "note": "First meeting. Inherited $800k from father who passed in December. "
                        "No prior investment experience. "
                        "Said 'I don't feel like it's mine to invest. It was his money.' "
                        "Currently sitting in money market for 14 months. "
                        "Has a brother who is pressuring him about splitting the inheritance — "
                        "will is clear that it belongs to Marcus alone.",
                "nodes": [
                    {"type": "belief", "label": "emotional_ownership_barrier_to_investing"},
                    {"type": "belief", "label": "family_tension_over_inheritance"},
                    {"type": "belief", "label": "loss_framed_as_losing_father_twice"},
                    {"type": "action", "label": "800k_sitting_in_money_market_14mo"},
                ],
                "edges": [
                    ("800k_sitting_in_money_market_14mo", "CAUSED_BY", "emotional_ownership_barrier_to_investing"),
                    ("emotional_ownership_barrier_to_investing", "CONNECTED_TO", "loss_framed_as_losing_father_twice"),
                    ("family_tension_over_inheritance", "ADDS_STRESS_TO", "emotional_ownership_barrier_to_investing"),
                ],
            },
            {
                "date": "2024-07-09",
                "note": "Second meeting. Marcus has been reading about investing but not acting. "
                        "Mentioned his father was a saver, not an investor. "
                        "'He would have wanted this to be safe.' "
                        "Opened to the idea of a conservative allocation if framed as honoring his father's values.",
                "nodes": [
                    {"type": "belief", "label": "fathers_values_conservative_saver"},
                    {"type": "belief", "label": "honoring_father_as_frame_for_investing"},
                ],
                "edges": [
                    ("honoring_father_as_frame_for_investing", "UNLOCKS", "emotional_ownership_barrier_to_investing"),
                    ("fathers_values_conservative_saver", "INFORMS", "honoring_father_as_frame_for_investing"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Any significant market move / 12-month inaction flag",
            "action": "GENTLE CHECK-IN",
            "context": (
                "Marcus has $800k sitting uninvested. The barrier is emotional, not financial. "
                "He is processing grief alongside a financial decision. "
                "His brother's pressure adds stress that may delay action further. "
                "In July 2024 he responded to the framing of investing as honoring his father's intentions."
            ),
            "suggested_approach": (
                "Do not lead with market performance or opportunity cost. "
                "Lead with his father's values — safety, preserving what he built. "
                "A conservative allocation (bonds, dividend equities) framed as stewardship "
                "is more likely to move him than a return-focused conversation. "
                "Do not mention the brother situation unless he raises it."
            ),
        },
    },

    {
        "id": "priya_n",
        "name": "Priya N.",
        "age": 44,
        "archetype": "DIY Defector — Rebuilding Trust",
        "alert_priority": 4,
        "trigger_conditions": ["portfolio_underperforms_sp500", "fee_discussion", "market_rally_strong"],
        "meetings": [
            {
                "date": "2022-11-03",
                "note": "New client. Managed own portfolio for 12 years on Fidelity. "
                        "Lost $180k in ARK Innovation ETF in 2022. "
                        "Said 'I thought I understood the thesis. I was wrong.' "
                        "Came to an advisor for the first time. Brought a 6-page spreadsheet.",
                "nodes": [
                    {"type": "event",  "label": "ark_etf_loss_180k_2022"},
                    {"type": "belief", "label": "self_directed_investor_identity_shaken"},
                    {"type": "belief", "label": "spreadsheet_driven_analytical_style"},
                ],
                "edges": [
                    ("self_directed_investor_identity_shaken", "CAUSED_BY", "ark_etf_loss_180k_2022"),
                ],
            },
            {
                "date": "2023-04-20",
                "note": "Quarterly review. Priya sent three articles before the meeting — "
                        "two questioning active management, one on expense ratios. "
                        "Asked 'why are we not just in VOO?' "
                        "Advisor walked through the reasoning. She took notes. Did not push back further.",
                "nodes": [
                    {"type": "belief", "label": "cost_and_evidence_focused_decision_maker"},
                    {"type": "belief", "label": "trust_earned_through_transparency_not_authority"},
                ],
                "edges": [
                    ("trust_earned_through_transparency_not_authority", "SHAPED_BY", "self_directed_investor_identity_shaken"),
                ],
            },
            {
                "date": "2024-09-11",
                "note": "Portfolio slightly underperformed S&P 500 YTD. "
                        "Priya flagged it before advisor did. "
                        "'I track this monthly. Can you explain the drag?' "
                        "Advisor explained international allocation rationale. She accepted it. "
                        "'Okay. But I'm watching.'",
                "nodes": [
                    {"type": "belief", "label": "actively_monitors_benchmark_comparison"},
                    {"type": "belief", "label": "trust_remains_conditional_on_performance_explanation"},
                ],
                "edges": [
                    ("actively_monitors_benchmark_comparison", "REFLECTS", "spreadsheet_driven_analytical_style"),
                    ("trust_remains_conditional_on_performance_explanation", "EVOLVES_FROM", "trust_earned_through_transparency_not_authority"),
                ],
            },
        ],
        "advisor_alert": {
            "trigger": "Portfolio underperforms S&P 500 benchmark by >2% in a quarter",
            "action": "PROACTIVE EXPLANATION — EMAIL BEFORE SHE SENDS ONE",
            "context": (
                "Priya tracks benchmark performance monthly and will flag underperformance herself. "
                "She lost $180k in ARK in 2022 — a high-conviction narrative investment that failed. "
                "She now trusts evidence and transparency over authority. "
                "If she identifies the underperformance before you explain it, trust erodes."
            ),
            "suggested_approach": (
                "Send the performance explanation before she asks. "
                "Use data — she will read every number. "
                "Never say 'trust the process' — show the process. "
                "Reference the international allocation conversation from September 2024 "
                "to show continuity of reasoning."
            ),
        },
    },
]


if __name__ == "__main__":
    print(f"Loaded {len(CLIENTS)} client archetypes\n")
    for c in CLIENTS:
        meetings = len(c["meetings"])
        nodes    = sum(len(m["nodes"]) for m in c["meetings"])
        edges    = sum(len(m["edges"]) for m in c["meetings"])
        print(f"  {c['name']:<20} | {c['archetype']:<45} | {meetings} meetings | {nodes} nodes | {edges} edges")
