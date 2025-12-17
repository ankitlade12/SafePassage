"""
Safe-Passage - Complete System (All Phases)
Emergency Liquidity + Exit Planning with Real Data & Simulated Payouts
"""

import streamlit as st
from models import create_sample_profile, PayoutMethod, FundStatus
from real_data_integration import EnhancedRiskMonitor
from payout_simulator import PayoutOrchestrator, PayoutTransaction
from exit_playbook import ExitPlaybookGenerator
from enhanced_ui import ProfileManager, TripPlanner, NotificationCenter, AnalyticsDashboard
from datetime import datetime

from crisis_scenarios import CrisisScenarioLibrary
from visual_enhancements import create_risk_gauge, create_location_map, create_payout_comparison_table, create_progress_animation
from export_features import ExportManager
from guided_tour import GuidedTour
from enhanced_analytics import AnalyticsDashboard as EnhancedAnalytics
import time

# Advanced Features (7 new features)
from advanced_features import QRCodeGenerator, AlertSimulator, ThemeManager
from advanced_features_part2 import PDFExporter, EmergencyWidget, ComparisonTool, CurrencyManager

# Page config
st.set_page_config(
    page_title="Safe-Passage - Emergency Liquidity System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .risk-low {
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .risk-high {
        background-color: #f8d7da;
        color: #721c24;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .payout-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state - Force fresh profile
if 'user_profile' not in st.session_state or st.session_state.user_profile.exit_fund is None:
    profile = create_sample_profile()
    st.session_state.user_profile = profile
    # Debug: verify exit fund exists
    # Exit fund created successfully

# CRITICAL FIX: Reset exit fund status to ACTIVE if it was triggered
if st.session_state.user_profile.exit_fund and st.session_state.user_profile.exit_fund.status != FundStatus.ACTIVE:
    st.session_state.user_profile.exit_fund.status = FundStatus.ACTIVE
    st.session_state.user_profile.exit_fund.triggered_at = None

if 'risk_monitor' not in st.session_state:
    st.session_state.risk_monitor = EnhancedRiskMonitor()
    st.session_state.risk_monitor.refresh_all_data(st.session_state.user_profile.current_location)

if 'payout_orchestrator' not in st.session_state:
    st.session_state.payout_orchestrator = PayoutOrchestrator()

if 'scenario_library' not in st.session_state:
    st.session_state.scenario_library = CrisisScenarioLibrary()


if 'crisis_triggered' not in st.session_state:
    st.session_state.crisis_triggered = False

if 'emergency_activated' not in st.session_state:
    st.session_state.emergency_activated = False

if 'payout_transaction' not in st.session_state:
    st.session_state.payout_transaction = None

# Get current state
user = st.session_state.user_profile
monitor = st.session_state.risk_monitor
payout_orch = st.session_state.payout_orchestrator
current_risk = monitor.get_current_risk_level(user.current_location)

# Header
st.title("🛡️ Safe-Passage")
st.markdown("**Emergency Liquidity + Exit Planning System**")
st.caption("Preparedness when minutes matter - Complete with real data integration & simulated payouts")

# Sidebar
with st.sidebar:
    st.header("👤 Profile")
    
    # Profile customization
    with st.expander("✏️ Customize Profile", expanded=False):
        st.markdown("**Current Location**")
        new_name = st.text_input("Your Name", value=user.name, key="profile_name")
        
        col1, col2 = st.columns(2)
        with col1:
            new_city = st.text_input("City", value=user.current_location.city, key="profile_city")
        with col2:
            new_country = st.text_input("Country", value=user.current_location.country, key="profile_country")
        
        st.markdown("**Fallback Destination (Safe Location)**")
        col3, col4 = st.columns(2)
        with col3:
            fallback_city = st.text_input("Fallback City", 
                value=user.exit_fund.fallback_destinations[0].city if user.exit_fund and user.exit_fund.fallback_destinations else "Athens",
                key="fallback_city")
        with col4:
            fallback_country = st.text_input("Fallback Country",
                value=user.exit_fund.fallback_destinations[0].country if user.exit_fund and user.exit_fund.fallback_destinations else "Greece",
                key="fallback_country")
        
        if st.button("💾 Save Profile", use_container_width=True):
            from geocoding import get_coordinates
            from models import Location
            
            # Update profile
            user.name = new_name
            
            # Get coordinates for new location
            lat, lon = get_coordinates(new_city, new_country)
            user.current_location = Location(new_city, new_country, lat, lon)
            
            # Update fallback destination
            fallback_lat, fallback_lon = get_coordinates(fallback_city, fallback_country)
            fallback_location = Location(fallback_city, fallback_country, fallback_lat, fallback_lon)
            
            if user.exit_fund:
                user.exit_fund.fallback_destinations = [fallback_location]
            
            # IMPORTANT: Refresh risk monitor for new location
            monitor.active_alerts = []  # Clear old alerts
            monitor.refresh_all_data(user.current_location)
            
            st.success("✅ Profile updated! Refreshing alerts for new location...")
            st.rerun()
    
    # Display current profile
    st.write(f"**{user.name}**")
    st.write(f"📍 {user.current_location}")
    st.write(f"🏠 {user.home_country}")
    
    st.markdown("---")
    
    st.header("💰 Exit Fund")
    
    if user.has_active_fund():
        status_color = {
            FundStatus.ACTIVE: "🟢",
            FundStatus.TRIGGERED: "🟡",
            FundStatus.COMPLETED: "✅"
        }[user.exit_fund.status]
        
        st.write(f"{status_color} **Status:** {user.exit_fund.status.value.upper()}")
        st.metric("Amount", f"${user.exit_fund.amount:,.0f} {user.exit_fund.currency}")
        
        with st.expander("Payout Methods"):
            for method in user.exit_fund.payout_methods:
                details = payout_orch.get_method_details(method)
                st.write(f"**{details.get('name', method.value)}**")
                st.caption(f"ETA: {details.get('eta', 'N/A')} | Fee: {details.get('fee', 'N/A')}")
    else:
        st.warning("⚠️ No exit fund configured")
    
    st.markdown("---")
    
    # Demo controls
    st.header("🎬 Demo Controls")
    
    if st.button("🚨 Trigger Crisis", use_container_width=True):
        st.session_state.crisis_triggered = True
        # Simulate high-risk alert
        from risk_monitor import RiskMonitor
        temp_monitor = RiskMonitor()
        temp_monitor.trigger_crisis_simulation(user.current_location)
        st.session_state.risk_monitor.active_alerts.extend(temp_monitor.active_alerts)
        st.rerun()
    
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.crisis_triggered = False
        st.session_state.emergency_activated = False
        st.session_state.payout_transaction = None
        st.session_state.risk_monitor = EnhancedRiskMonitor()
        st.session_state.risk_monitor.refresh_all_data(user.current_location)
        if user.exit_fund:
            user.exit_fund.status = FundStatus.ACTIVE
        st.rerun()
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        with st.spinner("Fetching latest data..."):
            monitor.refresh_all_data(user.current_location)
            time.sleep(1)
        st.success("✅ Data refreshed")
        st.rerun()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", 
    "🚨 Emergency", 
    "📋 Audit Trail",
    "✈️ Trip Planner",
    "⚙️ Settings",
    "📈 Analytics"
])

# Tab 1: Dashboard with Enhanced Visuals
with tab1:
    # Risk Gauge (Feature #3)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Risk Level")
        st.plotly_chart(create_risk_gauge(current_risk), use_container_width=True, key="risk_gauge")
    
    with col2:
        st.metric("Location", user.current_location.city)
        st.metric("Fund Status", user.exit_fund.status.value.upper() if user.exit_fund else "N/A")
        st.metric("Exit Fund", f"${user.exit_fund.amount:,.0f}" if user.exit_fund else "N/A")
        st.metric("Fallback", user.exit_fund.fallback_destinations[0].city if user.exit_fund and user.exit_fund.fallback_destinations else "N/A")
    
    st.markdown("---")
    
    # Interactive Map (Feature #1)
    st.subheader("📍 Location Map")
    fallback = user.exit_fund.fallback_destinations[0] if user.exit_fund and user.exit_fund.fallback_destinations else None
    nearby_alerts = monitor.get_nearby_alerts(user.current_location, radius_km=500)
    st.plotly_chart(create_location_map(user.current_location, fallback, nearby_alerts), use_container_width=True, key="location_map")
    
    st.markdown("---")
    
    # Active alerts with real data
    st.subheader("🌍 Active Alerts (Real Data)")
    
    nearby_alerts = monitor.get_nearby_alerts(user.current_location, radius_km=500)
    
    if nearby_alerts:
        for alert in nearby_alerts:
            severity_emoji = {
                "EXTREME": "🔴",
                "HIGH": "🟠",
                "MODERATE": "🟡",
                "LOW": "🟢"
            }[alert.get_severity_label()]
            
            with st.expander(f"{severity_emoji} {alert.title} - {alert.get_severity_label()}", expanded=alert.is_critical()):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Location:** {alert.location}")
                    st.write(f"**Type:** {alert.risk_type.value.replace('_', ' ').title()}")
                    st.write(f"**Description:** {alert.description}")
                    st.write(f"**Source:** {alert.source}")
                
                with col2:
                    st.metric("Severity", f"{alert.severity}/10")
                    st.write(f"**Time:** {alert.timestamp.strftime('%H:%M')}")
                    st.write(f"**Radius:** {alert.affected_radius_km} km")
    else:
        st.success("✅ No active alerts in your area")
    
    # Data sources
    st.markdown("---")
    st.subheader("📡 Data Sources")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**GDELT**\nGlobal events database")
    with col2:
        st.info("**USGS**\nEarthquake monitoring")
    with col3:
        st.info("**State Dept**\nTravel advisories")

# Tab 2: Emergency Activation
with tab2:
    st.header("🚨 Emergency Activation")
    
    if not user.has_active_fund():
        st.error("⚠️ No active exit fund. Please set up an exit fund first.")
        
        if st.button("Set Up Exit Fund Now"):
            st.session_state.show_fund_wizard = True
    
    elif st.session_state.emergency_activated and st.session_state.payout_transaction:
        st.success("✅ Emergency Protocol Activated!")
        
        transaction = st.session_state.payout_transaction
        
        # Update transaction status
        transaction = payout_orch.check_status(transaction)
        st.session_state.payout_transaction = transaction
        
        # Payout status
        st.markdown("### 💰 Payout Status")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Amount", f"${transaction.amount:,.0f}")
        with col2:
            st.metric("Method", transaction.method.value.replace('_', ' ').title())
        with col3:
            st.metric("Status", transaction.status.upper())
        with col4:
            progress = transaction.get_progress_percentage()
            st.metric("Progress", f"{progress}%")
        
        # Progress bar
        st.progress(progress / 100)
        
        if transaction.status == "completed":
            st.success(f"✅ Payout completed at {transaction.completed_at.strftime('%H:%M:%S')}")
            st.balloons()
        elif transaction.status == "processing":
            st.info(f"⏳ Processing... {transaction.confirmation_code}")
            time.sleep(2)
            st.rerun()
        else:
            st.warning("⏳ Payout pending...")
        
        # Transaction details
        with st.expander("Transaction Details"):
            st.write(f"**Transaction ID:** {transaction.transaction_id}")
            st.write(f"**Initiated:** {transaction.initiated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if transaction.estimated_arrival:
                st.write(f"**Est. Arrival:** {transaction.estimated_arrival.strftime('%Y-%m-%d %H:%M:%S')}")
            if transaction.recipient_address:
                st.write(f"**Recipient:** {transaction.recipient_address}")
        
        # Exit checklist
        st.markdown("---")
        st.markdown("### 📋 Exit Checklist")
        
        playbook_gen = ExitPlaybookGenerator()
        checklist = playbook_gen.generate_checklist(
            user.current_location,
            user.exit_fund.fallback_destinations[0],
            user.exit_fund.trusted_contacts
        )
        
        critical_items = checklist.get_critical_items()
        
        st.markdown("**🔴 Critical Actions (Do First):**")
        for item in critical_items:
            st.checkbox(item.title, key=f"critical_{item.item_id}", help=item.description)
        
        st.markdown("**📌 Additional Steps:**")
        for item in [i for i in checklist.items if i.priority > 2]:
            st.checkbox(item.title, key=f"item_{item.item_id}", help=item.description)
        
        # Safe routes
        st.markdown("---")
        st.markdown("### 🛫 Safe Routes")
        for route in checklist.safe_routes:
            st.info(f"**{route.method.upper()}:** {route.from_location} → {route.to_location} ({route.estimated_time})\n\n{route.notes}")
        
        # Money access
        st.markdown("---")
        st.markdown("### 💵 Money Access Steps")
        for step in checklist.money_access_steps:
            st.write(step)
        
        # Embassy info
        if checklist.embassy_info:
            st.markdown("---")
            st.markdown("### 🏛️ Embassy Information")
            st.write(f"**{checklist.embassy_info.get('name')}**")
            if checklist.embassy_info.get('address'):
                st.write(f"📍 {checklist.embassy_info.get('address')}")
            st.write(f"📞 {checklist.embassy_info.get('phone')}")
            st.write(f"🚨 Emergency: {checklist.embassy_info.get('emergency')}")
    
    else:
        # Show activation interface
        if current_risk >= 7:
            st.error("🚨 **HIGH RISK DETECTED** - Immediate action recommended")
            
            nearby_alerts = monitor.get_nearby_alerts(user.current_location)
            if nearby_alerts:
                alert = nearby_alerts[0]
                st.warning(f"**Alert:** {alert.title}\n\n{alert.description}")
            
            st.markdown("---")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 💰 Available Exit Fund")
                st.metric("Amount", f"${user.exit_fund.amount:,.0f} {user.exit_fund.currency}")
                
                st.markdown("**Select Payout Method:**")
                
                # Show all available methods with details
                selected_method = None
                for method in user.exit_fund.payout_methods:
                    details = payout_orch.get_method_details(method)
                    
                    if st.button(
                        f"💳 {details.get('name', method.value)}\n\nETA: {details.get('eta')} | Fee: {details.get('fee')}",
                        key=f"method_{method.value}",
                        use_container_width=True
                    ):
                        selected_method = method
                
                # Emergency Widget (Feature #6)
                EmergencyWidget.show_emergency_widget(user)
                
                if selected_method:
                    st.session_state.selected_payout_method = selected_method
            
            with col2:
                st.markdown("### ⚡ Quick Stats")
                st.metric("Fallback Destination", user.exit_fund.fallback_destinations[0].city)
                st.metric("Trusted Contacts", len(user.exit_fund.trusted_contacts))
                st.metric("Risk Level", f"{current_risk}/10")
            
            st.markdown("---")
            
            if 'selected_payout_method' in st.session_state:
                method = st.session_state.selected_payout_method
                details = payout_orch.get_method_details(method)
                
                st.info(f"**Selected:** {details.get('name')} - ETA: {details.get('eta')}")
                
                if st.button("🚨 ACTIVATE EMERGENCY PROTOCOL", use_container_width=True, type="primary"):
                    # Initiate payout
                    transaction = payout_orch.initiate_payout(
                        method=method,
                        amount=user.exit_fund.amount,
                        currency=user.exit_fund.currency
                    )
                    
                    st.session_state.payout_transaction = transaction
                    st.session_state.emergency_activated = True
                    user.exit_fund.status = FundStatus.TRIGGERED
                    user.exit_fund.triggered_at = datetime.now()
                    
                    st.rerun()
            
            # Feature #10: PDF Export (Emergency Checklist)
            st.markdown("---")
            st.subheader("📄 Export Emergency Checklist")
            st.write("Generate a printable PDF of your personalized emergency checklist.")
            if st.button("Download PDF Checklist", use_container_width=True):
                st.success("PDF generation initiated! (Simulated)")
                # In a real app, you'd call a function to generate and serve the PDF
                # For example: pdf_data = generate_checklist_pdf(user, checklist)
                # st.download_button(label="Click to Download", data=pdf_data, file_name="emergency_checklist.pdf", mime="application/pdf")

            # Feature #11: Currency Converter
            st.markdown("---")
            st.subheader("💱 Currency Converter")
            st.write("Convert your exit fund amount to local currency.")
            
            col_curr1, col_curr2 = st.columns(2)
            with col_curr1:
                amount_to_convert = st.number_input("Amount", value=float(user.exit_fund.amount), min_value=0.0, format="%.2f")
            with col_curr2:
                target_currency = st.selectbox("Convert to", options=["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL", "ZAR"], index=0)
            
            if st.button("Convert", use_container_width=True):
                # Simulate currency conversion
                exchange_rate = {
                    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 155.0, "CAD": 1.37,
                    "AUD": 1.52, "CHF": 0.91, "CNY": 7.24, "INR": 83.3, "BRL": 5.12, "ZAR": 18.5
                }.get(target_currency, 1.0) # Default to 1.0 if not found
                
                converted_amount = amount_to_convert * exchange_rate
                st.success(f"**{amount_to_convert:,.2f} {user.exit_fund.currency}** is approximately **{converted_amount:,.2f} {target_currency}**")
        
        else:
            st.info("✅ Risk level is low. Emergency activation not needed.")
            st.write("Emergency protocol can be activated when risk level reaches 7/10 or higher.")

# Tab 3: Audit Trail
with tab3:
    st.header("📋 Audit Trail")
    
    if st.session_state.payout_transaction:
        transaction = st.session_state.payout_transaction
        
        st.json({
            "transaction_id": transaction.transaction_id,
            "method": transaction.method.value,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "status": transaction.status,
            "initiated_at": transaction.initiated_at.isoformat(),
            "completed_at": transaction.completed_at.isoformat() if transaction.completed_at else None
        })
        
        st.markdown("---")
        st.markdown("### Event Timeline")
        st.write(f"**{transaction.initiated_at.strftime('%Y-%m-%d %H:%M:%S')}** - Emergency protocol activated")
        st.write(f"**Method:** {transaction.method.value}")
        st.write(f"**Amount:** ${transaction.amount:,.0f} {transaction.currency}")
        if transaction.completed_at:
            st.write(f"**{transaction.completed_at.strftime('%Y-%m-%d %H:%M:%S')}** - Payout completed")
    else:
        st.success("✅ **No Emergency Activations**")
        st.write("Your exit fund is active and ready, but you haven't needed to activate it yet.")
        st.write("")
        st.info("💡 **When you activate emergency protocol**, you'll see:")
        st.write("- Transaction ID and details")
        st.write("- Real-time payout status")
        st.write("- Complete event timeline")
        st.write("- Audit trail for compliance")

# Tab 4: Trip Planner
with tab4:
    TripPlanner.show_trip_planner()
    
    st.markdown("---")
    
    # Feature #9: Comparison Tool
    ComparisonTool.show_comparison_tool()

# Tab 5: Settings
with tab5:
    NotificationCenter.show_notification_settings()
    
    st.markdown("---")
    
    # Feature #1: QR Code Generator
    QRCodeGenerator.show_qr_widget(user)
    
    st.markdown("---")
    
    # Feature #2: Alert Previews
    AlertSimulator.show_alert_previews()

# Tab 6: Enhanced Analytics (Feature #9)
with tab6:
    from enhanced_analytics import AnalyticsDashboard as EnhancedAnalytics
    EnhancedAnalytics.show_enhanced_analytics(user.current_location.city)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Safe-Passage</strong> - Emergency Liquidity + Exit Planning</p>
    <p style="font-size: 0.8rem;">✨ Complete System: Real Data Integration + Simulated Payouts + Enhanced UI</p>
    <p style="font-size: 0.7rem;">Phase 1-4 Complete | Ready for Demo</p>
</div>
""", unsafe_allow_html=True)
