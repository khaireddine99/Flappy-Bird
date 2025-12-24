import random

class NeuralNetwrok:
    def __init__(self, weights = None):
        if weights is None:
            self.weights = [
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ]
        else:
            self.weights = weights
    
    def forward(self, inputs):
        x1, x2 = inputs
        w1, w2, b = self.weights

        output = (w1 * x1) + (w2 * x2) + b
        return output > 0
