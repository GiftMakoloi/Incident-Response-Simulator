# Incident Response Simulator

An interactive, scenario-based decision-making engine built with Streamlit. Designed for junior security analysts, Incident Response (IR) learners, and SOC teams to practice real-time triage and tactical decision-making during simulated cyber attacks.

## Overview

Theoretical cybersecurity knowledge often fails to prepare junior analysts for the high-pressure decision-making required during an active breach. Choosing the wrong remediation step early in an incident can lead to network-wide malware propagation or evidentiary destruction.

The Incident Response Simulator provides a sandboxed environment where users navigate branching incident scenarios. Every decision dynamically impacts operational metrics such as system infection rates, downtime costs, and containment progress, culminating in an After-Action Review (AAR).

## Key Features

*   Branching Decision Engine: Scenario paths that adapt dynamically based on user choices.
*   Real-Time Impact Metrics: Persistent session tracking for infection spread, financial/operational cost, and time elapsed.
*   Multiple Incident Scenarios: Built-in scenarios covering Ransomware Outbreaks, Credential Harvesting, and Insider Threats.
*   After-Action Review (AAR): Automated summary report breaking down decision efficiency, methodology errors, and recommended remediation protocols.

## Tech Stack

*   Python
*   Streamlit

## Quickstart

1. Clone the repository:
   git clone https://github.com/yourusername/incident-response-simulator.git
   cd incident-response-simulator

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   streamlit run app.py

## License
MIT License
