"""
Week 6 Multi-Agent Strategy MVP
Author: Daniel George

Purpose:
A safe research prototype for demonstrating independent Reconnaissance,
Profiling, and Strategy agents for AI-enabled social engineering risk analysis.

Important safety boundary:
This application does NOT generate phishing emails, payloads, scripts, or operational
attack instructions. The Strategy agent only returns high-level influence categories,
risk rationale, and defensive controls for research and education.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse

import pandas as pd
import streamlit as st

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    requests = None
    BeautifulSoup = None


INFLUENCE_PATTERNS = {
    "authority": [
        "manager", "director", "professor", "founder", "vp", "president",
        "security", "compliance", "audit", "risk", "governance", "policy"
    ],
    "professional_relevance": [
        "sap", "workday", "ey", "consulting", "internship", "research", "ai",
        "cybersecurity", "phishing", "enterprise", "data", "analytics", "product",
        "strategy", "business", "school", "university", "career"
    ],
    "opportunity": [
        "job", "hiring", "role", "interview", "application", "fellowship",
        "conference", "grant", "scholarship", "hackathon", "certificate"
    ],
    "curiosity": [
        "new", "launch", "demo", "prototype", "innovation", "agent", "generative",
        "pilot", "research", "experiment"
    ],
    "urgency": [
        "deadline", "due", "today", "tomorrow", "urgent", "immediate",
        "finalize", "sign", "offer", "approval", "compliance"
    ],
    "reciprocity": [
        "thank", "appreciate", "mentor", "help", "support", "feedback",
        "referral", "recommendation", "collaboration"
    ],
}

DEFENSIVE_CONTROLS = {
    "authority": [
        "Verify requests through a second channel before taking action.",
        "Check sender identity, domain, and internal directory details.",
        "Avoid acting only because a request appears to come from a senior person."
    ],
    "professional_relevance": [
        "Treat highly personalized career or work messages as higher risk.",
        "Validate links through official portals instead of embedded URLs.",
        "Compare message details against known legitimate timelines and contacts."
    ],
    "opportunity": [
        "Confirm opportunities directly with the organization or recruiter.",
        "Be cautious of forms requesting credentials, payments, or sensitive documents.",
        "Use official applicant portals for job or scholarship actions."
    ],
    "curiosity": [
        "Avoid opening unsolicited demos, prototypes, or attachments.",
        "Run unknown files or links only in approved sandbox environments.",
        "Ask whether the sender has a legitimate reason to share the item."
    ],
    "urgency": [
        "Pause and independently verify time-sensitive requests.",
        "Escalate suspicious urgent messages to security or a trusted contact.",
        "Do not bypass normal controls because of artificial deadlines."
    ],
    "reciprocity": [
        "Do not let gratitude or relationship pressure override verification.",
        "Validate requests for introductions, referrals, or document sharing.",
        "Limit the information shared in response to informal favors."
    ],
}


@dataclass
class ReconFinding:
    name: str
    source_type: str
    raw_text: str
    organizations: List[str]
    roles: List[str]
    interests: List[str]
    signals: Dict[str, int]


@dataclass
class VictimProfile:
    name: str
    possible_motivations: List[str]
    trust_signals: List[str]
    social_engineering_touchpoints: List[str]
    risk_summary: str


@dataclass
class StrategyRecommendation:
    name: str
    strategy: str
    confidence: float
    rationale: str
    safe_message_concept: str
    defensive_controls: List[str]


class ReconnaissanceAgent:
    """Collects and organizes public/contextual signals from text or a URL."""

    ORG_HINTS = [
        "SAP", "SAP Concur", "EY", "Indiana University", "Kelley", "USAII",
        "McKinsey", "Deloitte", "Workday", "Microsoft", "Google", "AWS",
        "Fortinet", "NIST", "IU", "Bloomington", "Alpharetta"
    ]

    ROLE_HINTS = [
        "student", "intern", "consultant", "analyst", "research assistant",
        "professor", "manager", "director", "recruiter", "engineer",
        "founder", "president", "vice president", "global vice president"
    ]

    INTEREST_HINTS = [
        "AI", "cybersecurity", "phishing", "SAP", "Workday", "digital risk",
        "audit", "strategy", "data analytics", "consulting", "research",
        "enterprise systems", "hackathon", "product marketing", "cloud"
    ]

    def from_text(self, name: str, text: str, source_type: str = "manual_text") -> ReconFinding:
        cleaned = clean_text(text)
        lower = cleaned.lower()

        organizations = sorted({x for x in self.ORG_HINTS if x.lower() in lower})
        roles = sorted({x for x in self.ROLE_HINTS if x.lower() in lower})
        interests = sorted({x for x in self.INTEREST_HINTS if x.lower() in lower})

        signals = {}
        for strategy, terms in INFLUENCE_PATTERNS.items():
            signals[strategy] = sum(lower.count(term.lower()) for term in terms)

        return ReconFinding(
            name=name.strip() or "Unknown user",
            source_type=source_type,
            raw_text=cleaned,
            organizations=organizations,
            roles=roles,
            interests=interests,
            signals=signals,
        )

    def from_url(self, name: str, url: str) -> Tuple[Optional[ReconFinding], Optional[str]]:
        if requests is None or BeautifulSoup is None:
            return None, "URL scraping dependencies are not installed. Install requests and beautifulsoup4."

        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return None, "Only http/https URLs are supported."

        try:
            headers = {
                "User-Agent": "Week6ResearchMVP/1.0 educational defensive research prototype"
            }
            response = requests.get(url, timeout=8, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ")
            return self.from_text(name, text, source_type=f"url:{parsed.netloc}"), None
        except Exception as exc:
            return None, f"Could not retrieve URL: {exc}"


class ProfilingAgent:
    """Transforms recon signals into a high-level risk profile."""

    def build_profile(self, finding: ReconFinding) -> VictimProfile:
        text = finding.raw_text.lower()
        motivations = []
        trust_signals = []
        touchpoints = []

        if any(x in text for x in ["job", "interview", "offer", "internship", "application", "recruiter"]):
            motivations.append("Career progress and recruiting outcomes")
            touchpoints.append("Recruiter or hiring-manager communication")
        if any(x in text for x in ["research", "paper", "professor", "university", "conference"]):
            motivations.append("Academic progress and research credibility")
            touchpoints.append("Research collaboration or publication-related message")
        if any(x in text for x in ["sap", "workday", "enterprise", "data", "analytics", "product"]):
            motivations.append("Enterprise technology and business problem solving")
            touchpoints.append("Product, data, or enterprise systems update")
        if any(x in text for x in ["cybersecurity", "phishing", "security", "risk", "audit", "compliance"]):
            motivations.append("Security, compliance, and risk-oriented work")
            touchpoints.append("Security advisory, assessment, or compliance request")
        if any(x in text for x in ["mentor", "thank", "feedback", "support", "recommend"]):
            trust_signals.append("Existing mentorship or professional relationship")
            touchpoints.append("Thank-you, feedback, or referral-style interaction")

        if finding.organizations:
            trust_signals.append("Named organizations: " + ", ".join(finding.organizations[:6]))
        if finding.roles:
            trust_signals.append("Role cues: " + ", ".join(finding.roles[:6]))
        if finding.interests:
            trust_signals.append("Interest cues: " + ", ".join(finding.interests[:8]))

        motivations = dedupe(motivations) or ["Professional relevance and information-seeking"]
        trust_signals = dedupe(trust_signals) or ["Publicly visible professional context"]
        touchpoints = dedupe(touchpoints) or ["Generic professional outreach"]

        risk_summary = (
            "The profile suggests potential susceptibility to messages that align with "
            f"{', '.join(motivations[:2]).lower()}, especially when the message appears "
            "professionally relevant and comes from a trusted or familiar context."
        )

        return VictimProfile(
            name=finding.name,
            possible_motivations=motivations,
            trust_signals=trust_signals,
            social_engineering_touchpoints=touchpoints,
            risk_summary=risk_summary,
        )


class StrategyAgent:
    """Chooses broad influence strategies and defensive mitigations."""

    def recommend(self, finding: ReconFinding, profile: VictimProfile, top_n: int = 3) -> List[StrategyRecommendation]:
        raw_scores = finding.signals.copy()

        # Add profile-based boosts.
        joined_profile = " ".join(
            profile.possible_motivations + profile.trust_signals + profile.social_engineering_touchpoints
        ).lower()

        if "career" in joined_profile or "recruit" in joined_profile:
            raw_scores["opportunity"] += 4
            raw_scores["professional_relevance"] += 2
        if "research" in joined_profile or "academic" in joined_profile:
            raw_scores["curiosity"] += 2
            raw_scores["professional_relevance"] += 2
        if "security" in joined_profile or "compliance" in joined_profile:
            raw_scores["authority"] += 2
            raw_scores["professional_relevance"] += 2
        if "deadline" in finding.raw_text.lower() or "finalize" in finding.raw_text.lower():
            raw_scores["urgency"] += 3
        if "mentor" in joined_profile or "relationship" in joined_profile:
            raw_scores["reciprocity"] += 3

        total = max(sum(raw_scores.values()), 1)
        ranked = sorted(raw_scores.items(), key=lambda x: x[1], reverse=True)

        recs = []
        for strategy, score in ranked[:top_n]:
            confidence = round(min(0.95, 0.35 + (score / total)), 2)
            recs.append(
                StrategyRecommendation(
                    name=finding.name,
                    strategy=strategy.replace("_", " ").title(),
                    confidence=confidence,
                    rationale=make_rationale(strategy, finding, profile),
                    safe_message_concept=make_safe_concept(strategy),
                    defensive_controls=DEFENSIVE_CONTROLS[strategy],
                )
            )
        return recs


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:12000]


def dedupe(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def make_rationale(strategy: str, finding: ReconFinding, profile: VictimProfile) -> str:
    evidence = []
    if finding.organizations:
        evidence.append("organization references")
    if finding.roles:
        evidence.append("role cues")
    if finding.interests:
        evidence.append("interest signals")
    if profile.possible_motivations:
        evidence.append("profiled motivations")
    evidence_text = ", ".join(evidence) if evidence else "available public context"

    readable = strategy.replace("_", " ")
    return (
        f"The {readable} strategy ranked highly because the Recon and Profiling agents "
        f"identified {evidence_text}. This is a risk-modeling recommendation only, not "
        "an instruction to contact or deceive the individual."
    )


def make_safe_concept(strategy: str) -> str:
    concepts = {
        "authority": "Simulate a message theme that appears to come from a trusted institution or senior role; evaluate verification behavior.",
        "professional_relevance": "Simulate a theme aligned to the person’s work or study interests; evaluate whether personalization increases trust.",
        "opportunity": "Simulate a career or learning opportunity theme; evaluate whether opportunity framing changes risk perception.",
        "curiosity": "Simulate a novelty or demo-oriented theme; evaluate whether curiosity leads to unsafe link or attachment behavior.",
        "urgency": "Simulate a time-sensitive theme; evaluate whether urgency causes users to bypass normal verification.",
        "reciprocity": "Simulate a relationship or favor-based theme; evaluate whether social obligation changes response behavior.",
    }
    return concepts[strategy]


def load_sample_data() -> pd.DataFrame:
    return pd.read_csv("data/sample_profiles.csv")


def run_pipeline(df: pd.DataFrame) -> Tuple[List[ReconFinding], List[VictimProfile], List[StrategyRecommendation]]:
    recon = ReconnaissanceAgent()
    profiler = ProfilingAgent()
    strategist = StrategyAgent()

    findings: List[ReconFinding] = []
    profiles: List[VictimProfile] = []
    all_recs: List[StrategyRecommendation] = []

    for _, row in df.iterrows():
        finding = recon.from_text(str(row["name"]), str(row["public_context"]), source_type=str(row.get("source_type", "sample")))
        profile = profiler.build_profile(finding)
        recs = strategist.recommend(finding, profile, top_n=3)

        findings.append(finding)
        profiles.append(profile)
        all_recs.extend(recs)

    return findings, profiles, all_recs


st.set_page_config(page_title="Week 6 Strategy Agent MVP", layout="wide")

st.title("Week 6 Multi-Agent Strategy MVP")
st.caption("Reconnaissance → Profiling → Strategy Selection | Safe research prototype")

st.warning(
    "Safety boundary: this system produces high-level social engineering risk strategies and defensive controls only. "
    "It does not generate phishing messages, payloads, credential-harvesting instructions, or attack execution steps."
)

with st.sidebar:
    st.header("Input Mode")
    mode = st.radio("Choose data source", ["Sample 3-user dataset", "Manual public-context text", "Public URL demo"])
    st.divider()
    st.markdown("**Agents shown independently:**")
    st.markdown("1. Reconnaissance Agent\n2. Profiling Agent\n3. Strategy Agent")
    st.divider()
    st.markdown("Use only public, consented, or synthetic data for research demonstrations.")

if mode == "Sample 3-user dataset":
    df = load_sample_data()
elif mode == "Manual public-context text":
    name = st.text_input("Person / participant label", value="Participant A")
    text = st.text_area(
        "Paste public or consented context",
        height=220,
        value="Graduate student interested in AI, cybersecurity, SAP, digital risk consulting, research, and career opportunities."
    )
    df = pd.DataFrame([{"name": name, "source_type": "manual", "public_context": text}])
else:
    st.info(
        "The URL demo attempts to retrieve public page text when deployed with internet access. "
        "For local demos without internet, use the sample dataset."
    )
    name = st.text_input("Person / participant label", value="URL Participant")
    url = st.text_input("Public URL", value="")
    scrape_clicked = st.button("Run URL Recon")
    df = pd.DataFrame(columns=["name", "source_type", "public_context"])

    if scrape_clicked and url:
        recon = ReconnaissanceAgent()
        finding, error = recon.from_url(name, url)
        if error:
            st.error(error)
        else:
            df = pd.DataFrame([{
                "name": name,
                "source_type": finding.source_type,
                "public_context": finding.raw_text
            }])

if len(df) > 0:
    findings, profiles, all_recs = run_pipeline(df)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Pipeline Overview", "Recon Agent", "Profiling Agent", "Strategy Agent"
    ])

    with tab1:
        st.subheader("Multi-Agent Pipeline")
        st.markdown(
            """
            This MVP demonstrates three independent agents:
            - **Reconnaissance Agent:** extracts public/contextual signals.
            - **Profiling Agent:** converts signals into possible motivations and touchpoints.
            - **Strategy Agent:** selects broad influence strategies and defensive controls.
            """
        )
        overview = []
        for finding, profile in zip(findings, profiles):
            top = [r.strategy for r in all_recs if r.name == finding.name][:3]
            overview.append({
                "Participant": finding.name,
                "Source": finding.source_type,
                "Organizations": ", ".join(finding.organizations) or "Not detected",
                "Interests": ", ".join(finding.interests) or "Not detected",
                "Top Strategies": ", ".join(top),
                "Risk Summary": profile.risk_summary,
            })
        st.dataframe(pd.DataFrame(overview), use_container_width=True)

    with tab2:
        st.subheader("Reconnaissance Agent Output")
        for f in findings:
            with st.expander(f"{f.name} — Recon Findings", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.write("**Organizations**")
                c1.write(f.organizations or "None detected")
                c2.write("**Roles**")
                c2.write(f.roles or "None detected")
                c3.write("**Interests**")
                c3.write(f.interests or "None detected")
                st.write("**Influence Signal Counts**")
                st.json(f.signals)
                st.write("**Source Text Preview**")
                st.write(f.raw_text[:1200] + ("..." if len(f.raw_text) > 1200 else ""))

    with tab3:
        st.subheader("Profiling Agent Output")
        for p in profiles:
            with st.expander(f"{p.name} — High-Level Profile", expanded=True):
                st.write("**Possible Motivations**")
                st.write(p.possible_motivations)
                st.write("**Trust Signals**")
                st.write(p.trust_signals)
                st.write("**Social Engineering Touchpoints**")
                st.write(p.social_engineering_touchpoints)
                st.write("**Risk Summary**")
                st.write(p.risk_summary)

    with tab4:
        st.subheader("Strategy Agent Output")
        rec_df = pd.DataFrame([asdict(r) for r in all_recs])
        rec_df["defensive_controls"] = rec_df["defensive_controls"].apply(lambda x: "\n".join(x))
        st.dataframe(rec_df, use_container_width=True)

        st.markdown("### Detailed Recommendations")
        for r in all_recs:
            with st.expander(f"{r.name} — {r.strategy} ({r.confidence})"):
                st.write("**Rationale**")
                st.write(r.rationale)
                st.write("**Safe Message Concept**")
                st.write(r.safe_message_concept)
                st.write("**Defensive Controls**")
                for control in r.defensive_controls:
                    st.markdown(f"- {control}")

        csv = rec_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download strategy output CSV", csv, "week6_strategy_agent_output.csv", "text/csv")
else:
    st.info("Choose or enter data to run the pipeline.")