import numpy as np
from scipy.stats import norm
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- Engine --- #
def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + (sigma**2) / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    cdf_d1 = norm.cdf(d1)
    cdf_d2 = norm.cdf(d2)
    pdf_d1 = norm.pdf(d1)

    # Option's prices
    call_price = cdf_d1 * S - cdf_d2 * K * np.exp(-r * T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    # Greeks
    delta_call = cdf_d1
    delta_put = -norm.cdf(-d1)

    gamma = pdf_d1  / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T)
    
    theta_call = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * cdf_d2) / 365
    theta_put = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    return call_price, put_price, delta_call, delta_put, gamma, vega, theta_call, theta_put


# --- Streamlit --- #

st.set_page_config(page_title="Options calculator", layout="wide")
st.title("Black-Scholes Option Calculator")

st.sidebar.header("Market Parameteres")
ticker = st.sidebar.text_input("Stock's ticker", value="AAPL")
vol_period = st.sidebar.selectbox("Volatility period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)


# --- Downloading Data --- #

def load_ticker(t, p):
    return yf.Ticker(t).history(period=p)

try: 
    data = load_ticker(ticker, vol_period)
    S = data['Close'].iloc[-1]

    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    sigma = log_returns.std() * np.sqrt(252)

    st.sidebar.subheader("Option parameters")
    K = st.sidebar.slider("Strike Price (K)", float(S*0.7), float(S*1.3), float(S), 0.1)
    T_days = st.sidebar.slider("Days to expiration", 1, 730, 30)
    r_pct = st.sidebar.slider("Risk free rate (%)", 0.0, 10.0, value=3.0, step=0.05)

    T = T_days / 365
    r = r_pct / 100

    # --- Calculations --- # 

    c_p, p_p, c_d, p_d, gam, veg, c_t, p_t = black_scholes(S, K, T, r, sigma)

    st.subheader("Option pricing & Greeks")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cena Call / Put", f"${c_p:.2f} / ${p_p:.2f}")
    with col2:
        st.metric("Delta Call / Put", f"{c_d:.3f} / {p_d:.3f}")
    with col3:
        st.metric("Gamma | Vega", f"{gam:.4f} | {veg:.2f}")
    with col4:
        st.metric("Theta Call / Put", f"{c_t:.4f} / {p_t:.4f}")

    st.divider()


    # --- Visualisation --- #
    view_col1, view_col2 = st.columns(2)

    with view_col1:
        st.subheader("Stock History")
        fig_stock = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=ticker
        )])
        fig_stock.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_stock, use_container_width=True)

    with view_col2:
        st.subheader("Profit and Loss (P&L)")
        
        
        opt_type = st.radio("Option's type:", ("Call", "Put"), horizontal=True)
        position = st.radio("Position:", ("Buy (Long)", "Sell (Short)"), horizontal=True)

        sT = np.linspace(S * 0.8, S * 1.2, 100)

                
        if opt_type == "Call":
            pnl = np.maximum(sT - K, 0) - c_p
            base_color = "#00ff00"
        else:
            pnl = np.maximum(K - sT, 0) - p_p
            base_color = "#ff0000"

        
        if position == "Sprzedaż (Short)":
            pnl = -pnl
            color = "#ffaa00" if opt_type == "Call" else "#00aaff" 
        else:
            color = base_color

        fig_pnl = go.Figure()
        fig_pnl.add_trace(go.Scatter(x=sT, y=pnl, name="P&L", line=dict(color=color, width=3)))
        fig_pnl.add_hline(y=0, line_dash="dash", line_color="white")
        fig_pnl.add_vline(x=K, line_dash="dot", line_color="yellow")
        fig_pnl.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20), xaxis_title="Price at expiration date", yaxis_title="Profit / Loss")
        st.plotly_chart(fig_pnl, use_container_width=True)

except Exception as e:
    st.error(f"Error while downloading data for '{ticker}': {e}")