"""
Guided Tour System
Interactive walkthrough for first-time users
"""

import streamlit as st


class GuidedTour:
    """Manage guided tour for new users"""
    
    @staticmethod
    def show_welcome():
        """Show welcome message"""
        if 'tour_completed' not in st.session_state:
            st.session_state.tour_completed = False
        
        if not st.session_state.tour_completed:
            with st.expander("👋 Welcome to Safe-Passage!", expanded=True):
                st.markdown("""
                ### Quick Start Guide
                
                **Safe-Passage** helps travelers prepare for emergencies with:
                
                1. **💰 Pre-funded Exit Fund** - Set up emergency liquidity before you travel
                2. **📊 Real-Time Risk Monitoring** - Track alerts for your location
                3. **🚨 One-Tap Emergency Activation** - Instant access to funds when crisis hits
                4. **📋 Personalized Exit Plan** - Step-by-step checklist for safe evacuation
                
                **Try the Demo:**
                1. Click "🚨 Trigger Crisis" in the sidebar
                2. Go to "Emergency" tab
                3. Select a payout method
                4. Click "Activate Emergency Protocol"
                5. Watch the real-time simulation!
                
                ---
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Start Tour", use_container_width=True):
                        st.session_state.show_tour = True
                        st.rerun()
                with col2:
                    if st.button("⏭️ Skip Tour", use_container_width=True):
                        st.session_state.tour_completed = True
                        st.rerun()
    
    @staticmethod
    def show_feature_tooltip(feature_name: str, description: str):
        """Show tooltip for a feature"""
        st.info(f"💡 **{feature_name}**: {description}")
    
    @staticmethod
    def show_tour_step(step_number: int, total_steps: int, title: str, content: str):
        """Show a tour step"""
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 4px solid #2196F3;">
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Step {step_number} of {total_steps}</p>
            <h4 style="margin: 5px 0;">{title}</h4>
            <p style="margin: 5px 0;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
