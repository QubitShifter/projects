import pandas as pd 
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)

n= 10000
data = []

for _ in range(n):

    amount = np.random.exponential(200)
    frequency = np.random.randint(1, 20)
    time_since_last_tx = np.random.randint(1, 1000)

    new_device = np.random.choice([0, 1], p=[0.9, 0.1])
    country_change = np.random.choice([0, 1], p=[0.95, 0.05])
    transactions_last_1min = np.random.randint(0, 20)

    fraud = 0

    # probabilistic fraud (NOT deterministic)
    score = 0

    if amount > 1000:
        score += 0.3

    if frequency > 15:
        score += 0.3

    if new_device == 1:
        score += 0.1

    if country_change == 1:
        score += 0.2

    if transactions_last_1min > 10:
        score += 0.4    

    # randomness
    if np.random.rand() < score * 0.1:
        fraud = 1
    else:
         fraud = 0

    data.append([
        amount,
        frequency,
        time_since_last_tx,
        new_device,
        country_change,
        transactions_last_1min,
        fraud
    ])

df = pd.DataFrame(data, columns=[
    "amount",
    "frequency",
    "time_since_last_tx",
    "new_device",
    "country_change",
    "transactions_last_1min",
    "class"
])

df.to_csv("data/raw/creditcard.csv", index =False)

print("CreditCard dataset generated successfully.")
