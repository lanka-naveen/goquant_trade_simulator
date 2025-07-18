import numpy as np
from sklearn.linear_model import LinearRegression, QuantileRegressor
from sklearn.preprocessing import StandardScaler

class SlippageModel:
    def __init__(self, model_type="linear", quantile=0.5):
        self.model_type = model_type
        self.scaler = StandardScaler()

        if model_type == "linear":
            self.model = LinearRegression()
        elif model_type == "quantile":
            self.model = QuantileRegressor(quantile=quantile, solver="highs")
        else:
            raise ValueError("Unsupported model type. Choose 'linear' or 'quantile'.")

    def train(self, X, y):
        X = np.array(X)
        y = np.array(y)

        # Feature scaling
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, features):
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)
        return float(prediction[0])
