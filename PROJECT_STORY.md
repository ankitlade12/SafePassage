# SafePassage Project Story

## Inspiration

The idea for SafePassage was born from a simple but terrifying question: What happens to your money when the world falls apart?

In 2024, we've witnessed countless crises unfold at unprecedented speed—civil unrest, natural disasters, banking collapses, and geopolitical instability. We noticed a critical gap: while there are apps for travel safety advisories and emergency SOS services, no one was solving the financial liquidity crisis that strands millions of travelers, expats, and aid workers when traditional banking infrastructure fails.

Consider these real scenarios:
- ATMs run dry during bank runs
- Wire transfers take 3-5 business days while borders close in hours
- Credit cards get blocked by fraud algorithms precisely when you need them most
- Mobile networks go offline, cutting access to digital wallets

We asked ourselves: "In a crisis that moves faster than a bank wire, how do we ensure your money isn't trapped with the failing infrastructure?"

That question became SafePassage—a Tactical Financial Resiliency System that keeps your exit funds accessible when everything else fails.

---

## What It Does

SafePassage is the "Waze for Money" in a crisis. Just like Waze reroutes you around traffic, SafePassage automatically reroutes your emergency funds through the only financial pathways still working.

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Liquidity Oracle** | AI-powered algorithm that ranks payout methods (crypto, wire, cash pickup, mobile money) based on real-time network conditions |
| **$5,000 Exit Vault** | Pre-funded emergency reserve verified on-chain, ready to deploy instantly |
| **Real-Time Risk Monitoring** | Integration with live GDELT (political events), USGS (earthquakes), and State Department (travel advisories) data |
| **Dead Man's Switch** | Timer-based check-in system that auto-triggers payout to your fallback destination if you go dark |
| **Guardian Network** | Multi-sig safety net with trusted contacts who get notified when risk exceeds critical thresholds |
| **Shadow Banking Mode** | Offline QR code system for redeeming funds at realistic partner networks when internet/banks fail |
| **Crisis Packet** | Dynamic, location-aware emergency phrases and situational status reports for local authorities |

### The Magic Formula

The SafePassage Score is calculated using a dynamic weighting system:
- **Crisis Mode (Risk >= 7):** Speed = 0.50, Reliability = 0.40, Cost = 0.10
- **Normal Mode:** Speed = 0.30, Reliability = 0.30, Cost = 0.40

---

## How We Built It

### Tech Stack

We chose technologies optimized for rapid development and real-world reliability:

- **Frontend:** Streamlit 1.37+ for interactive, real-time dashboards
- **Backend:** Python 3.11 for robust risk monitoring and payout orchestration
- **Visualization:** Plotly for risk gauges, Sankey diagrams, and interactive maps
- **Data Sources:** GDELT API, USGS Earthquake API, State Department Travel Advisories
- **Package Management:** uv for lightning-fast dependency resolution

### Architecture Philosophy

We designed SafePassage with a modular, event-driven architecture:

1. **Real-Time Monitoring:** GDELT, USGS, and State Department signals are fused into a unified Risk Monitor (Score 0-10).
2. **Liquidity Oracle:** The monitor feeds into the Oracle, which checks network status and ranks payout methods.
3. **Emergency Activation:** Based on user selection or automated triggers, the Payout Orchestrator executes the transaction and provides confirmation.

### Key Implementation Details

1. **Risk Score Fusion:** We combine signals from three independent data sources, normalizing them into a unified 0-10 risk scale with configurable weights.
2. **Realistic Network Status:** We modeled how different payment rails degrade as crisis levels increase—traditional banking and ATMs go offline first, while crypto remains resilient.
3. **Chaos Simulator:** A unique testing tool that lets users simulate any crisis level and see exactly how SafePassage responds, building trust through transparency.
4. **Audit Trail with Oracle Reasoning:** Every decision is logged with the AI's reasoning, ensuring users understand why a particular payout method was recommended.

---

## Challenges We Ran Into

### 1. Data Source Reliability

**Challenge:** Free public APIs (GDELT, USGS) have rate limits and occasional downtime.
**Solution:** We implemented a robust fallback system with cached data and graceful degradation. If live data isn't available, we use the most recent cached values with a clear stale data indicator.

### 2. Simulating Network Failures Realistically

**Challenge:** How do you accurately model which payment methods fail during different crisis scenarios?
**Solution:** We researched historical crises (Venezuela banking collapse, Ukraine evacuation, Sri Lanka crisis) to build a realistic degradation matrix. Traditional traditional infrastructure is highly sensitive to security threats, while crypto rails offer greater resilience.

### 3. Balancing Speed vs. User Trust

**Challenge:** Users want instant access to funds, but also need confidence their money is secure.
**Solution:** We added Proof of Reserves (simulated on-chain verification) and a comprehensive Audit Trail. Users can see exactly where their money is and why each decision was made.

### 4. Offline Functionality

**Challenge:** If the internet is down, how do users access their funds?
**Solution:** Shadow Banking Mode generates secure QR codes that can be verified offline at partner locations. Each code is one-time-use with embedded verification data.

---

## Accomplishments That We're Proud Of

### Novel AI Application
The Liquidity Oracle is the first AI system we know of that ranks payout methods by real-time network health. It doesn't just tell you there's a problem—it actively reroutes your money through working channels.

### Dynamic Contextual Intelligence
The system now adapts its output based on your exact location. For example, a user in Kyiv receives a Crisis Packet with priority Ukrainian phrases and an authority help message pre-filled with their actual passport and emergency contact details.

### Human-Centered Safety Features
- **Dead Man's Switch:** Acknowledges that users might not be able to act in an emergency.
- **Guardian Network:** Leverages social trust for additional security.
- **Dynamic Crisis Packet:** Removes language and information barriers when minutes matter most.

### Addressing a Real Gap
No existing solution combines real-time crisis monitoring, AI-powered payout routing, offline backup options, and automated safety nets into a single, cohesive travel safety platform.

---

## What We Learned

### Technical Learnings

1. **Real-Time Data Fusion is Hard:** Combining data from multiple sources with different update frequencies and reliability levels requires careful normalization and fallback strategies.
2. **Streamlit's Power and Limits:** Streamlit is incredible for rapid prototyping, but complex state management across multiple interactive tabs requires disciplined state centralization.
3. **Visualization Matters:** Features like the Chaos Simulator and Sankey diagrams were essential for building user trust by making the "black box" of the Oracle transparent.

### Product Learnings

1. **Edge Cases Define the Product:** A crisis-response app is defined by how it handles edge cases—offline scenarios, stale data, and infrastructure failure. These are not just bugs; they are the core problem we solve.
2. **Trust Through Transparency:** Every decision the Oracle makes is logged with reasoning. This audit trail transformed a complex algorithm into a trusted travel companion.
3. **Social Features Multiply Value:** The Guardian Network creates organic security loops—users naturally invite trusted contacts, expanding their own safety net.

---

## What's Next for SafePassage

### Immediate Roadmap

- **Real Blockchain Integration:** Actual USDC on Base/Polygon instead of simulation.
- **SMS Alerts:** Twilio integration for automated Guardian and emergency notifications.
- **Satellite Connectivity:** Starlink API integration for truly offline areas.
- **Embassy Directory:** Auto-populating local embassy and consulate info based on user location.

### Vision

SafePassage is positioned to become the financial backbone of crisis response. We envision partnerships with travel insurance providers, NGOs operating in high-risk zones, and corporate travel programs to ensure that no one is ever stranded without access to their survival capital.

---

**SafePassage: When minutes matter, your money moves first.**
