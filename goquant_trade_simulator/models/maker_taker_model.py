import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

class MakerTakerModel:
    def __init__(self):
        self.scaler = StandardScaler()
        base_model = LogisticRegression(
            solver='lbfgs',
            max_iter=1000,
            class_weight='balanced'
        )
        # CalibratedClassifier improves probability estimates
        self.model = CalibratedClassifierCV(base_model, cv=3)

    def train(self, X, y):
        """
        X: 2D numpy array (samples × features)
        y: 1D array of labels: 0 for maker, 1 for taker
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, features):
        """
        features: 1D array of features for prediction
        returns: (maker_prob, taker_prob)
        """
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        probs = self.model.predict_proba(features_scaled)[0]
        return {
            "maker_probability": float(probs[0]),
            "taker_probability": float(probs[1])
        }
