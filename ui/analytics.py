"""
Enhanced Analytics Dashboard
Risk heatmap, charts, and statistics
"""

import streamlit as st
import plotly.graph_objects as go

from datetime import datetime, timedelta
import random


class AnalyticsDashboard:
    """Enhanced analytics and insights"""

    @staticmethod
    def create_risk_heatmap():
        """Create risk heatmap by country"""

        countries = [
            # High Risk
            "Ukraine",
            "Turkey",
            "Lebanon",
            "Syria",
            "Afghanistan",
            # Moderate Risk
            "Egypt",
            "Pakistan",
            "Russia",
            "Iran",
            # Low-Moderate Risk
            "India",
            "China",
            "Brazil",
            "Mexico",
            "South Africa",
            # Low Risk
            "United States",
            "United Kingdom",
            "France",
            "Germany",
            "Canada",
            "Australia",
            "Japan",
            "Singapore",
            "Switzerland",
            "Norway",
        ]

        risk_levels = [
            # High Risk
            10,
            9,
            8,
            9,
            10,
            # Moderate Risk
            6,
            7,
            6,
            8,
            # Low-Moderate Risk
            4,
            5,
            4,
            5,
            5,
            # Low Risk
            2,
            2,
            3,
            2,
            2,
            2,
            3,
            2,
            2,
            2,
        ]

        fig = go.Figure(
            data=go.Choropleth(
                locations=countries,
                locationmode="country names",
                z=risk_levels,
                colorscale="RdYlGn_r",
                colorbar_title="Risk Level",
                zmin=0,
                zmax=10,
            )
        )

        fig.update_layout(
            title="Global Risk Heatmap",
            geo=dict(
                showframe=False, showcoastlines=True, projection_type="natural earth"
            ),
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
        )

        return fig

    @staticmethod
    def create_alert_frequency_chart():
        """Create alert frequency chart"""

        # Generate sample data
        dates = [
            (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(30, 0, -1)
        ]
        alerts = [random.randint(0, 5) for _ in range(30)]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=alerts,
                mode="lines+markers",
                name="Alerts",
                line=dict(color="#FF6B6B", width=2),
                marker=dict(size=6),
            )
        )

        fig.update_layout(
            title="Alert Frequency (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Number of Alerts",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False,
        )

        return fig

    @staticmethod
    def create_payout_method_stats():
        """Create payout method usage statistics"""

        methods = ["Crypto Wallet", "Wire Transfer", "Cash Pickup", "Mobile Money"]
        usage = [45, 25, 20, 10]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=methods,
                    values=usage,
                    hole=0.3,
                    marker=dict(colors=["#4CAF50", "#2196F3", "#FF9800", "#9C27B0"]),
                )
            ]
        )

        fig.update_layout(
            title="Payout Method Preferences",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
        )

        return fig

    @staticmethod
    def create_user_journey_timeline(user_location="Dallas"):
        """Create user journey timeline"""
        from datetime import datetime, timedelta

        today = datetime.now()

        events = [
            {
                "date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "event": "Profile Created",
                "type": "setup",
            },
            {
                "date": (today - timedelta(days=11)).strftime("%Y-%m-%d"),
                "event": "Exit Fund Activated",
                "type": "setup",
            },
            {
                "date": (today - timedelta(days=6)).strftime("%Y-%m-%d"),
                "event": "First Alert Received",
                "type": "alert",
            },
            {
                "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                "event": f"Location Set: {user_location}",
                "type": "travel",
            },
            {
                "date": today.strftime("%Y-%m-%d"),
                "event": "System Active",
                "type": "setup",
            },
        ]

        fig = go.Figure()

        for i, event in enumerate(events):
            color = {
                "setup": "#4CAF50",
                "alert": "#FF9800",
                "travel": "#2196F3",
                "emergency": "#F44336",
            }[event["type"]]

            fig.add_trace(
                go.Scatter(
                    x=[event["date"]],
                    y=[i],
                    mode="markers+text",
                    marker=dict(size=15, color=color),
                    text=[event["event"]],
                    textposition="middle right",
                    showlegend=False,
                )
            )

        fig.update_layout(
            title="User Journey Timeline",
            xaxis_title="Date",
            yaxis=dict(showticklabels=False),
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
        )

        return fig

    @staticmethod
    def show_enhanced_analytics(user_location_city="Dallas", alerts=None, risk_level=2):
        """Show complete enhanced analytics dashboard with real data"""

        st.subheader("📊 Enhanced Analytics Dashboard")

        # Calculate realistic metrics based on current date
        from datetime import datetime, timedelta

        today = datetime.now()
        days_since_signup = (today - datetime(2025, 12, 1)).days
        
        # Use actual alerts if provided
        actual_alert_count = len(alerts) if alerts else 0

        # Key metrics - USE REAL DATA
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Days Monitored",
                str(days_since_signup),
                delta=f"{min(days_since_signup, 7)} this week",
            )
        with col2:
            # Use actual alert count
            st.metric(
                "Active Alerts",
                str(actual_alert_count),
                delta=f"from {user_location_city}",
            )
        with col3:
            # Use actual risk level
            st.metric(
                "Current Risk", 
                f"{risk_level}/10", 
                delta="Live data" if actual_alert_count > 0 else "Baseline"
            )
        with col4:
            st.metric(
                "Emergency Activations", "0", delta="None triggered"
            )

        st.markdown("---")

        # Risk heatmap
        st.markdown("### 🌍 Global Risk Heatmap")
        st.plotly_chart(
            AnalyticsDashboard.create_risk_heatmap(),
            width="stretch",
            key="risk_heatmap",
        )

        # Journey timeline with user's location
        st.markdown("### 📅 Your Journey")
        st.plotly_chart(
            AnalyticsDashboard.create_user_journey_timeline(user_location_city),
            width="stretch",
            key="journey_timeline",
        )

        # Real alert history table
        st.markdown("### 📋 Recent Alerts")

        if alerts and len(alerts) > 0:
            # Use actual alerts
            alert_data = {
                "Date": [],
                "Location": [],
                "Type": [],
                "Severity": [],
                "Source": [],
            }
            
            for alert in alerts[:5]:  # Show up to 5 recent alerts
                alert_data["Date"].append(alert.timestamp.strftime("%Y-%m-%d %H:%M") if hasattr(alert, 'timestamp') else today.strftime("%Y-%m-%d"))
                alert_data["Location"].append(f"{alert.location.city}, {alert.location.country}" if hasattr(alert, 'location') else user_location_city)
                alert_data["Type"].append(alert.risk_type.value if hasattr(alert, 'risk_type') and hasattr(alert.risk_type, 'value') else "Unknown")
                alert_data["Severity"].append(f"{alert.severity}/10" if hasattr(alert, 'severity') else "N/A")
                alert_data["Source"].append(alert.source if hasattr(alert, 'source') else "Unknown")
            
            st.dataframe(alert_data, width="stretch")
        else:
            st.success("✅ No active alerts - your area is currently safe")

