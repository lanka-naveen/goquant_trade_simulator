import numpy as np

class AlmgrenChrissModel:
    def __init__(self, 
                 quantity,            # Total shares to trade (Q)
                 volatility,          # σ: daily return volatility
                 liquidity,           # V: daily volume (proxy for liquidity)
                 risk_aversion=1e-6,  # λ: trader's risk aversion
                 num_intervals=10,    # T: number of time steps (uniform)
                 impact_factor=0.1,   # γ: permanent impact coefficient
                 temporary_impact=0.2 # η: temporary impact coefficient
                ):
        self.Q = quantity
        self.sigma = volatility
        self.V = liquidity
        self.lambda_ = risk_aversion
        self.T = num_intervals
        self.gamma = impact_factor
        self.eta = temporary_impact

    def calculate(self):
        """
        Calculates expected market impact cost using a simplified
        Almgren-Chriss model.
        """
        dt = 1 / self.T
        x = np.linspace(self.Q, 0, self.T + 1)  # Linear schedule
        v = -np.diff(x)                         # Volume per interval

        expected_cost = 0
        variance = 0

        for i in range(self.T):
            temp_cost = self.eta * (v[i] ** 2) / self.V
            perm_cost = self.gamma * v[i] * (x[i] - self.Q / 2) / self.V
            expected_cost += temp_cost + perm_cost

            variance += (self.sigma ** 2) * (x[i] ** 2) * dt

        total_cost = expected_cost + self.lambda_ * variance
        return total_cost
