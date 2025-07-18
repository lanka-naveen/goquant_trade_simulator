# goquant_trade_simulator
A real-time trade simulator using OKX L2 orderbook data. Built with PyQt5, it estimates slippage, market impact, fees, and latency using models like Linear Regression, Logistic Regression, and Almgren-Chriss. Developed for the GoQuant recruitment assignment.
# 📈 GoQuant High-Performance Trade Simulator

A real-time trade simulator using OKX L2 orderbook data. Built with PyQt5, it estimates slippage, market impact, fees, and latency using models like Linear Regression, Logistic Regression, and Almgren-Chriss. Developed as part of the GoQuant recruitment assignment.

---

## 🚀 Features

- 🔌 Live WebSocket stream from OKX (BTC-USDT-SWAP)
- 📊 Simulates slippage, market impact, fees, and latency
- 🧠 Quant models:  
  - **Slippage Model** – Linear Regression  
  - **Market Impact** – Almgren-Chriss  
  - **Maker/Taker** – Logistic Regression  
- 🖥️ Responsive UI using PyQt5
- 🧵 Threaded WebSocket for smooth updates

---

## 🧱 Architecture

[UI (PyQt5)] <--> [Trade Simulator] <--> [WebSocket Connector]
|
v
[Quant Models & Metrics]

markdown
Copy
Edit

**Modules Overview**:
- `main_ui.py`: UI controller and layout
- `trade_simulator.py`: Core simulation logic
- `models/`: Contains ML and quant models
- `goquant_ws_client.py`: WebSocket handler

---

## 📦 Installation

```bash
git clone https://github.com/your-username/goquant-trade-simulator.git
cd goquant-trade-simulator
pip install -r requirements.txt
python main.py
Requirements:

PyQt5

websocket-client

numpy

scikit-learn

🎯 UI Overview
Left Panel (Inputs):

Exchange: OKX

Asset: BTC-USDT-SWAP

Order Type: Market

Quantity, Volatility, Fee Tier

Right Panel (Outputs):

Slippage (%)

Market Impact (%)

Fees (USD)

Net Cost (USD)

Maker/Taker Probabilities

Latency (s)

📊 Performance Metrics
Benchmarked for:

Data ingestion latency

Processing latency

UI update latency

Profiling with time.time() for per-tick analysis.

✅ Error Handling
Auto-reconnect on WebSocket failure

Safe JSON parsing

Input validation on UI

📽️ Demo
A video walkthrough is included in the submission for explanation and usage.

