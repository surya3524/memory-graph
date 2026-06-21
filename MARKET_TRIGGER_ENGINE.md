# Market Trigger Engine — Technical Design
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## Verified: Raymond James Uses FactSet for Market Data

Raymond James officially selected FactSet as its market data provider for all
U.S. financial advisors in August 2022. Over 7,500 advisor workstations were
deployed with FactSet's Wealth Workstation. Raymond James Canada also uses
FactSet for its 900+ advisors.

**Source (verified):**
https://www.globenewswire.com/news-release/2022/08/17/2499935/7768/en/Raymond-James-Selects-FactSet-as-the-Market-Data-Provider-for-U.S.-Financial-Advisors.html

**Official FactSet press release:**
https://investor.factset.com/news-releases/news-release-details/raymond-james-selects-factset-market-data-provider-us-financial

**Submission narrative:**
> "The POC uses Alpaca and Benzinga for market event streaming. In production,
> the trigger engine connects to Raymond James's existing FactSet data feed —
> the same market data platform already deployed across 7,500 RJ advisor
> workstations. The graph matching and alert generation logic is data-source
> agnostic. The intelligence is in the graph, not the feed."

---

## Two Data Sources Cover All Trigger Scenarios

| Trigger Type | POC Data Source | Production (RJ) |
|---|---|---|
| Price moves (SPY drops 5%) | Polygon.io WebSocket | FactSet real-time feed |
| News events (Fed, CPI, Taiwan) | Alpaca + Benzinga stream | FactSet News API |
| SEC filings, earnings | Alpaca + Benzinga | FactSet fundamentals |

### Are Alpaca/Benzinga Enterprise Grade?
No — they are suitable for POC and startups, not production at RJ scale.

| | Alpaca + Benzinga | FactSet (what RJ uses) |
|---|---|---|
| Who uses it | Retail traders, fintech startups | Goldman, JPMorgan, Raymond James |
| Uptime SLA | 99.9% self-reported | 99.99% contractual |
| News latency | Seconds | Milliseconds |
| Cost | $37–$197/month | Enterprise contract |
| Regulatory coverage | General market news | Full SEC, Fed wire, earnings |

---

## Dynamic Trigger Generation (Not Hardcoded)

Trigger conditions are NOT hardcoded. Claude reads each client's memory graph
at onboarding and generates what market conditions should trigger an alert for
that specific client.

```python
def generate_triggers_for_client(client_id: str) -> list[dict]:
    """
    Ask Claude to read this client's graph and generate
    what market conditions should trigger an alert for them.
    """
    graph = CLIENT_GRAPHS[client_id]
    nodes_text = "\n".join([
        f"[{n['node_type'].upper()}] {n['label']}: {n['value']}"
        for n in graph["nodes"]
    ])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""You are a financial risk analyst.
        Given a client's memory graph, identify what market events
        should trigger an advisor alert for this specific client.

        Return a JSON array of trigger conditions. Each condition must have:
        - scenario: plain English name
        - source: "price" or "news"
        - keywords: list of words to watch for (if news)
        - symbol: stock symbol to watch (if price)
        - threshold_type: "pct_change" | "pct_from_52w_high" | "price_level" | "keyword"
        - threshold: numeric value (if price)
        - direction: "below" or "above" (if price)
        - reason: why this client specifically needs this alert
        """,
        messages=[{
            "role": "user",
            "content": f"Client: {graph['client_name']}\n\nMemory graph:\n{nodes_text}\n\nGenerate trigger conditions based only on what is in their graph."
        }]
    )
    return json.loads(response.content[0].text)
```

### Example Output — John M. (panic-sold in 2020)
```json
[
  {
    "scenario": "Single session equity drop",
    "source": "price",
    "symbol": "SPY",
    "threshold_type": "pct_change",
    "threshold": -3.0,
    "direction": "below",
    "reason": "Client panic-sold during March 2020 drop. Any significant drop risks repeat behavior."
  },
  {
    "scenario": "Recession narrative in financial media",
    "source": "news",
    "threshold_type": "keyword",
    "keywords": ["recession", "bear market", "crash", "selloff"],
    "reason": "Client emotion node shows fear response to recession language."
  }
]
```

### Example Output — Michael T. (Taiwan semiconductor believer)
```json
[
  {
    "scenario": "Taiwan geopolitical tension",
    "source": "news",
    "threshold_type": "keyword",
    "keywords": ["Taiwan", "Taiwan Strait", "TSMC", "China military"],
    "reason": "Client holds concentrated semiconductor position. Taiwan news directly threatens his thesis."
  },
  {
    "scenario": "Semiconductor sector drop",
    "source": "price",
    "symbol": "SOXX",
    "threshold_type": "pct_change",
    "threshold": -5.0,
    "direction": "below",
    "reason": "Client sector belief node tied to semiconductor performance."
  }
]
```

### Example Output — Priya N. (inflation hedge seeker)
```json
[
  {
    "scenario": "CPI above expectations",
    "source": "news",
    "threshold_type": "keyword",
    "keywords": ["CPI", "inflation", "hotter than expected", "price surge"],
    "reason": "Client holds inflation hedge positions. CPI data directly relevant."
  },
  {
    "scenario": "Fed rate cut announcement",
    "source": "news",
    "threshold_type": "keyword",
    "keywords": ["Fed cuts", "rate cut", "dovish", "stimulus"],
    "reason": "Rate cuts signal dollar weakness — client's hedge thesis strengthens."
  }
]
```

---

## Four Threshold Types Explained

```python
# Type 1 — Percentage change in a single session
{
    "threshold_type": "pct_change",
    "threshold": -5.0,       # -5% today
    "direction": "below"
}

# Type 2 — Change from 52-week high (correction territory)
{
    "threshold_type": "pct_from_52w_high",
    "threshold": -10.0,      # -10% from peak = correction
    "direction": "below"
}

# Type 3 — Absolute price level
{
    "threshold_type": "price_level",
    "threshold": 60.0,       # Oil below $60/barrel
    "direction": "below"
}

# Type 4 — News keyword match (no numeric threshold)
{
    "threshold_type": "keyword",
    "keywords": ["recession", "bear market"],
}
```

Claude picks the right type based on the client's graph:
- Retirement goal node → pct_change on SPY
- Oil sector belief node → price_level on USO
- Inflation fear emotion node → keyword match on CPI news
- Sector concentration node → pct_change on SOXX/QQQ

---

## Full Trigger Flow

```
App starts → Claude generates triggers for all 8 clients
                        ↓
         DYNAMIC_TRIGGERS map stored in memory
                        ↓
    Polygon.io WebSocket open (price triggers)
    Alpaca/Benzinga stream open (news triggers)
                        ↓
         S&P drops 3.2% at 2:14pm
                        ↓
    match_event_to_clients() runs
    → John M. matched (pct_change -3.0 threshold)
    → Carol & Jim matched (retirement goal, 3yr remaining)
                        ↓
    For each matched client:
    [Market event] + [Client graph context] + [Advisor persona]
    → Claude generates personalized outreach draft
                        ↓
    Advisor dashboard: "3 clients need attention. Drafts ready."
```

---

## Production Architecture (Phase 4)

```python
# Swap Alpaca → FactSet, same trigger logic
import factset

factset_client = factset.ApiClient(
    factset.Configuration(username="RJ_API_USER", password="RJ_API_KEY")
)

prices_api = factset.PricesApi(factset_client)   # real-time price stream
news_api   = factset.NewsApi(factset_client)      # news wire feed

# FactSet API docs: https://developer.factset.com
```

The trigger engine is data-source agnostic — swapping FactSet in for
production requires changing only the data source layer, not the graph
matching or alert generation logic.

---

## One Line for the Submission

> "Market monitoring uses Polygon.io WebSockets (POC) connecting to FactSet
> in production — Raymond James's existing market data platform across 7,500
> advisor workstations. Trigger conditions are not hardcoded: Claude reads each
> client's memory graph and generates what market events matter specifically to
> that client. When a trigger fires, the graph matches affected clients and
> generates a personalized outreach draft in the advisor's voice before the
> market closes."

---

## References

- Raymond James selects FactSet (verified):
  https://www.globenewswire.com/news-release/2022/08/17/2499935/7768/en/Raymond-James-Selects-FactSet-as-the-Market-Data-Provider-for-U.S.-Financial-Advisors.html
- FactSet official press release:
  https://investor.factset.com/news-releases/news-release-details/raymond-james-selects-factset-market-data-provider-us-financial
- Polygon.io WebSocket docs:
  https://polygon.io/docs/websocket/stocks
- Alpaca real-time news stream:
  https://docs.alpaca.markets/us/docs/streaming-real-time-news
- FactSet developer API:
  https://developer.factset.com
