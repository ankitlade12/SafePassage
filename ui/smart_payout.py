"""
Smart Payout UI Component
Displays AI-ranked payout recommendations to the user.
"""

import streamlit as st
from core.liquidity_oracle import LiquidityOracle, NetworkStatus


class SmartPayoutUI:
    """UI for Smart Liquidity Oracle"""

    @staticmethod
    def show_smart_payout_options(user_profile, risk_level: int, payout_orchestrator):
        """
        Render the smart payout selection interface.
        Returns the selected transaction if initiated, else None.
        """
        st.markdown("### 🤖 Smart Liquidity Oracle")
        st.write("Real-time network analysis recommending the safest payout channels.")

        # Get Recommendations
        recommendations = LiquidityOracle.get_recommendations(user_profile, risk_level)

        if not recommendations:
            st.error("❌ No payout methods available. Please check your configuration.")
            return None

        # Display loop
        for reco in recommendations:
            # Card styling based on score
            with st.container():
                # Visual Container
                col_score, col_details, col_action = st.columns([1, 3, 1])

                with col_score:
                    st.metric("Match Score", f"{reco.match_score}%")
                    st.progress(reco.match_score / 100)

                with col_details:
                    # Title and Badges
                    method_name = reco.method.value.replace("_", " ").title()
                    badge_html = " ".join(
                        [
                            f"<span style='background-color:{'#e8f5e9' if 'Recommended' in b else '#e3f2fd'}; color:{'#2e7d32' if 'Recommended' in b else '#1565c0'}; padding:4px 10px; border-radius:16px; font-size:0.75em; font-weight:600; margin-right:5px'>{b}</span>"
                            for b in reco.badges
                        ]
                    )
                    st.markdown(
                        f"<h4 style='margin:0; padding:0;'>{method_name}</h4>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<div style='margin-top:5px; margin-bottom:10px'>{badge_html}</div>",
                        unsafe_allow_html=True,
                    )

                    # Network Status
                    status_colors = {
                        NetworkStatus.ONLINE: "#4caf50",
                        NetworkStatus.CONGESTED: "#ff9800",
                        NetworkStatus.RESTRICTED: "#ffc107",
                        NetworkStatus.OFFLINE: "#f44336",
                    }
                    status_color = status_colors.get(
                        reco.network_condition.status, "#9e9e9e"
                    )

                    st.markdown(
                        f"""
                        <div style='font-size:0.9em; color:#555;'>
                            <span style='color:{status_color}; font-weight:bold'>● {reco.network_condition.status.value}</span> 
                            &nbsp;•&nbsp; ⏱️ {reco.estimated_time} 
                            &nbsp;•&nbsp; 🏷️ {reco.estimated_fee}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if reco.reason != "Network optimal":
                        st.info(f"ℹ️ {reco.reason}")

                with col_action:
                    # Action Button
                    if reco.network_condition.status == NetworkStatus.OFFLINE:
                        st.button(
                            "Unavailable", disabled=True, key=f"btn_{reco.method.value}"
                        )
                    else:
                        if st.button(
                            "Select",
                            key=f"select_{reco.method.value}",
                            width="stretch",
                            type="primary" if reco.match_score > 80 else "secondary",
                        ):
                            # Initiate Payout Logic (matching what was in main.py)
                            transaction = payout_orchestrator.initiate_payout(
                                method=reco.method,
                                amount=user_profile.exit_fund.amount,
                                currency=user_profile.exit_fund.currency,
                            )
                            return transaction

                st.markdown("---")

        return None
