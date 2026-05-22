# Architecture Notes

## Multi-Agent Design

The Week 6 system is intentionally decomposed into three independent agents.

## 1. Reconnaissance Agent

**Input:** Public text, consented user context, or public URL text.

**Output:**

- Organizations
- Roles
- Interests
- Influence signal counts

**Purpose:** Organizes public signals without interpreting deeper motivations.

## 2. Profiling Agent

**Input:** Recon Agent output.

**Output:**

- Possible motivations
- Trust signals
- Social engineering touchpoints
- Risk summary

**Purpose:** Converts raw public signals into a high-level behavioral risk profile.

## 3. Strategy Agent

**Input:** Recon Agent output + Profiling Agent output.

**Output:**

- Ranked influence strategies
- Confidence scores
- Safe message concepts
- Defensive controls

**Purpose:** Selects broad strategy categories for defensive simulation and research analysis.

## Strategy Categories

- Authority
- Professional relevance
- Opportunity
- Curiosity
- Urgency
- Reciprocity

## Why This Counts as Multi-Agent

Each agent has a distinct responsibility, input, and output. The Strategy Agent does not directly scrape or build the profile. It only makes a strategy-selection decision after the Recon and Profiling agents complete their independent tasks.

## Ethical Guardrails

The system is designed for academic and defensive research. It avoids:

- Real phishing text
- Credential-harvesting pages
- Malware or payload generation
- Instructions for bypassing security tools
- Operational targeting guidance

The output should be used to understand risk, evaluate training needs, and design safer awareness simulations.