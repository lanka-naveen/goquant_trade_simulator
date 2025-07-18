from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QComboBox, QApplication
)
from PyQt5.QtCore import QTimer
from goquant_ws_client import WebSocketClient
from simulation import TradeSimulator

class TradeSimulatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoQuant Trade Simulator")
        self.setGeometry(100, 100, 800, 500)

        self.simulator = TradeSimulator()
        self.websocket = WebSocketClient(symbol='BTC-USDT-SWAP', callback=self.on_data)

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_output)
        self.timer.start(1000)

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left panel - Inputs
        input_layout = QVBoxLayout()

        self.asset_label = QLabel("Asset:")
        self.asset_combo = QComboBox()
        self.asset_combo.addItems(["BTC-USDT-SWAP"])  # Add more if needed
        input_layout.addWidget(self.asset_label)
        input_layout.addWidget(self.asset_combo)

        self.quantity_input = QLineEdit("100")
        input_layout.addWidget(QLabel("Quantity (USD):"))
        input_layout.addWidget(self.quantity_input)

        self.volatility_input = QLineEdit("0.01")
        input_layout.addWidget(QLabel("Volatility:"))
        input_layout.addWidget(self.volatility_input)

        self.fee_tier_input = QLineEdit("0.001")
        input_layout.addWidget(QLabel("Fee Tier:"))
        input_layout.addWidget(self.fee_tier_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        input_layout.addWidget(self.connect_button)

        self.status_label = QLabel("WebSocket Status: Disconnected")
        input_layout.addWidget(self.status_label)

        # Right panel - Outputs
        output_layout = QVBoxLayout()
        self.output_view = QTextEdit()
        self.output_view.setReadOnly(True)
        output_layout.addWidget(QLabel("Simulation Output:"))
        output_layout.addWidget(self.output_view)

        # Store layout references for simulation update
        self.output_labels = {
            "slippage": QLabel("Slippage: -"),
            "fees": QLabel("Fees: -"),
            "impact": QLabel("Market Impact: -"),
            "net_cost": QLabel("Net Cost: -"),
            "maker_taker": QLabel("Maker/Taker: -"),
            "latency": QLabel("Latency: -"),
        }
        for label in self.output_labels.values():
            output_layout.addWidget(label)

        main_layout.addLayout(input_layout, 1)
        main_layout.addLayout(output_layout, 2)
        self.setLayout(main_layout)

    def toggle_connection(self):
        if self.websocket.is_running:
            self.websocket.stop()
            self.status_label.setText("WebSocket Status: Disconnected")
            self.connect_button.setText("Connect")
        else:
            self.websocket.start()
            self.status_label.setText("WebSocket Status: Connected")
            self.connect_button.setText("Disconnect")

    def on_data(self, orderbook,latency):
        # Get latest parameters from UI
        try:
            quantity = float(self.quantity_input.text())
            volatility = float(self.volatility_input.text())
            fee_tier = float(self.fee_tier_input.text())

            self.simulator.process_orderbook(orderbook)
            self.simulator.run_simulation(quantity, volatility, fee_tier)
        except ValueError as e:
            print("Invalid input in UI:", e)

    def update_output(self):
        results = self.simulator.get_latest_metrics()
        if results:
            self.output_labels["slippage"].setText(f"Slippage: {results['slippage']:.6f}")
            self.output_labels["fees"].setText(f"Fees: {results['fees']:.6f}")
            self.output_labels["impact"].setText(f"Market Impact: {results['impact']:.6f}")
            self.output_labels["net_cost"].setText(f"Net Cost: {results['net_cost']:.6f}")
            self.output_labels["maker_taker"].setText(f"Maker/Taker Prob: {float(results['maker_prob']):.2%} / {float(results['taker_prob']):.2%}")

            self.output_labels["latency"].setText(f"Latency: {results['latency']:.6f} sec")

            # Optional log panel
            self.output_view.append(f"Price: {results['price']} | Qty: {results['qty']}")

