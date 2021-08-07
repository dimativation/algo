import numpy as np
import matplotlib.pyplot as plt

class EMA:
    def __init__(self, number_days, max_buffer_length=1, ema_init=0.0):
        self.ema = [ema_init]
        self.number_days = number_days
        self.k = 2 / (number_days + 1)
        self.max_buffer_length = max(1, max_buffer_length)

    def update(self, price_frame):
        ema = self.ema[-1]
        for price in price_frame:
            ema = price * self.k + ema * (1 - self.k)
            if len(self.ema) >= self.max_buffer_length:
                self.ema.pop(0) 
            self.ema.append(ema)


if __name__ == "__main__":
    
    time = np.arange(0, 99, 1)
    price = np.full(100, 100.0)
    ema20 = EMA(20, 200)
    ema50 = EMA(50, 200)

    ema20.update(price)
    ema50.update(price)

    plt.plot(price)
    plt.plot(ema20.ema)
    plt.plot(ema50.ema)
    plt.show()