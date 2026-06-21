# Data Privacy & Compliance — How Large Firms Cleared This Blocker
### RJ MemoryAlpha · Raymond James Engineering Challenge 2026

---

## How Large Financial Firms Solved the AI Data Privacy Problem

Three proven patterns used by the biggest firms. All three available to Raymond James today.

---

## Pattern 1 — Private Deployment Behind the Firewall
**Used by: Goldman Sachs, JPMorgan, Morgan Stanley**

The model runs inside the firm's own infrastructure. No data leaves the network.

**Goldman Sachs — GS AI Assistant**
LLMs are "firewalled within Goldman, eliminating the threat that sensitive data
could escape." Rolled out to all 46,500 employees with a governance platform
covering audit trails, data lineage, and GDPR compliance.
Source: https://fortune.com/2025/06/24/goldman-sachs-internal-ai-assistant/

**JPMorgan — LLM Suite**
Built entirely in-house over two years. Model-agnostic — integrates Claude,
GPT-4, and others — all running inside JPMorgan's private cloud. 230,000+
employees. Generates $1.5 billion in annual business value. The explicit reason
for building internally: "how to harness AI capabilities without exposing
sensitive firm and client data to public models."
Source: https://thedigitalbanker.com/jpmorgan-chases-llm-suite-drives-ai-transformation-across-the-enterprise/

**Morgan Stanley — AI @ Morgan Stanley Assistant**
Partnered with OpenAI but hosted privately on Morgan Stanley's own
infrastructure. OpenAI's zero data retention policy was the compliance unlock —
data is processed but never stored on OpenAI's servers. 98% advisor adoption.
35% improvement in client engagement.
Source: https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch

---

## Pattern 2 — Cloud Provider with Financial Compliance Certifications
**Used by: Mid-size banks, regional brokers, wealth management firms**

Instead of building their own infrastructure, firms use AWS Bedrock or
Azure OpenAI Service — both carry the certifications regulators require.

| Certification  | AWS Bedrock | What it means                              |
|----------------|-------------|--------------------------------------------|
| SOC 2 Type II  | ✓           | Audited security controls                  |
| HIPAA eligible | ✓           | Highest bar for sensitive personal data    |
| FedRAMP High   | ✓           | Cleared for US government-level data       |
| ISO 27001      | ✓           | International security standard            |
| GDPR           | ✓           | European data protection                   |

**Key guarantee: prompts and responses never leave the AWS VPC.
AWS does not use your inputs to train any model.**

Raymond James already runs AWS infrastructure — confirmed by active job postings
for Senior AWS Cloud Engineers in St. Petersburg, FL. Bedrock is not a new
vendor. It is a new service on infrastructure RJ already operates.

Verify: https://aws.amazon.com/bedrock/security-compliance/
Claude on Bedrock: https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock

---

## Pattern 3 — Send Metadata, Not PII
**Used by all firms as a universal safeguard**

Every firm — even those with private deployments — applies this rule:
the AI never sees raw client data. It sees an abstracted representation.

```
WHAT GETS SENT TO THE AI:
✓ Portfolio drift percentage        e.g. "+8.0% above 7% target"
✓ Behavioral pattern label          e.g. "Accepted rebalancing 3 times"
✓ Goal timeline                     e.g. "4 years to retirement"
✓ Risk score                        e.g. "Conservative (3/10)"
✓ Life event flag                   e.g. "Spouse retired Jan 2026"

WHAT NEVER GETS SENT:
✗ Account numbers
✗ Social Security numbers
✗ Full legal names in sensitive context
✗ Raw transaction records
✗ Wire transfer details
✗ Tax information
```

RJ MemoryAlpha follows this pattern by design — the graph sends structured
behavioral metadata, not raw account data. The graph is already an
abstraction layer.

---

## The Compliance Bill Is Coming Due for Everyone

A 2025 industry analysis found that firms that did not build governance
infrastructure in 2024–2025 are now facing retroactive compliance costs
significantly higher than firms that built it correctly from the start.

The SEC fined over $2 billion across 100+ firms since 2021 for AI-related
recordkeeping failures. Every major bank is now building the governance
layer first, not after.

Source: https://convergences.substack.com/p/the-compliance-bill-for-ai-in-asset
Source: https://www.smarsh.com/regulations/sec-rule-17a-4-records-preservation/

---

## Recommended Path for Raymond James

| Phase | Approach | Time |
|---|---|---|
| POC (now) | Direct Claude API, synthetic data only | Done |
| Pilot (10 advisors) | Claude via AWS Bedrock, metadata only, zero data retention | 4–6 weeks |
| Production | Bedrock or private deployment, RJ InfoSec sign-off | Phase 4 |

---

## One Line for the Submission

> "Morgan Stanley solved this with OpenAI's zero data retention policy and
> private hosting — achieving 98% advisor adoption. JPMorgan solved it by
> building LLM Suite in-house behind their firewall. RJ MemoryAlpha takes
> the fastest path to the same outcome: Claude via Amazon Bedrock, which
> keeps all data within the AWS VPC, carries SOC 2, HIPAA, and FedRAMP High
> certifications, and runs on infrastructure Raymond James already operates."

---

## References

- Goldman Sachs GS AI firewalled deployment:
  https://fortune.com/2025/06/24/goldman-sachs-internal-ai-assistant/
- JPMorgan LLM Suite $1.5B business value:
  https://thedigitalbanker.com/jpmorgan-chases-llm-suite-drives-ai-transformation-across-the-enterprise/
- Morgan Stanley 98% advisor adoption:
  https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch
- AWS Bedrock security and compliance certifications:
  https://aws.amazon.com/bedrock/security-compliance/
- Claude on Amazon Bedrock:
  https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock
- SEC $2B in recordkeeping fines:
  https://www.smarsh.com/regulations/sec-rule-17a-4-records-preservation/
- The compliance bill for AI in asset management:
  https://convergences.substack.com/p/the-compliance-bill-for-ai-in-asset
- Big banks ease security worries as AI accelerates:
  https://www.bankingdive.com/news/banks-ai-push-accelerates-jpmorgan-stanley-citi-bny-goldman-security-worries/817923/
