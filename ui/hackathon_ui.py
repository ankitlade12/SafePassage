"""
Hackathon UI Components
Advanced visualizations and widgets for hackathon demo:
- Chaos Slider
- Sankey Diagram (Fund Flow)
- Dead Man's Switch Widget
- Guardian Widget
- Shadow Banking Widget
- Blockchain Badge
"""

import streamlit as st
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64
import json
from datetime import datetime
from typing import Optional

from core.hackathon_features import (
    DeadManSwitch,
    GuardianNetwork,
    ShadowBankingMode,
    ShadowBankingCode,
    ProofOfReserves,
    ChaosSimulator,
    CheckInStatus,
)


class ChaosSliderUI:
    """Interactive chaos level slider for demo"""
    
    @staticmethod
    def show_chaos_slider(current_level: int = 2) -> int:
        """Display chaos slider and return selected level"""
        
        st.markdown("### 🎚 Risk Simulator")
        st.caption("Adjust risk level to simulate different crisis scenarios")
        
        # Create a styled slider
        col1, col2, col3 = st.columns([1, 8, 1])
        
        with col1:
            st.markdown("🕊️")
            st.caption("Peace")
        
        with col2:
            level = st.slider(
                "Chaos Level",
                min_value=0,
                max_value=10,
                value=current_level,
                key="chaos_slider",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("⚔️")
            st.caption("War")
        
        # Get level info
        simulator = ChaosSimulator()
        simulator.set_level(level)
        info = simulator.get_level_info()
        
        # Display current status
        status_color = "#4caf50" if level <= 3 else "#ff9800" if level <= 6 else "#f44336"
        
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, {status_color}22, {status_color}11); border-radius: 10px; margin: 10px 0;'>
                <span style='font-size: 2em;'>{info['emoji']}</span>
                <h3 style='margin: 5px 0; color: {status_color};'>{info['label'].upper()}</h3>
                <p style='margin: 0; color: #666;'>{info['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Show network effects
        effects = simulator.get_network_effects()
        ChaosSliderUI._show_network_effects(effects)
        
        return level
    
    @staticmethod
    def _show_network_effects(effects: dict):
        """Display network status indicators"""
        st.markdown("**Network Status:**")
        
        cols = st.columns(5)
        icons = {
            "banking": "🏦",
            "atm": "💳",
            "crypto": "₿",
            "mobile_money": "📱",
            "cash_pickup": "💵"
        }
        
        status_colors = {
            "ONLINE": "#4caf50",
            "CONGESTED": "#ff9800",
            "RESTRICTED": "#ffc107",
            "OFFLINE": "#f44336"
        }
        
        for i, (network, status) in enumerate(effects.items()):
            with cols[i]:
                color = status_colors.get(status, "#9e9e9e")
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 5px;'>
                        <span style='font-size: 1.5em;'>{icons.get(network, '📡')}</span><br>
                        <span style='color: {color}; font-weight: bold; font-size: 0.7em;'>●</span>
                        <span style='font-size: 0.7em;'>{status}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


class SankeyDiagramUI:
    """Sankey diagram showing fund flow through the Oracle"""
    
    @staticmethod
    def create_sankey(risk_level: int, fund_amount: float = 5000.0) -> go.Figure:
        """Create Sankey diagram for fund flow visualization"""
        
        # Determine network statuses based on risk
        if risk_level <= 3:
            bank_status = "ONLINE"
            crypto_status = "ONLINE"
            cash_status = "ONLINE"
            mobile_status = "ONLINE"
        elif risk_level <= 6:
            bank_status = "CONGESTED"
            crypto_status = "ONLINE"
            cash_status = "CONGESTED"
            mobile_status = "ONLINE"
        elif risk_level <= 8:
            bank_status = "RESTRICTED"
            crypto_status = "ONLINE"
            cash_status = "RESTRICTED"
            mobile_status = "ONLINE"
        else:
            bank_status = "OFFLINE"
            crypto_status = "ONLINE"
            cash_status = "OFFLINE"
            mobile_status = "RESTRICTED"
        
        # Node labels
        labels = [
            f"Exit Fund<br>${fund_amount:,.0f}",  # 0
            "Network Check",                       # 1
            f"Crypto<br>({crypto_status})",        # 2
            f"Bank<br>({bank_status})",            # 3
            f"Cash<br>({cash_status})",            # 4
            f"Mobile<br>({mobile_status})",        # 5
            "✅ User Wallet",                       # 6
            "❌ BLOCKED",                           # 7
        ]
        
        # Define colors based on status
        def get_color(status):
            if status == "ONLINE":
                return "rgba(76, 175, 80, 0.8)"
            elif status == "CONGESTED":
                return "rgba(255, 152, 0, 0.8)"
            elif status == "RESTRICTED":
                return "rgba(255, 193, 7, 0.8)"
            else:
                return "rgba(244, 67, 54, 0.8)"
        
        # Node colors
        node_colors = [
            "rgba(33, 150, 243, 0.8)",  # Fund - blue
            "rgba(156, 39, 176, 0.8)",  # Network Check - purple
            get_color(crypto_status),
            get_color(bank_status),
            get_color(cash_status),
            get_color(mobile_status),
            "rgba(76, 175, 80, 0.8)",   # User Wallet - green
            "rgba(244, 67, 54, 0.8)",   # Blocked - red
        ]
        
        # Define links (source, target, value)
        sources = []
        targets = []
        values = []
        link_colors = []
        
        # Fund to Network Check
        sources.append(0)
        targets.append(1)
        values.append(fund_amount)
        link_colors.append("rgba(33, 150, 243, 0.4)")
        
        # Calculate amounts based on recommendation
        if risk_level >= 8:
            crypto_amount = fund_amount * 0.6
            mobile_amount = fund_amount * 0.3
            bank_amount = 0
            cash_amount = 0
            blocked_amount = fund_amount * 0.1
        elif risk_level >= 6:
            crypto_amount = fund_amount * 0.4
            mobile_amount = fund_amount * 0.3
            bank_amount = fund_amount * 0.2
            cash_amount = fund_amount * 0.1
            blocked_amount = 0
        else:
            crypto_amount = fund_amount * 0.25
            mobile_amount = fund_amount * 0.25
            bank_amount = fund_amount * 0.25
            cash_amount = fund_amount * 0.25
            blocked_amount = 0
        
        # Network to methods
        for method_idx, (amount, status) in enumerate([
            (crypto_amount, crypto_status),
            (bank_amount, bank_status),
            (cash_amount, cash_status),
            (mobile_amount, mobile_status),
        ], start=2):
            if amount > 0:
                sources.append(1)
                targets.append(method_idx)
                values.append(amount)
                link_colors.append(get_color(status).replace("0.8", "0.4"))
        
        # Methods to destination
        for method_idx, (amount, status) in enumerate([
            (crypto_amount, crypto_status),
            (bank_amount, bank_status),
            (cash_amount, cash_status),
            (mobile_amount, mobile_status),
        ], start=2):
            if amount > 0:
                if status in ["ONLINE", "CONGESTED"]:
                    sources.append(method_idx)
                    targets.append(6)  # User Wallet
                    values.append(amount)
                    link_colors.append("rgba(76, 175, 80, 0.4)")
                elif status == "RESTRICTED":
                    # Split between success and blocked
                    sources.append(method_idx)
                    targets.append(6)
                    values.append(amount * 0.5)
                    link_colors.append("rgba(255, 193, 7, 0.4)")
                    
                    sources.append(method_idx)
                    targets.append(7)
                    values.append(amount * 0.5)
                    link_colors.append("rgba(244, 67, 54, 0.4)")
                else:  # OFFLINE
                    sources.append(method_idx)
                    targets.append(7)
                    values.append(amount)
                    link_colors.append("rgba(244, 67, 54, 0.4)")
        
        # Add blocked amount if any
        if blocked_amount > 0:
            sources.append(1)
            targets.append(7)
            values.append(blocked_amount)
            link_colors.append("rgba(244, 67, 54, 0.4)")
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="white", width=0.5),
                label=labels,
                color=node_colors
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=link_colors
            )
        )])
        
        fig.update_layout(
            title=dict(
                text="Liquidity Oracle: Fund Flow Analysis",
                font=dict(size=16)
            ),
            font=dict(size=12),
            height=350,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig
    
    @staticmethod
    def show_sankey(risk_level: int, fund_amount: float = 5000.0):
        """Display Sankey diagram"""
        fig = SankeyDiagramUI.create_sankey(risk_level, fund_amount)
        st.plotly_chart(fig, width="stretch")


class DeadManSwitchWidget:
    """Dead Man's Switch UI component"""
    
    @staticmethod
    def show_switch(switch: DeadManSwitch) -> DeadManSwitch:
        """Display Dead Man's Switch controls"""
        
        st.markdown("### Dead Man's Switch")
        st.caption("Automatic safety check-in system")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            enabled = st.toggle(
                "Enable Dead Man's Switch",
                value=switch.enabled,
                key="dms_toggle"
            )
            switch.enabled = enabled
            
            if enabled:
                interval = st.select_slider(
                    "Check-in Interval",
                    options=[4, 8, 12, 24, 48],
                    value=switch.interval_hours,
                    format_func=lambda x: f"{x} hours",
                    key="dms_interval"
                )
                switch.interval_hours = interval
        
        with col2:
            if enabled:
                status = switch.get_status()
                
                if status == CheckInStatus.ACTIVE:
                    st.success(f"✅ Active")
                    st.caption(f"Time remaining: {switch.format_remaining()}")
                elif status == CheckInStatus.WARNING:
                    st.warning(f"⚠️ Check-in Soon!")
                    st.caption(f"Only {switch.format_remaining()} left")
                elif status == CheckInStatus.EXPIRED:
                    st.error(f"🚨 EXPIRED!")
                    st.caption("Auto-payout triggered")
        
        if enabled:
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ Check In Now", type="primary", width="stretch"):
                    switch.check_in()
                    st.success("Checked in! Timer reset.")
                    st.rerun()
            
            with col2:
                st.metric(
                    "Last Check-in",
                    switch.last_checkin.strftime("%H:%M"),
                    delta=f"{(datetime.now() - switch.last_checkin).seconds // 60}m ago"
                )
            
            with col3:
                with st.expander("⚙️ Settings"):
                    auto_payout = st.checkbox(
                        "Auto-payout on expiry",
                        value=switch.auto_payout_enabled,
                        key="dms_auto_payout"
                    )
                    switch.auto_payout_enabled = auto_payout
                    
                    st.caption("When expired, automatically initiate emergency payout to fallback destination.")
        
        return switch


class GuardianWidget:
    """Guardian Network UI component"""
    
    @staticmethod
    def show_guardian_manager(network: GuardianNetwork) -> GuardianNetwork:
        """Display guardian management interface"""
        
        st.markdown("### Guardian Network")
        st.caption("Trusted contacts for emergency multi-sig safety")
        
        # Show existing guardians
        if network.guardians:
            for i, guardian in enumerate(network.guardians):
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{guardian.name}**")
                        st.caption(guardian.phone)
                    
                    with col2:
                        st.caption(guardian.email)
                    
                    with col3:
                        active = st.toggle(
                            "Active",
                            value=guardian.is_active,
                            key=f"guardian_active_{i}",
                            label_visibility="collapsed"
                        )
                        guardian.is_active = active
                    
                    with col4:
                        if st.button("🗑️", key=f"remove_guardian_{i}"):
                            network.remove_guardian(i)
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No guardians configured. Add up to 3 trusted contacts.")
        
        # Add new guardian
        if len(network.guardians) < 3:
            with st.expander("➕ Add Guardian", expanded=len(network.guardians) == 0):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Name", key="new_guardian_name")
                    new_phone = st.text_input("Phone", key="new_guardian_phone", placeholder="+1-555-0123")
                
                with col2:
                    new_email = st.text_input("Email", key="new_guardian_email")
                
                if st.button("Add Guardian", disabled=not (new_name and new_phone and new_email)):
                    network.add_guardian(new_name, new_phone, new_email)
                    st.success(f"✅ Added {new_name} as guardian")
                    st.rerun()
        
        # Alert threshold info
        st.markdown("---")
        st.markdown(f"""
        **Auto-Alert Trigger:** When risk level reaches **{network.alert_threshold}/10** or higher, 
        all active guardians will receive an emergency notification.
        """)
        
        return network
    
    @staticmethod
    def show_guardian_alert(network: GuardianNetwork, risk_level: int):
        """Show guardian alert notification"""
        if network.should_alert(risk_level):
            notifications = network.notify_all()
            
            st.error("GUARDIAN ALERT TRIGGERED")
            
            for notif in notifications:
                st.markdown(f"""
                <div style='background: #ffebee; padding: 10px; border-radius: 8px; margin: 5px 0;'>
                    <strong>📤 Alert sent to {notif['guardian']}</strong><br>
                    <small>{notif['phone']} | {notif['email']}</small><br>
                    <em style='color: #666;'>{notif['message']}</em>
                </div>
                """, unsafe_allow_html=True)


class ShadowBankingWidget:
    """Shadow Banking Mode UI component"""
    
    @staticmethod
    def show_shadow_mode(mode: ShadowBankingMode, fund_amount: float, currency: str):
        """Display Shadow Banking Mode interface"""
        
        st.markdown("### Shadow Banking Mode")
        st.caption("Offline-first emergency fund access")
        
        st.warning("Use when internet/banking infrastructure is down")
        
        # Generate offline code button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Generate Offline Code", type="primary", width="stretch"):
                code = mode.generate_offline_code(fund_amount, currency)
                st.session_state.shadow_code = code
        
        # Display active code
        if hasattr(st.session_state, 'shadow_code') and st.session_state.shadow_code:
            code = st.session_state.shadow_code
            
            st.markdown("---")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Generate QR code
                qr_data = mode.get_qr_data(code)
                qr = qrcode.QRCode(version=1, box_size=6, border=2)
                qr.add_data(json.dumps(qr_data))
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                
                buffer = BytesIO()
                qr_img.save(buffer, format="PNG")
                qr_b64 = base64.b64encode(buffer.getvalue()).decode()
                
                st.markdown(
                    f"""
                    <div style='text-align: center; background: white; padding: 20px; border-radius: 10px;'>
                        <img src='data:image/png;base64,{qr_b64}' style='max-width: 200px;'>
                        <p style='margin-top: 10px; font-family: monospace; font-size: 1.2em; font-weight: bold;'>{code.code}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown("**Redemption Details:**")
                st.markdown(f"- **Amount:** ${code.amount:,.2f} {code.currency}")
                st.markdown(f"- **Verification Hash:** `{code.verification_hash}`")
                st.markdown(f"- **Valid Until:** {code.expires_at.strftime('%Y-%m-%d %H:%M')}")
                
                if code.is_valid():
                    st.success("✅ Code is VALID")
                else:
                    st.error("❌ Code EXPIRED")
        
        # Partner agents
        st.markdown("---")
        st.markdown("**Partner Redemption Network:**")
        
        agents = mode.get_partner_agents()
        cols = st.columns(len(agents))
        
        for i, agent in enumerate(agents):
            with cols[i]:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: #f5f5f5; border-radius: 8px; height: 100px;'>
                    <strong style='font-size: 0.8em;'>{agent['name']}</strong><br>
                    <small style='color: #666;'>{agent['type']}</small><br>
                    <small style='color: #999;'>{agent['locations']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.caption("Present QR code at any partner location to redeem funds without internet access.")


class BlockchainBadge:
    """Proof of Reserves blockchain verification badge"""
    
    @staticmethod
    def show_badge(proof: ProofOfReserves):
        """Display blockchain verification badge"""
        
        data = proof.get_verification_data()
        
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #1a237e, #4a148c); padding: 15px; border-radius: 12px; color: white;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-size: 1.2em; font-weight: bold;'>Proof of Reserves</span>
                    <span style='background: #4caf50; padding: 3px 10px; border-radius: 20px; font-size: 0.8em;'>✓ VERIFIED</span>
                </div>
                <hr style='border-color: rgba(255,255,255,0.2); margin: 10px 0;'>
                <div style='font-size: 0.9em;'>
                    <p style='margin: 5px 0;'><strong>Balance:</strong> {data['balance']}</p>
                    <p style='margin: 5px 0;'><strong>Chain:</strong> {data['chain']} (ID: {data['chain_id']})</p>
                    <p style='margin: 5px 0;'><strong>Vault:</strong> <code style='background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px;'>{data['short_address']}</code></p>
                    <p style='margin: 5px 0; color: #aaa;'><small>Last verified: {data['last_verified']}</small></p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.expander("🔍 View On-Chain Details"):
            st.markdown(f"**Transaction Hash:**")
            st.code(data['tx_hash'])
            
            st.markdown(f"**Vault Address:**")
            st.code(data['vault_address'])
            
            st.markdown(f"[View on BaseScan ↗]({data['explorer_url']})")
            
            if st.button("🔄 Refresh Verification"):
                proof.refresh_verification()
                st.success("✅ Verification refreshed!")
                st.rerun()
