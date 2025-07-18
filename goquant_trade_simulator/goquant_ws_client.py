import json
import time
import threading
import websocket

class WebSocketClient:
    def __init__(self, symbol="BTC-USDT-SWAP", callback=None):
        self.symbol = symbol
        self.callback = callback
        self.ws_url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{self.symbol}"
        self.ws = None
        self.thread = None
        self.is_running = False



    def _on_message(self, ws, message):
        if not message.strip():
            print("⚠️ Received empty message, skipping.")
            return

        tick_start_time = time.time()

        try:
            data = json.loads(message)
            print("✅ Parsed JSON:", data)
            if self.callback:
                tick_end_time = time.time()
                latency = tick_end_time - tick_start_time
                self.callback(data, latency)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print("⚠️ Raw message received:", repr(message))

    def _on_error(self, ws, error):
        print("❌ WebSocket error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("🔌 WebSocket closed")
        self.is_running = False

    def _on_open(self, ws):
        print("✅ WebSocket connection opened")

    def start(self):
        if self.is_running:
            return
        self.is_running = True

        def run():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            self.ws.run_forever()

        self.thread = threading.Thread(target=run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
