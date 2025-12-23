"""
Enhanced UI Features - Phase 4
Profile management, trip planning, and advanced features
"""

import streamlit as st
from models import UserProfile, ExitFund, Location, Contact, PayoutMethod, FundStatus
from datetime import datetime
from typing import List


class ProfileManager:
    """Manage user profiles"""

    @staticmethod
    def create_profile_wizard():
        """Interactive profile creation wizard"""
        st.subheader("👤 Create Your Profile")

        with st.form("profile_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Full Name*", placeholder="Sarah Johnson")
                email = st.text_input("Email*", placeholder="sarah@example.com")
                phone = st.text_input("Phone*", placeholder="+1-555-0100")

            with col2:
                home_country = st.selectbox(
                    "Home Country*",
                    [
                        "United States",
                        "United Kingdom",
                        "Canada",
                        "Australia",
                        "Germany",
                        "France",
                        "Other",
                    ],
                )
                passport_country = st.selectbox(
                    "Passport Country*",
                    [
                        "United States",
                        "United Kingdom",
                        "Canada",
                        "Australia",
                        "Germany",
                        "France",
                        "Other",
                    ],
                )

            st.markdown("### 📍 Current Location")
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City*", placeholder="Istanbul")
                country = st.text_input("Country*", placeholder="Turkey")
            with col2:
                latitude = st.number_input("Latitude", value=41.0082)
                longitude = st.number_input("Longitude", value=28.9784)

            submitted = st.form_submit_button("Create Profile", width="stretch")

            if submitted:
                location = Location(city, country, latitude, longitude)

                profile = UserProfile(
                    user_id=f"user_{datetime.now().timestamp()}",
                    name=name,
                    email=email,
                    phone=phone,
                    current_location=location,
                    home_country=home_country,
                    passport_country=passport_country,
                    notification_preferences={"email": True, "sms": True, "push": True},
                )

                return profile

        return None

    @staticmethod
    def create_exit_fund_wizard(user_id: str):
        """Interactive exit fund setup wizard"""
        st.subheader("💰 Set Up Exit Fund")

        with st.form("exit_fund_form"):
            st.markdown("### Fund Details")
            col1, col2 = st.columns(2)

            with col1:
                amount = st.number_input(
                    "Amount*", min_value=1000, max_value=50000, value=5000, step=500
                )
                currency = st.selectbox("Currency*", ["USD", "EUR", "GBP", "CAD"])

            with col2:
                st.markdown("**Recommended:** $5,000 - $10,000")
                st.info("Covers flights, accommodation, and emergency expenses")

            st.markdown("### Payout Methods")
            st.write("Select one or more payout methods:")

            crypto = st.checkbox("Crypto Wallet (15 min)", value=True)
            wire = st.checkbox("Wire Transfer (2-3 days)")
            cash = st.checkbox("Cash Pickup (2-4 hours)")
            mobile = st.checkbox("Mobile Money (30 min)")

            methods = []
            if crypto:
                methods.append(PayoutMethod.CRYPTO_WALLET)
                wallet = st.text_input(
                    "Wallet Address",
                    placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                )
            if wire:
                methods.append(PayoutMethod.WIRE_TRANSFER)
            if cash:
                methods.append(PayoutMethod.CASH_PICKUP)
            if mobile:
                methods.append(PayoutMethod.MOBILE_MONEY)

            st.markdown("### Emergency Contacts")
            contact_name = st.text_input("Contact Name", placeholder="John Smith")
            contact_phone = st.text_input("Contact Phone", placeholder="+1-555-0123")
            contact_email = st.text_input(
                "Contact Email", placeholder="john@example.com"
            )

            st.markdown("### Fallback Destination")
            fallback_city = st.text_input("Safe City", placeholder="Athens")
            fallback_country = st.text_input("Safe Country", placeholder="Greece")

            submitted = st.form_submit_button("Create Exit Fund", width="stretch")

            if submitted and methods:
                contacts = []
                if contact_name:
                    contacts.append(
                        Contact(
                            name=contact_name,
                            relationship="Emergency Contact",
                            phone=contact_phone,
                            email=contact_email,
                        )
                    )

                fallback = Location(fallback_city, fallback_country, 37.9838, 23.7275)

                exit_fund = ExitFund(
                    user_id=user_id,
                    amount=amount,
                    currency=currency,
                    payout_methods=methods,
                    trusted_contacts=contacts,
                    fallback_destinations=[fallback],
                    status=FundStatus.ACTIVE,
                    created_at=datetime.now(),
                )

                return exit_fund

        return None


class TripPlanner:
    """Trip planning and risk assessment"""

    @staticmethod
    def assess_destination_risk(destination: Location) -> dict:
        """Assess risk for a destination"""

        # Realistic risk database by country
        risk_database = {
            # High Risk
            "ukraine": {
                "political": 2,
                "natural": 7,
                "healthcare": 5,
                "payment": 4,
                "overall": 9,
            },
            "afghanistan": {
                "political": 1,
                "natural": 6,
                "healthcare": 3,
                "payment": 3,
                "overall": 10,
            },
            "syria": {
                "political": 1,
                "natural": 6,
                "healthcare": 3,
                "payment": 2,
                "overall": 9,
            },
            "turkey": {
                "political": 4,
                "natural": 6,
                "healthcare": 7,
                "payment": 6,
                "overall": 7,
            },
            "lebanon": {
                "political": 3,
                "natural": 6,
                "healthcare": 6,
                "payment": 3,
                "overall": 8,
            },
            # Moderate Risk
            "egypt": {
                "political": 5,
                "natural": 7,
                "healthcare": 6,
                "payment": 6,
                "overall": 6,
            },
            "pakistan": {
                "political": 4,
                "natural": 5,
                "healthcare": 5,
                "payment": 5,
                "overall": 7,
            },
            "russia": {
                "political": 5,
                "natural": 7,
                "healthcare": 7,
                "payment": 6,
                "overall": 6,
            },
            "iran": {
                "political": 3,
                "natural": 6,
                "healthcare": 6,
                "payment": 4,
                "overall": 8,
            },
            "india": {
                "political": 7,
                "natural": 6,
                "healthcare": 6,
                "payment": 7,
                "overall": 4,
            },
            "china": {
                "political": 6,
                "natural": 6,
                "healthcare": 7,
                "payment": 8,
                "overall": 5,
            },
            "brazil": {
                "political": 6,
                "natural": 7,
                "healthcare": 6,
                "payment": 7,
                "overall": 4,
            },
            "mexico": {
                "political": 5,
                "natural": 7,
                "healthcare": 6,
                "payment": 7,
                "overall": 5,
            },
            # Low Risk
            "united states": {
                "political": 9,
                "natural": 7,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "usa": {
                "political": 9,
                "natural": 7,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "united kingdom": {
                "political": 9,
                "natural": 9,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "uk": {
                "political": 9,
                "natural": 9,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "canada": {
                "political": 9,
                "natural": 8,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "germany": {
                "political": 9,
                "natural": 9,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "france": {
                "political": 8,
                "natural": 8,
                "healthcare": 9,
                "payment": 10,
                "overall": 3,
            },
            "australia": {
                "political": 9,
                "natural": 7,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "japan": {
                "political": 9,
                "natural": 5,
                "healthcare": 9,
                "payment": 10,
                "overall": 3,
            },
            "singapore": {
                "political": 9,
                "natural": 8,
                "healthcare": 9,
                "payment": 10,
                "overall": 2,
            },
            "switzerland": {
                "political": 10,
                "natural": 9,
                "healthcare": 10,
                "payment": 10,
                "overall": 1,
            },
            "norway": {
                "political": 10,
                "natural": 9,
                "healthcare": 10,
                "payment": 10,
                "overall": 1,
            },
            "greece": {
                "political": 7,
                "natural": 7,
                "healthcare": 7,
                "payment": 8,
                "overall": 3,
            },
        }

        country_key = destination.country.lower().strip()

        if country_key in risk_database:
            risk = risk_database[country_key]
            return {
                "political_stability": risk["political"],
                "natural_disaster_risk": risk["natural"],
                "healthcare_quality": risk["healthcare"],
                "payment_infrastructure": risk["payment"],
                "overall_risk": risk["overall"],
            }

        # Default for unknown countries
        return {
            "political_stability": 6,
            "natural_disaster_risk": 6,
            "healthcare_quality": 6,
            "payment_infrastructure": 6,
            "overall_risk": 5,
        }

    @staticmethod
    def show_trip_planner(fallback_city: str = "", fallback_country: str = ""):
        """Show trip planning interface"""
        st.subheader("✈️ Plan Your Trip")

        st.info("💡 Assess risk for potential travel destinations before you go")

        col1, col2 = st.columns(2)

        with col1:
            # Use fallback destination as default if provided
            destination_city = st.text_input(
                "Destination City", 
                value=fallback_city,
                placeholder="e.g., Mumbai, Tokyo, London"
            )
            destination_country = st.text_input(
                "Destination Country", 
                value=fallback_country,
                placeholder="e.g., India, Japan, UK"
            )

            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")

        with col2:
            trip_purpose = st.selectbox(
                "Trip Purpose", ["Tourism", "Business", "Study", "Work", "Family Visit"]
            )

            budget = st.number_input(
                "Budget (USD)", min_value=1000, value=5000, step=500
            )

        if st.button("📊 Assess Risk", width="stretch"):
            if destination_city and destination_country:
                destination = Location(destination_city, destination_country, 0, 0)
                risk = TripPlanner.assess_destination_risk(destination)

                st.markdown("### 📊 Risk Assessment Results")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Overall Risk", f"{risk['overall_risk']}/10")
                with col2:
                    st.metric(
                        "Political Stability", f"{risk['political_stability']}/10"
                    )
                with col3:
                    st.metric("Healthcare", f"{risk['healthcare_quality']}/10")
                with col4:
                    st.metric("Payment Systems", f"{risk['payment_infrastructure']}/10")

                st.markdown("---")

                if risk["overall_risk"] >= 7:
                    st.error(
                        f"🔴 **HIGH RISK** - {destination_city}, {destination_country}"
                    )
                    st.write("**Recommendations:**")
                    st.write("- ✅ Set up exit fund BEFORE travel")
                    st.write("- ✅ Register with embassy upon arrival")
                    st.write("- ✅ Have multiple payout methods ready")
                    st.write("- ✅ Share itinerary with emergency contacts")
                elif risk["overall_risk"] >= 4:
                    st.warning(
                        f"🟡 **MODERATE RISK** - {destination_city}, {destination_country}"
                    )
                    st.write("**Recommendations:**")
                    st.write("- ✅ Exit fund recommended")
                    st.write("- ✅ Monitor local news and alerts")
                    st.write("- ✅ Keep emergency contacts updated")
                else:
                    st.success(
                        f"🟢 **LOW RISK** - {destination_city}, {destination_country}"
                    )
                    st.write("**Recommendations:**")
                    st.write("- ✅ Standard travel precautions apply")
                    st.write("- ✅ Travel insurance recommended")
                    st.write("- ✅ Keep copies of important documents")
            else:
                st.warning("Please enter both city and country")


class NotificationCenter:
    """Manage notifications and alerts"""

    @staticmethod
    def show_notification_settings():
        """Show notification preferences"""
        st.subheader("🔔 Notification Settings")

        st.write("Choose how you want to receive alerts:")

        email_enabled = st.checkbox("Email Notifications", value=True)
        if email_enabled:
            st.text_input("Email Address", value="user@gmail.com")

        sms_enabled = st.checkbox("SMS Notifications", value=True)
        if sms_enabled:
            st.text_input("Phone Number", value="+1-999-999-9999")

        push_enabled = st.checkbox("Push Notifications", value=True)

        st.markdown("### Alert Thresholds")

        risk_threshold = st.slider(
            "Alert me when risk level reaches:",
            min_value=1,
            max_value=10,
            value=7,
            help="You'll receive alerts when risk level equals or exceeds this value",
        )

        st.info(
            f"You will receive alerts when risk level reaches {risk_threshold}/10 or higher"
        )

        if st.button("Save Settings", width="stretch"):
            st.success("✅ Notification settings saved")


class AnalyticsDashboard:
    """Analytics and insights"""

    @staticmethod
    def show_analytics():
        """Show analytics dashboard"""
        st.subheader("📊 Analytics & Insights")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Days Monitored", "45", delta="5 this week")
        with col2:
            st.metric("Alerts Received", "12", delta="-3 vs last week")
        with col3:
            st.metric("Avg Risk Level", "3.2/10", delta="-0.5")
        with col4:
            st.metric("Activations", "0", delta="0")

        st.markdown("### 📈 Risk Trend")
        st.line_chart({"Risk Level": [2, 3, 2, 4, 3, 2, 3]})

        st.markdown("### 🌍 Alert History")

        alerts_data = [
            {
                "Date": "2025-12-10",
                "Location": "Istanbul",
                "Type": "Political",
                "Severity": 6,
            },
            {
                "Date": "2025-12-05",
                "Location": "Beirut",
                "Type": "Payment",
                "Severity": 7,
            },
            {
                "Date": "2025-12-01",
                "Location": "Tokyo",
                "Type": "Natural",
                "Severity": 5,
            },
        ]

        st.dataframe(alerts_data, width="stretch")
