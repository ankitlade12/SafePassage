"""
Theme Management
"""

import streamlit as st


class ThemeManager:
    """Manage light/dark theme"""

    @staticmethod
    def get_dark_mode_css():
        """Get dark mode CSS"""
        return """
        <style>
            /* Dark mode styles */
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stSidebar {
                background-color: #262730;
            }
            .stSidebar [data-testid="stMarkdownContainer"] {
                color: #fafafa;
            }
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #fafafa;
            }
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #fafafa !important;
            }
            /* Info boxes */
            .stAlert {
                background-color: #1e2130;
                color: #fafafa;
            }
            /* Buttons */
            .stButton>button {
                background-color: #3d4050;
                color: #fafafa;
                border: 1px solid #4a4d5e;
            }
            .stButton>button:hover {
                background-color: #4a4d5e;
                border-color: #5a5d6e;
            }
            /* Inputs */
            .stTextInput>div>div>input,
            .stSelectbox>div>div>select {
                background-color: #262730;
                color: #fafafa;
                border-color: #4a4d5e;
            }
            /* Tables */
            .dataframe {
                background-color: #1e2130;
                color: #fafafa;
            }
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: #262730;
                color: #fafafa;
            }
        </style>
        """

    @staticmethod
    def show_theme_toggle():
        """Show theme toggle in sidebar"""
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = False

        st.sidebar.markdown("---")
        st.sidebar.subheader("🎨 Theme")

        theme_option = st.sidebar.radio(
            "Select Theme:",
            ["☀️ Light Mode", "🌙 Dark Mode"],
            index=1 if st.session_state.dark_mode else 0,
            key="theme_selector",
        )

        # Update session state
        st.session_state.dark_mode = theme_option == "🌙 Dark Mode"

    @staticmethod
    def apply_dark_mode():
        """Apply dark mode CSS if enabled"""
        if st.session_state.get("dark_mode", False):
            st.markdown(ThemeManager.get_dark_mode_css(), unsafe_allow_html=True)
