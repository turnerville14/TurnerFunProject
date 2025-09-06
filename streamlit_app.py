import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Stock Valuation & Investment Advisor 📊", layout="wide")

# Title
st.title("📈 Stock Valuation & Investment Advisor")
st.markdown("Analyze a stock's historical performance and get a valuation-based recommendation.")

# Input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)", "AAPL")

# Cached data fetch (only serializable objects)
@st.cache_data
def get_data(ticker):
    stock = yf.Ticker(ticker)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)
    price_data = stock.history(start=start_date, end=end_date)
    dividends = stock.dividends
    return price_data, dividends

# Get cached data
price_data, dividends = get_data(ticker)

# Get uncached stock object
stock = yf.Ticker(ticker)

# Section: Price Chart
st.subheader("📉 Historical Price (5 Years)")
st.line_chart(price_data['Close'])

# Section: Dividend History
st.subheader("💰 Dividend History")
if not dividends.empty:
    st.bar_chart(dividends)
else:
    st.info("No dividend data available for this stock.")

# Section: Valuation Metrics
st.subheader("📊 Valuation Analysis")

# PE Ratio
try:
    pe_ratio = stock.info['trailingPE']
    st.metric("Trailing P/E Ratio", f"{pe_ratio:.2f}")
except:
    st.warning("P/E Ratio not available.")

# Dividend Discount Model (DDM)
if not dividends.empty:
    avg_dividend = dividends[-5:].mean()
    growth_rate = (dividends[-1] / dividends[-5] - 1) if len(dividends) >= 5 else 0.05
    required_return = 0.10  # Assume 10% required return
    try:
        intrinsic_value = avg_dividend * (1 + growth_rate) / (required_return - growth_rate)
        current_price = price_data['Close'][-1]
        st.metric("Intrinsic Value (DDM)", f"${intrinsic_value:.2f}")
        st.metric("Current Price", f"${current_price:.2f}")

        # Recommendation
        if intrinsic_value > current_price * 1.1:
            st.success("✅ Recommendation: BUY — Stock appears undervalued.")
            st.markdown(f"**Reason:** Intrinsic value (${intrinsic_value:.2f}) is significantly higher than current price (${current_price:.2f}).")
        elif intrinsic_value < current_price * 0.9:
            st.error("❌ Recommendation: SELL — Stock appears overvalued.")
            st.markdown(f"**Reason:** Intrinsic value (${intrinsic_value:.2f}) is significantly lower than current price (${current_price:.2f}).")
        else:
            st.warning("⚖️ Recommendation: HOLD — Stock is fairly valued.")
            st.markdown(f"**Reason:** Intrinsic value (${intrinsic_value:.2f}) is close to current price (${current_price:.2f}).")
    except:
        st.warning("Unable to calculate intrinsic value due to missing data.")
else:
    st.warning("Dividend data insufficient for DDM valuation.")

# Section: EPS & Revenue Growth
st.subheader("📈 EPS & Revenue Growth")
try:
    eps_history = stock.earnings
    if not eps_history.empty:
        st.line_chart(eps_history[['Earnings', 'Revenue']])
        st.markdown("**Interpretation:** Rising EPS and Revenue suggest improving profitability and business growth.")
    else:
        st.info("EPS and Revenue data not available.")
except:
    st.warning("Unable to fetch EPS and Revenue data.")

# Section: Earnings Calendar
st.subheader("🗓️ Upcoming Earnings Date")
try:
    earnings_date = stock.calendar.loc['Earnings Date'][0]
    st.metric("Next Earnings Report", earnings_date.strftime("%Y-%m-%d"))
    st.markdown("**Tip:** Earnings reports often cause price volatility. Consider timing your entry/exit accordingly.")
except:
    st.info("Earnings date not available.")

# Section: Analyst Ratings
st.subheader("🧠 Analyst Recommendations")
try:
    recs = stock.recommendations
    if not recs.empty:
        latest_recs = recs.tail(10)
        st.dataframe(latest_recs[['Firm', 'To Grade', 'From Grade', 'Action']])
        st.markdown("**Note:** Analyst upgrades/downgrades can influence investor sentiment.")
    else:
        st.info("No recent analyst recommendations available.")
except:
    st.warning("Unable to fetch analyst ratings.")

# Footer
st.markdown("---")
st.caption("Powered by Yahoo Finance & Streamlit • Not financial advice")