# goquant_trade_simulator/

# main.py
import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from ui.main_ui import TradeSimulatorUI
from goquant_ws_client import WebSocketClient
from simulation import TradeSimulator

class App:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.ui = TradeSimulatorUI()
        self.simulator = TradeSimulator()

    def on_message(self, data, tick_time):
        try:
            quantity = float(self.ui.quantity_input.text())
            volatility = float(self.ui.volatility_input.text())
            fee_tier = float(self.ui.fee_tier_input.text())

            slippage, fees, impact, net_cost, latency = self.simulator.simulate(
                data, quantity, volatility, fee_tier, tick_time
            )

            self.ui.slippage_label.setText(f"Slippage: {slippage:.6f}")
            self.ui.fees_label.setText(f"Fees: {fees:.6f}")
            self.ui.market_impact_label.setText(f"Market Impact: {impact:.6f}")
            self.ui.net_cost_label.setText(f"Net Cost: {net_cost:.6f}")
            self.ui.latency_label.setText(f"Latency: {latency:.8f}s")
        except Exception as e:
            print(f"Error processing message: {e}")

    async def run_ws(self):
        url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
        client = WebSocketClient(url, self.on_message)
        await client.connect()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.create_task(self.run_ws())
        self.ui.show()
        sys.exit(self.qt_app.exec_())

if __name__ == "__main__":
    app = App()
    app.run()
