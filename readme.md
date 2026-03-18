# 📈 Black-Scholes Option Calculator

An interactive web application built with **Streamlit** that allows users to price European options using the Black-Scholes model. The tool fetches real-time market data, calculates historical volatility, and provides a comprehensive analysis of Option Greeks.

## Features

* **Real-time Data:** Integration with `yfinance` to fetch current stock prices and historical data.
* **Dynamic Volatility:** Automatically calculates historical volatility based on the selected look-back period (1mo to 2y).
* **Full Option Greeks:** Calculates **Delta, Gamma, Vega, and Theta** for both Call and Put options.
* **Interactive Visualizations:**
    * **Candlestick Chart:** Historical price action of the underlying asset.
    * **P&L Projection:** Interactive Profit/Loss diagrams at expiration for Long/Short and Call/Put positions.
* **User-friendly Interface:** Sidebar controls for adjusting strike price, expiry, and risk-free rates.

## Tech Stack

* **Language:** Python
* **UI Framework:** [Streamlit](https://streamlit.io/)
* **Data Science:** NumPy, SciPy
* **Financial Data:** yfinance
* **Visualization:** Plotly

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/dawidtr28/Black-Scholes.git](https://github.com/dawidtr28/Black-Scholes.git)
   cd Black-Scholes