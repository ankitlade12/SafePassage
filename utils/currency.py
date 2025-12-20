"""
Currency Management
"""

import streamlit as st


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
        "CHF": 0.88,
    }

    @staticmethod
    def convert(amount, from_currency, to_currency):
        """Convert between currencies"""
        if from_currency == to_currency:
            return amount

        # Convert to USD first, then to target currency
        usd_amount = amount / CurrencyManager.EXCHANGE_RATES.get(from_currency, 1.0)
        target_amount = usd_amount * CurrencyManager.EXCHANGE_RATES.get(
            to_currency, 1.0
        )

        return round(target_amount, 2)

    @staticmethod
    def show_currency_converter():
        """Show currency converter widget"""
        st.subheader("💱 Currency Converter")

        col1, col2, col3 = st.columns(3)

        with col1:
            amount = st.number_input("Amount", min_value=0.0, value=5000.0, step=100.0)

        with col2:
            from_curr = st.selectbox(
                "From", list(CurrencyManager.EXCHANGE_RATES.keys()), index=0
            )

        with col3:
            to_curr = st.selectbox(
                "To", list(CurrencyManager.EXCHANGE_RATES.keys()), index=4
            )

        if amount > 0:
            converted = CurrencyManager.convert(amount, from_curr, to_curr)

            st.success(
                f"💰 **{amount:,.2f} {from_curr}** = **{converted:,.2f} {to_curr}**"
            )

            # Show rate
            rate = (
                CurrencyManager.EXCHANGE_RATES[to_curr]
                / CurrencyManager.EXCHANGE_RATES[from_curr]
            )
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
                        exit_fund.amount, exit_fund.currency, curr
                    )
                    st.metric(curr, f"{converted:,.0f}")
