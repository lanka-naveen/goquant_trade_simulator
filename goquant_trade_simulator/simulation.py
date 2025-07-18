import time
import numpy as np
from models.market_impact import AlmgrenChrissModel
from models.slippage_model import SlippageModel
from models.maker_taker_model import MakerTakerModel

class TradeSimulator:
    def __init__(self):
        self.orderbook = None
        self.latest_metrics = {}
        self.model_slippage = SlippageModel()
        self.model_maker_taker = MakerTakerModel()
        self.almgren_chriss = None
        self.trades = []

        # ✅ Dummy training with enough samples for both classes
        self.model_slippage.train([
            [1000, 0.01],
            [1200, 0.015],
            [900, 0.012]
        ], [0.05, 0.06, 0.04])

        self.model_maker_taker.train([
            [0.01, 1000],
            [0.02, 900],
            [0.03, 800],
            [0.01, 500],
            [0.02, 600],
            [0.03, 400],
        ], [1, 1, 1, 0, 0, 0])

    def process_orderbook(self, data):
        if 'bids' in data and 'asks' in data:
            self.orderbook = data

    def run_simulation(self, quantity, volatility, fee_tier):
        if not self.orderbook or not self.orderbook['bids'] or not self.orderbook['asks']:
            return

        start_time = time.time()

        best_bid = float(self.orderbook['bids'][0][0])
        best_ask = float(self.orderbook['asks'][0][0])
        mid_price = (best_bid + best_ask) / 2
        liquidity = sum(float(bid[1]) for bid in self.orderbook['bids'][:5])

        # Calculate slippage
        slippage = self.model_slippage.predict([quantity, volatility])

        # Calculate market impact using Almgren-Chriss
        self.almgren_chriss = AlmgrenChrissModel(volatility, quantity, liquidity)
        impact = self.almgren_chriss.calculate()

        # Calculate fees
        fees = quantity * fee_tier

        # Maker/Taker prediction
        probs = self.model_maker_taker.predict([volatility, quantity])
        maker_prob = probs["maker_probability"]
        taker_prob = probs["taker_probability"]


        # Net cost = base cost + slippage + impact + fees
        net_cost = quantity + (quantity * slippage) + (quantity * impact) + fees

        latency = time.time() - start_time

        # Save result
        self.latest_metrics = {
            "price": mid_price,
            "qty": quantity,
            "slippage": slippage,
            "fees": fees,
            "impact": impact,
            "net_cost": net_cost,
            "maker_prob": maker_prob,
            "taker_prob": taker_prob,
            "latency": latency
        }

        self.trades.append({
            "price": mid_price,
            "quantity": quantity,
            "timestamp": time.time()
        })

    def get_trades(self):
        return self.trades[-20:]

    def get_latest_metrics(self):
        return self.latest_metrics if self.latest_metrics else None
