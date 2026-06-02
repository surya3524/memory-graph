"""
Market Event Trigger System — maps real-world events to client alerts.
"""

from graph_engine import build_graph, query_alerts

MARKET_SCENARIOS = {
    "market_drop_5pct": {
        "label": "S&P 500 drops 5%+ in a session",
        "description": "Broad equity market sell-off. Single session decline exceeding 5%.",
    },
    "market_drop_10pct": {
        "label": "S&P 500 correction — down 10%+ from peak",
        "description": "Correction territory. Sustained multi-week decline.",
    },
    "recession_news": {
        "label": "Recession language dominant in major financial media",
        "description": "WSJ, Bloomberg, CNBC leading with recession probability coverage.",
    },
    "fed_rate_decision": {
        "label": "Federal Reserve rate decision — unexpected move",
        "description": "Fed surprises market with rate cut or hold against expectations.",
    },
    "fed_money_printing": {
        "label": "Federal Reserve announces large-scale asset purchases",
        "description": "QE announcement or balance sheet expansion.",
    },
    "inflation_data_high": {
        "label": "CPI print significantly above expectations",
        "description": "Inflation data surprises to the upside.",
    },
    "taiwan_strait_news": {
        "label": "Taiwan Strait military tensions escalate",
        "description": "Geopolitical escalation in Taiwan Strait. Semiconductor supply chain risk.",
    },
    "china_export_controls": {
        "label": "China announces semiconductor export restrictions",
        "description": "New controls on chip materials or equipment affecting US supply chain.",
    },
    "nvda_earnings_miss": {
        "label": "NVIDIA misses earnings expectations",
        "description": "NVDA reports below-consensus revenue or guidance.",
    },
    "soxx_drop_10pct": {
        "label": "Semiconductor ETF (SOXX) down 10%+ from recent high",
        "description": "Broad semiconductor sector drawdown.",
    },
    "oil_price_drop_15pct": {
        "label": "WTI crude oil drops 15%+ in 30 days",
        "description": "Significant oil price decline. Energy sector under pressure.",
    },
    "energy_policy_news": {
        "label": "Major energy policy announcement",
        "description": "Drilling permit changes, pipeline regulation, or energy tax policy shift.",
    },
    "opec_decision": {
        "label": "OPEC+ production decision surprises market",
        "description": "Unexpected output cut or increase affecting crude prices.",
    },
    "dollar_weakness": {
        "label": "US Dollar Index (DXY) weakens significantly",
        "description": "Dollar declining vs. major currencies. Inflation hedge assets in focus.",
    },
    "gold_price_drop": {
        "label": "Gold drops 5%+ from recent high",
        "description": "Precious metals sell-off despite macro environment.",
    },
    "portfolio_underperforms_sp500": {
        "label": "Client portfolio underperforms S&P 500 by 2%+ this quarter",
        "description": "Benchmark comparison shows meaningful lag.",
    },
    "market_rally_10pct": {
        "label": "S&P 500 rallies 10%+ from recent low",
        "description": "Strong recovery. Clients sitting in cash may feel they missed it.",
    },
    "within_24mo_of_retirement": {
        "label": "Client is within 24 months of planned retirement date",
        "description": "Sequence-of-returns risk window is active.",
    },
}

ACTION_COLORS = {
    "CALL FIRST":               "🔴",
    "CALL THIS WEEK":           "🟠",
    "EMAIL TODAY":              "🟡",
    "PROACTIVE EMAIL":          "🟡",
    "PROACTIVE EXPLANATION — EMAIL BEFORE SHE SENDS ONE": "🟡",
    "CALL CAROL FIRST, THEN JIM": "🟠",
    "HEADS UP":                 "🟢",
    "GENTLE CHECK-IN":          "🟢",
    "MONITOR":                  "🟢",
}


def run_trigger(trigger_key: str) -> list:
    G = build_graph()
    return query_alerts(G, trigger_key)


def print_alerts(trigger_key: str):
    scenario = MARKET_SCENARIOS.get(trigger_key, {})
    label = scenario.get("label", trigger_key)
    description = scenario.get("description", "")

    print(f"\n{'━' * 70}")
    print(f"  MARKET EVENT: {label}")
    print(f"  {description}")
    print(f"{'━' * 70}\n")

    alerts = run_trigger(trigger_key)

    if not alerts:
        print("  No clients flagged for this trigger.\n")
        return

    print(f"  {len(alerts)} client(s) need your attention:\n")
    for i, a in enumerate(alerts, 1):
        action = a["alert"]["action"]
        icon = ACTION_COLORS.get(action, "⚪")
        print(f"  {i}. {icon}  {a['name']}")
        print(f"     Action   : {action}")
        print(f"     Archetype: {a['archetype']}")
        print(f"\n     Why now:")
        for line in a["alert"]["context"].split(". "):
            line = line.strip()
            if line:
                print(f"       — {line}.")
        print(f"\n     Suggested approach:")
        for line in a["alert"]["suggested_approach"].split(". "):
            line = line.strip()
            if line:
                print(f"       {line}.")
        print()


if __name__ == "__main__":
    print_alerts("market_drop_5pct")
    print_alerts("taiwan_strait_news")
    print_alerts("oil_price_drop_15pct")
