import streamlit as st

st.set_page_config(page_title="Incident Response Simulator", layout="wide")

st.title("Incident Response Simulator")
st.caption("Interactive scenario engine for cybersecurity incident triage and containment training.")

# Scenario Data Structure
SCENARIOS = {
    "Ransomware Outbreak": {
        "title": "Operation DarkLock: Enterprise Ransomware Outbreak",
        "initial_description": "At 08:30 AM, the IT Helpdesk receives three urgent tickets reporting encrypted files on server FS-02. File extensions have changed to '.darklock', and a ransom note sits on the desktop.",
        "start_step": "step_1",
        "steps": {
            "step_1": {
                "situation": "Initial alert received. Server FS-02 is actively encrypting local shares. Network monitoring shows high outbound SMB traffic to subnets 10.0.2.0/24.",
                "choices": [
                    {
                        "label": "Isolate FS-02 from the network immediately via VLAN disablement.",
                        "next_step": "step_2_isolate",
                        "impact": {"time": 15, "cost": 500, "containment": 40, "spread": 0},
                        "feedback": "Correct initial containment choice. Isolating the host halts active SMB propagation across the subnet."
                    },
                    {
                        "label": "Run a full antivirus scan on FS-02 while keeping it online to collect evidence.",
                        "next_step": "step_2_scan",
                        "impact": {"time": 45, "cost": 5000, "containment": 10, "spread": 35},
                        "feedback": "Incorrect choice. Running an AV scan on an active encryption host allows malware to continue spreading to adjacent network shares."
                    },
                    {
                        "label": "Restart server FS-02 to stop running unauthorized processes.",
                        "next_step": "step_2_restart",
                        "impact": {"time": 30, "cost": 2000, "containment": 5, "spread": 20},
                        "feedback": "Poor tactical choice. Rebooting destroys critical volatile memory (RAM) evidence and does not prevent encryption on startup."
                    }
                ]
            },
            "step_2_isolate": {
                "situation": "FS-02 is isolated. Network traffic stabilizes. However, the attacker holds active domain administrator credentials used during the initial entry.",
                "choices": [
                    {
                        "label": "Force a global password reset for all Domain Administrator accounts and revoke active kerberos tickets.",
                        "next_step": "step_3_win",
                        "impact": {"time": 30, "cost": 1000, "containment": 50, "spread": 0},
                        "feedback": "Excellent decision. Revoking active domain admin tokens prevents lateral movement to backup servers."
                    },
                    {
                        "label": "Attempt to pay the ransom immediately to obtain the decryption key.",
                        "next_step": "step_3_pay",
                        "impact": {"time": 120, "cost": 50000, "containment": 0, "spread": 10},
                        "feedback": "Violation of incident policy. Ransom payment offers no guarantee of data recovery and funds further malicious operations."
                    }
                ]
            },
            "step_2_scan": {
                "situation": "The AV scan failed to stop the process. Ransomware has now spread to secondary file server FS-03 and domain controller DC-01.",
                "choices": [
                    {
                        "label": "Execute emergency network-wide disconnect and isolate all domain controllers.",
                        "next_step": "step_3_win",
                        "impact": {"time": 60, "cost": 15000, "containment": 45, "spread": 10},
                        "feedback": "Drastic but necessary measure to prevent total infrastructure compromise after initial containment failure."
                    }
                ]
            },
            "step_2_restart": {
                "situation": "Upon rebooting, ransomware service automatically executes again. Volatile memory is lost, hindering forensic analysis.",
                "choices": [
                    {
                        "label": "Sever physical network links and initiate full incident response plan escalation.",
                        "next_step": "step_3_win",
                        "impact": {"time": 45, "cost": 10000, "containment": 40, "spread": 10},
                        "feedback": "Necessary escalation. Network link disconnect stops further payload distribution."
                    }
                ]
            },
            "step_3_win": {
                "situation": "Incident contained! Malicious processes are stopped, lateral movement paths are blocked, and forensic triage is underway.",
                "choices": []
            },
            "step_3_pay": {
                "situation": "Ransom paid, but attacker provided broken decryption keys. Incident response failed.",
                "choices": []
            }
        }
    }
}

# Initialize Session State
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = "Ransomware Outbreak"
if "current_step" not in st.session_state:
    st.session_state.current_step = SCENARIOS["Ransomware Outbreak"]["start_step"]
if "history" not in st.session_state:
    st.session_state.history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {"time": 0, "cost": 0, "containment": 0, "spread": 0}

# Helper to reset state
def reset_simulation():
    scen = SCENARIOS[st.session_state.current_scenario]
    st.session_state.current_step = scen["start_step"]
    st.session_state.history = []
    st.session_state.metrics = {"time": 0, "cost": 0, "containment": 0, "spread": 0}

# Sidebar controls
st.sidebar.header("Scenario Controls")
scenario_choice = st.sidebar.selectbox("Select Incident Scenario", list(SCENARIOS.keys()))

if scenario_choice != st.session_state.current_scenario:
    st.session_state.current_scenario = scenario_choice
    reset_simulation()

if st.sidebar.button("Restart Scenario"):
    reset_simulation()

# Fetch active scenario step
scenario = SCENARIOS[st.session_state.current_scenario]
step_data = scenario["steps"][st.session_state.current_step]

# Top level metrics display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Elapsed Time (min)", f"{st.session_state.metrics['time']} mins")
col2.metric("Financial Impact ($)", f"${st.session_state.metrics['cost']:,}")
col3.metric("Containment Level", f"{st.session_state.metrics['containment']}%")
col4.metric("Infection Spread", f"{st.session_state.metrics['spread']}%")

st.divider()

# Main Scenario Interface
st.subheader(scenario["title"])
st.write(step_data["situation"])

# Check if scenario has concluded
if not step_data["choices"]:
    st.success("Scenario Completed!")
    st.header("After-Action Review (AAR)")
    
    st.write(f"**Total Time Spent:** {st.session_state.metrics['time']} minutes")
    st.write(f"**Total Estimated Financial Impact:** ${st.session_state.metrics['cost']:,}")
    st.write(f"**Final Containment Score:** {st.session_state.metrics['containment']}%")
    
    st.subheader("Decision Audit Trail")
    for idx, log in enumerate(st.session_state.history, start=1):
        with st.expander(f"Decision {idx}: {log['choice']}"):
            st.write(f"**Feedback:** {log['feedback']}")
            st.write(f"**Impact:** +{log['impact']['time']} mins, +${log['impact']['cost']} cost")
else:
    st.subheader("Select Tactical Action")
    for choice in step_data["choices"]:
        if st.button(choice["label"], key=choice["label"]):
            # Update metrics
            for key in st.session_state.metrics:
                st.session_state.metrics[key] += choice["impact"][key]
            
            # Log history
            st.session_state.history.append({
                "step": st.session_state.current_step,
                "choice": choice["label"],
                "feedback": choice["feedback"],
                "impact": choice["impact"]
            })
            
            # Advance to next step
            st.session_state.current_step = choice["next_step"]
            st.rerun()

# Display decision history in expandable tab
if st.session_state.history:
    st.divider()
    with st.expander("View Action Log"):
        for log in st.session_state.history:
            st.write(f"- **Action:** {log['choice']}")
            st.write(f"  *Note:* {log['feedback']}")
