import pandas as pd
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)

n = 10000

df = pd.DataFrame({
    "Time": np.random.randint(0, 86400, n),
    "Amount": np.random.exponential(100, n),
    "V1": np.random.randn(n),
    "V2": np.random.randn(n),
    "V3": np.random.randn(n),
    "Class": np.random.choice([0, 1], n, p=[0.98, 0.02])
})

df.to_csv("data/raw/creditcard.csv", index=False)

print("Fake dataset created.")