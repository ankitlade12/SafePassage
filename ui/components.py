"""
UI Components and Visual Enhancements
"""

import streamlit as st
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
import json
import plotly.graph_objects as go
from typing import List

# Import models using absolute import
from models import Location, RiskAlert

# ============================================================================
# QR Code Generator
# ============================================================================


class QRCodeGenerator:
    """Generate QR codes for emergency information"""

    @staticmethod
    def generate_emergency_qr(user_profile):
        """Generate QR code with emergency contact info"""

        emergency_data = {
            "name": user_profile.name,
            "location": f"{user_profile.current_location.city}, {user_profile.current_location.country}",
            "phone": user_profile.phone if hasattr(user_profile, "phone") else "N/A",
            "emergency_contact": user_profile.exit_fund.trusted_contacts[0].phone
            if user_profile.exit_fund and user_profile.exit_fund.trusted_contacts
            else "N/A",
            "exit_fund": f"${user_profile.exit_fund.amount} {user_profile.exit_fund.currency}"
            if user_profile.exit_fund
            else "N/A",
            "fallback": user_profile.exit_fund.fallback_destinations[0].city
            if user_profile.exit_fund and user_profile.exit_fund.fallback_destinations
            else "N/A",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        qr_data = json.dumps(emergency_data, indent=2)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer

    @staticmethod
    def show_qr_widget(user_profile):
        """Display QR code widget"""
        st.subheader("📱 Emergency QR Code")
        st.write(
            "Share this QR code with trusted contacts for quick access to your emergency info"
        )

        try:
            qr_buffer = QRCodeGenerator.generate_emergency_qr(user_profile)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(qr_buffer, caption="Scan for Emergency Info")

            with col2:
                st.write("**Contains:**")
                st.write("- Your name and current location")
                st.write("- Emergency contact number")
                st.write("- Exit fund details")
                st.write("- Fallback destination")

                # Download button
                qr_buffer.seek(0)
                st.download_button(
                    label="📥 Download QR Code",
                    data=qr_buffer,
                    file_name=f"emergency_qr_{user_profile.name.replace(' ', '_')}.png",
                    mime="image/png",
                    width="stretch",
                )
        except Exception as e:
            st.error(f"Error generating QR code: {e}")


# ============================================================================
# Alert Simulator
# ============================================================================


class AlertSimulator:
    """Simulate email and SMS alerts"""

    @staticmethod
    def create_email_preview(alert_type, location, severity):
        """Create email alert preview"""

        severity_color = (
            "#d32f2f" if severity >= 7 else "#ff9800" if severity >= 4 else "#4caf50"
        )

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; border: 2px solid {severity_color}; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
            <h2 style="color: {severity_color}; margin-top: 0;">🚨 Safe-Passage Alert</h2>
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p style="margin: 5px 0;"><strong>Alert Type:</strong> {alert_type}</p>
                <p style="margin: 5px 0;"><strong>Location:</strong> {location}</p>
                <p style="margin: 5px 0;"><strong>Severity:</strong> <span style="color: {severity_color}; font-weight: bold;">{severity}/10</span></p>
                <p style="margin: 5px 0;"><strong>Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            <p>A risk alert has been detected in your area. Please review your Safe-Passage dashboard for details and consider activating your emergency protocol if necessary.</p>
            <a href="#" style="background-color: {severity_color}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 15px; font-weight: bold;">View Dashboard →</a>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #666;">Safe-Passage Emergency Liquidity System | Do not reply to this email</p>
        </div>
        """
        return html

    @staticmethod
    def create_sms_preview(alert_type, location, severity):
        """Create SMS alert preview"""
        emoji = "🔴" if severity >= 7 else "🟡" if severity >= 4 else "🟢"
        return f"{emoji} Safe-Passage Alert: {alert_type} in {location}. Severity: {severity}/10. Check dashboard: safepassage.app/dashboard"

    @staticmethod
    def show_alert_previews():
        """Show alert preview interface"""
        st.subheader("📧 Alert Notifications Preview")
        st.write("Customize and preview how you'll receive emergency alerts")

        col1, col2 = st.columns(2)

        with col1:
            alert_type = st.selectbox(
                "Alert Type",
                [
                    "Political Unrest",
                    "Natural Disaster",
                    "Payment Disruption",
                    "Security Threat",
                    "Weather Emergency",
                ],
            )
            location = st.text_input("Location", value="Dallas, USA")

        with col2:
            severity = st.slider("Severity Level", 1, 10, 7)
            notification_type = st.radio("Preview Type", ["Email", "SMS", "Both"])

        st.markdown("---")

        if notification_type in ["Email", "Both"]:
            st.markdown("### 📧 Email Preview")
            email_html = AlertSimulator.create_email_preview(
                alert_type, location, severity
            )
            st.markdown(email_html, unsafe_allow_html=True)

        if notification_type in ["SMS", "Both"]:
            st.markdown("### 📱 SMS Preview")
            sms_text = AlertSimulator.create_sms_preview(alert_type, location, severity)
            st.info(sms_text)

        st.markdown("---")

        if st.button("🧪 Send Test Alert", width="stretch"):
            st.success("✅ Test alert sent successfully! (Simulated)")
            st.balloons()


# ============================================================================
# Emergency Widget
# ============================================================================


class EmergencyWidget:
    """Quick access emergency contacts widget"""

    @staticmethod
    def show_emergency_widget(user_profile):
        """Display emergency contacts widget in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("🆘 Emergency Contacts")

        # SOS Button
        if st.sidebar.button("🚨 SOS - ACTIVATE NOW", width="stretch", type="primary"):
            st.sidebar.warning(
                "⚠️ Are you sure? This will activate your emergency protocol."
            )
            if st.sidebar.button("✅ Yes, Activate Emergency", width="stretch"):
                st.session_state.emergency_activated = True
                st.sidebar.success("Emergency activated! Go to Emergency tab.")

        # Quick dial contacts
        with st.sidebar.expander("📞 Quick Dial"):
            # Embassy
            st.write("**🏛️ U.S. Embassy**")
            st.code("+1-888-407-4747")

            # Emergency contact
            if user_profile.exit_fund and user_profile.exit_fund.trusted_contacts:
                contact = user_profile.exit_fund.trusted_contacts[0]
                st.write(f"**👤 {contact.name}**")
                st.code(contact.phone)

            # Local emergency
            st.write("**🚑 Local Emergency**")
            st.code("911 (USA)")


# ============================================================================
# Comparison Tool
# ============================================================================


class ComparisonTool:
    """Compare multiple destinations side-by-side"""

    @staticmethod
    def show_comparison_tool():
        """Display destination comparison interface"""
        st.subheader("🔄 Compare Destinations")
        st.write("Compare risk levels and costs for multiple destinations")

        # Select destinations
        col1, col2, col3 = st.columns(3)

        destinations = []

        with col1:
            st.markdown("### Destination 1")
            city1 = st.text_input("City", value="Mumbai", key="comp_city1")
            country1 = st.text_input("Country", value="India", key="comp_country1")
            if city1 and country1:
                destinations.append((city1, country1))

        with col2:
            st.markdown("### Destination 2")
            city2 = st.text_input("City", value="Tokyo", key="comp_city2")
            country2 = st.text_input("Country", value="Japan", key="comp_country2")
            if city2 and country2:
                destinations.append((city2, country2))

        with col3:
            st.markdown("### Destination 3")
            city3 = st.text_input("City", value="London", key="comp_city3")
            country3 = st.text_input("Country", value="UK", key="comp_country3")
            if city3 and country3:
                destinations.append((city3, country3))

        if st.button("📊 Compare All", width="stretch") and len(destinations) >= 2:
            # Import TripPlanner here to avoid circular dependencies if possible,
            # or ensure structure supports it.
            from ui.dashboard import TripPlanner
            from models import Location

            st.markdown("---")
            st.markdown("### 📊 Comparison Results")

            # Create comparison table
            comparison_data = {
                "Destination": [],
                "Overall Risk": [],
                "Political": [],
                "Healthcare": [],
                "Payment": [],
                "Recommendation": [],
            }

            for city, country in destinations:
                loc = Location(city, country, 0, 0)
                risk = TripPlanner.assess_destination_risk(loc)

                comparison_data["Destination"].append(f"{city}, {country}")
                comparison_data["Overall Risk"].append(f"{risk['overall_risk']}/10")
                comparison_data["Political"].append(f"{risk['political_stability']}/10")
                comparison_data["Healthcare"].append(f"{risk['healthcare_quality']}/10")
                comparison_data["Payment"].append(
                    f"{risk['payment_infrastructure']}/10"
                )

                if risk["overall_risk"] >= 7:
                    comparison_data["Recommendation"].append("🔴 High Risk")
                elif risk["overall_risk"] >= 4:
                    comparison_data["Recommendation"].append("🟡 Moderate")
                else:
                    comparison_data["Recommendation"].append("🟢 Low Risk")

            st.dataframe(comparison_data, width="stretch")

            # Best/worst
            risks = [
                TripPlanner.assess_destination_risk(Location(c, co, 0, 0))[
                    "overall_risk"
                ]
                for c, co in destinations
            ]
            best_idx = risks.index(min(risks))
            worst_idx = risks.index(max(risks))

            col1, col2 = st.columns(2)
            with col1:
                st.success(
                    f"✅ **Safest:** {destinations[best_idx][0]}, {destinations[best_idx][1]}"
                )
            with col2:
                st.error(
                    f"⚠️ **Highest Risk:** {destinations[worst_idx][0]}, {destinations[worst_idx][1]}"
                )


# ============================================================================
# Visual Enhancements
# ============================================================================


def create_risk_gauge(risk_level: int) -> go.Figure:
    """Create speedometer-style risk gauge"""

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_level,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Risk Level", "font": {"size": 24}},
            gauge={
                "axis": {"range": [None, 10], "tickwidth": 1, "tickcolor": "darkgray"},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 3], "color": "#d4edda"},
                    {"range": [3, 5], "color": "#fff3cd"},
                    {"range": [5, 7], "color": "#f8d7da"},
                    {"range": [7, 10], "color": "#f5c6cb"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 7,
                },
            },
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "darkgray", "family": "Arial"},
    )

    return fig


def create_location_map(
    current_location: Location,
    fallback_location: Location = None,
    alerts: List[RiskAlert] = None,
) -> go.Figure:
    """Create interactive map with location markers"""

    # Create map
    fig = go.Figure()

    # Add current location
    fig.add_trace(
        go.Scattergeo(
            lon=[current_location.longitude],
            lat=[current_location.latitude],
            text=[f"📍 Current: {current_location.city}"],
            mode="markers+text",
            marker=dict(size=15, color="red", symbol="circle"),
            textposition="top center",
            name="Current Location",
        )
    )

    # Add fallback location if provided
    if fallback_location:
        fig.add_trace(
            go.Scattergeo(
                lon=[fallback_location.longitude],
                lat=[fallback_location.latitude],
                text=[f"✈️ Fallback: {fallback_location.city}"],
                mode="markers+text",
                marker=dict(size=15, color="green", symbol="star"),
                textposition="top center",
                name="Fallback Destination",
            )
        )

        # Add route line
        fig.add_trace(
            go.Scattergeo(
                lon=[current_location.longitude, fallback_location.longitude],
                lat=[current_location.latitude, fallback_location.latitude],
                mode="lines",
                line=dict(width=2, color="blue", dash="dash"),
                name="Escape Route",
            )
        )

    # Add alert markers
    if alerts:
        for alert in alerts[:5]:  # Limit to 5 alerts
            color = "orange" if alert.severity >= 7 else "yellow"
            fig.add_trace(
                go.Scattergeo(
                    lon=[alert.location.longitude],
                    lat=[alert.location.latitude],
                    text=[f"⚠️ {alert.title}"],
                    mode="markers",
                    marker=dict(size=10, color=color, symbol="x"),
                    name=alert.title,
                    hovertext=alert.description,
                )
            )

    # Update layout
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
        showcountries=True,
        countrycolor="rgb(204, 204, 204)",
    )

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)

    return fig


def create_payout_comparison_table():
    """Create comparison table for payout methods"""

    comparison_data = {
        "Method": [
            "💳 Crypto Wallet",
            "🏦 Wire Transfer",
            "💵 Cash Pickup",
            "📱 Mobile Money",
        ],
        "ETA": ["15 minutes", "2-3 days", "2-4 hours", "30 minutes"],
        "Fee": ["$2.50", "$25.00", "$10.00", "$1.00"],
        "Best For": [
            "Immediate access",
            "Large amounts",
            "No bank account",
            "Developing countries",
        ],
        "Availability": ["Global", "Global", "50K+ locations", "Africa, Asia"],
    }

    return comparison_data


def show_crisis_scenario_selector():
    """Show crisis scenario selection"""

    scenarios = {
        "Istanbul Political Unrest": {
            "location": "Istanbul, Turkey",
            "risk_type": "Political Unrest",
            "severity": 9,
            "description": "Major protests and civil unrest. Banks closing, ATMs offline.",
            "headline": "🚨 BREAKING: Mass protests in Istanbul - Payment systems disrupted",
        },
        "Beirut Banking Crisis": {
            "location": "Beirut, Lebanon",
            "risk_type": "Payment Disruption",
            "severity": 8,
            "description": "Banking sector collapse. Capital controls in effect.",
            "headline": "💰 ALERT: Lebanese banks impose strict withdrawal limits",
        },
        "Tokyo Earthquake": {
            "location": "Tokyo, Japan",
            "risk_type": "Natural Disaster",
            "severity": 7,
            "description": "Major earthquake. Infrastructure damage, transportation disrupted.",
            "headline": "🌊 URGENT: 7.2 magnitude earthquake hits Tokyo region",
        },
        "Kyiv Security Alert": {
            "location": "Kyiv, Ukraine",
            "risk_type": "Security Threat",
            "severity": 10,
            "description": "Armed conflict. Immediate evacuation recommended.",
            "headline": "⚠️ CRITICAL: State Dept issues Level 4 - Do Not Travel",
        },
    }

    st.subheader("🎬 Crisis Scenarios")
    st.write("Select a pre-built scenario for demo:")

    selected = st.selectbox(
        "Choose scenario:", list(scenarios.keys()), key="crisis_scenario"
    )

    if selected:
        scenario = scenarios[selected]

        with st.expander(f"📰 {scenario['headline']}", expanded=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Location:** {scenario['location']}")
                st.write(f"**Type:** {scenario['risk_type']}")
                st.write(f"**Description:** {scenario['description']}")

            with col2:
                st.metric("Severity", f"{scenario['severity']}/10")

        return selected

    return None


def create_progress_animation(progress: int, method: str):
    """Create animated progress indicator"""

    # Progress bar with custom styling
    st.markdown(
        f"""
    <style>
        .progress-container {{
            width: 100%;
            background-color: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            height: 30px;
            margin: 10px 0;
        }}
        .progress-bar {{
            width: {progress}%;
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
    </style>
    <div class="progress-container">
        <div class="progress-bar">{progress}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Status message
    if progress < 30:
        st.info(f"⏳ Initiating {method} transfer...")
    elif progress < 70:
        st.warning(f"🔄 Processing {method} transaction...")
    else:
        st.success(f"✅ {method} transfer completing...")
