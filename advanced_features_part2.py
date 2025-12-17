"""
Advanced Features - Part 2
Features 4-7: PDF Export, Emergency Widget, Comparison Tool, Multi-Currency
"""

from io import BytesIO
from datetime import datetime
import streamlit as st


# ============================================================================
# FEATURE 4: PDF Export for Exit Checklist
# ============================================================================

class PDFExporter:
    """Export exit checklist to PDF"""
    
    @staticmethod
    def create_simple_pdf(checklist, user_profile):
        """Create simple text-based PDF"""
        from export_features import ExportManager
        
        # Use existing text export and convert to downloadable format
        text_content = ExportManager.export_checklist_text(checklist)
        
        return text_content.encode('utf-8')
    
    @staticmethod
    def show_pdf_export_button(checklist, user_profile):
        """Show PDF export button"""
        if checklist:
            st.markdown("### 📄 Export Checklist")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Text export
                text_content = PDFExporter.create_simple_pdf(checklist, user_profile)
                st.download_button(
                    label="📥 Download as Text",
                    data=text_content,
                    file_name=f"exit_checklist_{user_profile.name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # JSON export (for backup)
                import json
                checklist_data = {
                    "user": user_profile.name,
                    "location": str(checklist.location),
                    "generated": checklist.generated_at.isoformat(),
                    "critical_items": [{"title": item.title, "description": item.description} 
                                      for item in checklist.get_critical_items()],
                    "routes": [{"method": route.method, "from": str(route.from_location), 
                               "to": str(route.to_location), "time": route.estimated_time}
                              for route in checklist.safe_routes]
                }
                
                st.download_button(
                    label="📥 Download as JSON",
                    data=json.dumps(checklist_data, indent=2),
                    file_name=f"exit_checklist_{user_profile.name.replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )


# ============================================================================
# FEATURE 6: Emergency Contacts Widget
# ============================================================================

class EmergencyWidget:
    """Quick access emergency contacts widget"""
    
    @staticmethod
    def show_emergency_widget(user_profile):
        """Display emergency contacts widget in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("🆘 Emergency Contacts")
        
        # SOS Button
        if st.sidebar.button("🚨 SOS - ACTIVATE NOW", use_container_width=True, type="primary"):
            st.sidebar.warning("⚠️ Are you sure? This will activate your emergency protocol.")
            if st.sidebar.button("✅ Yes, Activate Emergency", use_container_width=True):
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
# FEATURE 9: Destination Comparison Tool
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
        
        if st.button("📊 Compare All", use_container_width=True) and len(destinations) >= 2:
            from enhanced_ui import TripPlanner
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
                "Recommendation": []
            }
            
            for city, country in destinations:
                loc = Location(city, country, 0, 0)
                risk = TripPlanner.assess_destination_risk(loc)
                
                comparison_data["Destination"].append(f"{city}, {country}")
                comparison_data["Overall Risk"].append(f"{risk['overall_risk']}/10")
                comparison_data["Political"].append(f"{risk['political_stability']}/10")
                comparison_data["Healthcare"].append(f"{risk['healthcare_quality']}/10")
                comparison_data["Payment"].append(f"{risk['payment_infrastructure']}/10")
                
                if risk['overall_risk'] >= 7:
                    comparison_data["Recommendation"].append("🔴 High Risk")
                elif risk['overall_risk'] >= 4:
                    comparison_data["Recommendation"].append("🟡 Moderate")
                else:
                    comparison_data["Recommendation"].append("🟢 Low Risk")
            
            st.dataframe(comparison_data, use_container_width=True)
            
            # Best/worst
            risks = [TripPlanner.assess_destination_risk(Location(c, co, 0, 0))['overall_risk'] 
                    for c, co in destinations]
            best_idx = risks.index(min(risks))
            worst_idx = risks.index(max(risks))
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ **Safest:** {destinations[best_idx][0]}, {destinations[best_idx][1]}")
            with col2:
                st.error(f"⚠️ **Highest Risk:** {destinations[worst_idx][0]}, {destinations[worst_idx][1]}")


# ============================================================================
# FEATURE 14: Multi-Currency Support
# ============================================================================

class CurrencyManager:
    """Multi-currency support and conversion"""
    
    # Simplified exchange rates (in production, use real API)
    EXCHANGE_RATES = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "INR": 83.12,
        "JPY": 149.50,
        "CAD": 1.36,
        "AUD": 1.52,
        "CHF": 0.88
    }
    
    @staticmethod
    def convert(amount, from_currency, to_currency):
        """Convert between currencies"""
        if from_currency == to_currency:
            return amount
        
        # Convert to USD first, then to target currency
        usd_amount = amount / CurrencyManager.EXCHANGE_RATES.get(from_currency, 1.0)
        target_amount = usd_amount * CurrencyManager.EXCHANGE_RATES.get(to_currency, 1.0)
        
        return round(target_amount, 2)
    
    @staticmethod
    def show_currency_converter():
        """Show currency converter widget"""
        st.subheader("💱 Currency Converter")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            amount = st.number_input("Amount", min_value=0.0, value=5000.0, step=100.0)
        
        with col2:
            from_curr = st.selectbox("From", list(CurrencyManager.EXCHANGE_RATES.keys()), index=0)
        
        with col3:
            to_curr = st.selectbox("To", list(CurrencyManager.EXCHANGE_RATES.keys()), index=4)
        
        if amount > 0:
            converted = CurrencyManager.convert(amount, from_curr, to_curr)
            
            st.success(f"💰 **{amount:,.2f} {from_curr}** = **{converted:,.2f} {to_curr}**")
            
            # Show rate
            rate = CurrencyManager.EXCHANGE_RATES[to_curr] / CurrencyManager.EXCHANGE_RATES[from_curr]
            st.caption(f"Exchange rate: 1 {from_curr} = {rate:.4f} {to_curr}")
    
    @staticmethod
    def show_exit_fund_in_currencies(exit_fund):
        """Show exit fund value in multiple currencies"""
        if exit_fund:
            st.markdown("### 💰 Your Exit Fund in Different Currencies")
            
            currencies = ["USD", "EUR", "GBP", "INR", "JPY"]
            cols = st.columns(len(currencies))
            
            for i, curr in enumerate(currencies):
                with cols[i]:
                    converted = CurrencyManager.convert(
                        exit_fund.amount,
                        exit_fund.currency,
                        curr
                    )
                    st.metric(curr, f"{converted:,.0f}")


# Advanced features Part 2 module loaded
