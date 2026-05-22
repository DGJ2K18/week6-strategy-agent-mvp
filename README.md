# Week 6 Strategy Agent MVP

## Objective

This project implements a safe Week 6 prototype for a multi-agent system:

1. **Reconnaissance Agent**: organizes public/contextual signals such as organization, role, interests, and visible professional activity.
2. **Profiling Agent**: builds a high-level profile of possible motivations, trust signals, and social engineering touchpoints.
3. **Strategy Agent**: selects broad influence strategies such as urgency, authority, curiosity, opportunity, reciprocity, and professional relevance.

The prototype is designed for research demonstration and does **not** generate phishing messages, malicious payloads, credential-harvesting flows, or operational attack instructions.

## Safety Boundary

The Strategy Agent only returns:

- High-level influence strategy categories
- Risk-modeling rationale
- Safe message concepts for simulation planning
- Defensive controls and verification behaviors

It intentionally avoids generating real phishing text or step-by-step attack execution details.

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to Deploy

The easiest deployment path is Streamlit Community Cloud:

1. Push this folder to a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Select the repository.
4. Set the main file path to `app.py`.
5. Deploy.

## Demo Flow

Use the **Sample 3-user dataset** mode to show that the system can process at least three participant profiles.

Suggested demo sequence:

1. Open the app.
2. Select **Sample 3-user dataset**.
3. Show the **Pipeline Overview** tab.
4. Open the **Recon Agent** tab and explain extracted signals.
5. Open the **Profiling Agent** tab and explain motivations, trust signals, and touchpoints.
6. Open the **Strategy Agent** tab and show ranked strategy recommendations.
7. Download the CSV output.

## Files

- `app.py`: Streamlit web application.
- `data/sample_profiles.csv`: Three sample/consented participant profiles.
- `requirements.txt`: Python dependencies.
- `docs/demo_script.md`: Brief presentation script.
- `docs/architecture.md`: Explanation of the multi-agent architecture.

## Research Positioning

This MVP demonstrates independence among agents rather than presenting a single centralized system as a multi-agent system:

- The Recon Agent extracts signals.
- The Profiling Agent interprets those signals.
- The Strategy Agent makes a separate strategy-selection decision using outputs from the earlier agents.

This supports the manuscript argument that the system can be decomposed into interoperable but distinct agent capabilities.