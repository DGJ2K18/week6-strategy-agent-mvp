# Demo Script

## Opening

This is the Week 6 Strategy Agent MVP. The goal is to demonstrate an interoperable multi-agent system that can ingest public or consented user context, generate high-level profiles, and select broad social engineering risk strategies for defensive research.

## Step 1: Pipeline Overview

The app starts with a three-user sample dataset. Each profile represents public or consented professional context. The pipeline overview shows how each participant flows through the three agents.

## Step 2: Reconnaissance Agent

The Recon Agent extracts visible public signals such as organizations, roles, interests, and influence-related keywords. This agent does not infer intent. It only organizes observable context.

## Step 3: Profiling Agent

The Profiling Agent converts those signals into possible motivations, trust signals, and social engineering touchpoints. This creates a high-level risk profile without making sensitive or definitive claims about the person.

## Step 4: Strategy Agent

The Strategy Agent ranks broad influence strategies such as authority, opportunity, curiosity, urgency, reciprocity, and professional relevance. Importantly, it does not generate phishing messages. It only produces safe message concepts and defensive controls.

## Step 5: Output Export

The final table can be downloaded as a CSV, which can support later analysis, validation, or conference demonstrations.

## Closing

This MVP demonstrates agent independence: Recon extracts signals, Profiling interprets them, and Strategy chooses broad defensive simulation strategies. This separation helps avoid conflating a single centralized system with a multi-agent architecture.