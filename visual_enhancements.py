"""
Visual Enhancements for Safe-Passage
Interactive map, risk gauge, and improved UI elements
"""

import streamlit as st
import plotly.graph_objects as go
from models import Location, RiskAlert
from typing import List


def create_risk_gauge(risk_level: int) -> go.Figure:
    """Create speedometer-style risk gauge"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_level,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Level", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': '#d4edda'},
                {'range': [3, 5], 'color': '#fff3cd'},
                {'range': [5, 7], 'color': '#f8d7da'},
                {'range': [7, 10], 'color': '#f5c6cb'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkgray", 'family': "Arial"}
    )
    
    return fig


def create_location_map(current_location: Location, 
                       fallback_location: Location = None,
                       alerts: List[RiskAlert] = None) -> go.Figure:
    """Create interactive map with location markers"""
    
    # Create map
    fig = go.Figure()
    
    # Add current location
    fig.add_trace(go.Scattergeo(
        lon=[current_location.longitude],
        lat=[current_location.latitude],
        text=[f"📍 Current: {current_location.city}"],
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='circle'),
        textposition="top center",
        name="Current Location"
    ))
    
    # Add fallback location if provided
    if fallback_location:
        fig.add_trace(go.Scattergeo(
            lon=[fallback_location.longitude],
            lat=[fallback_location.latitude],
            text=[f"✈️ Fallback: {fallback_location.city}"],
            mode='markers+text',
            marker=dict(size=15, color='green', symbol='star'),
            textposition="top center",
            name="Fallback Destination"
        ))
        
        # Add route line
        fig.add_trace(go.Scattergeo(
            lon=[current_location.longitude, fallback_location.longitude],
            lat=[current_location.latitude, fallback_location.latitude],
            mode='lines',
            line=dict(width=2, color='blue', dash='dash'),
            name="Escape Route"
        ))
    
    # Add alert markers
    if alerts:
        for alert in alerts[:5]:  # Limit to 5 alerts
            color = 'orange' if alert.severity >= 7 else 'yellow'
            fig.add_trace(go.Scattergeo(
                lon=[alert.location.longitude],
                lat=[alert.location.latitude],
                text=[f"⚠️ {alert.title}"],
                mode='markers',
                marker=dict(size=10, color=color, symbol='x'),
                name=alert.title,
                hovertext=alert.description
            ))
    
    # Update layout
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
        showcountries=True,
        countrycolor="rgb(204, 204, 204)"
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    return fig


def create_payout_comparison_table():
    """Create comparison table for payout methods"""
    
    comparison_data = {
        "Method": ["💳 Crypto Wallet", "🏦 Wire Transfer", "💵 Cash Pickup", "📱 Mobile Money"],
        "ETA": ["15 minutes", "2-3 days", "2-4 hours", "30 minutes"],
        "Fee": ["$2.50", "$25.00", "$10.00", "$1.00"],
        "Best For": ["Immediate access", "Large amounts", "No bank account", "Developing countries"],
        "Availability": ["Global", "Global", "50K+ locations", "Africa, Asia"]
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
            "headline": "🚨 BREAKING: Mass protests in Istanbul - Payment systems disrupted"
        },
        "Beirut Banking Crisis": {
            "location": "Beirut, Lebanon",
            "risk_type": "Payment Disruption",
            "severity": 8,
            "description": "Banking sector collapse. Capital controls in effect.",
            "headline": "💰 ALERT: Lebanese banks impose strict withdrawal limits"
        },
        "Tokyo Earthquake": {
            "location": "Tokyo, Japan",
            "risk_type": "Natural Disaster",
            "severity": 7,
            "description": "Major earthquake. Infrastructure damage, transportation disrupted.",
            "headline": "🌊 URGENT: 7.2 magnitude earthquake hits Tokyo region"
        },
        "Kyiv Security Alert": {
            "location": "Kyiv, Ukraine",
            "risk_type": "Security Threat",
            "severity": 10,
            "description": "Armed conflict. Immediate evacuation recommended.",
            "headline": "⚠️ CRITICAL: State Dept issues Level 4 - Do Not Travel"
        }
    }
    
    st.subheader("🎬 Crisis Scenarios")
    st.write("Select a pre-built scenario for demo:")
    
    selected = st.selectbox(
        "Choose scenario:",
        list(scenarios.keys()),
        key="crisis_scenario"
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
    st.markdown(f"""
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
    """, unsafe_allow_html=True)
    
    # Status message
    if progress < 30:
        st.info(f"⏳ Initiating {method} transfer...")
    elif progress < 70:
        st.warning(f"🔄 Processing {method} transaction...")
    else:
        st.success(f"✅ {method} transfer completing...")
