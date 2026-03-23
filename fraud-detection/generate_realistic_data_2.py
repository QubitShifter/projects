import pandas as pd 
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)

n= 10000
data = []

for _ in range(n):

    # base features
    amount = np.random.exponential(200)
    frequency = np.random.randint(1, 20)
    time_since_last_tx = np.random.randint(1, 1000)

    new_device = np.random.choice([0, 1], p=[0.9, 0.1])
    country_change = np.random.choice([0, 1], p=[0.95, 0.05])
    transactions_last_1min = np.random.randint(0, 20)
    
    #advanced features
    velocity_ration = transactions_last_1min / (frequency + 1)
    rapid_repeat = 1 if time_since_last_tx < 100 else 0

    avg_amount_7d = np.random.normal(120, 50)
    amount_deviation = amount / (avg_amount_7d + 1)

    device_trusted = np.random.choice([0, 1], p=[0.9, 0.1])
    ip_risk = np.random.choice([0, 1], p=[0.9, 0.1])
    fraud = 0#

    # pattern based fraud (deterministic)
    fraud_signal = 0

    if frequency > 12:
        fraud_signal += 1

    if transactions_last_1min > 8:
        fraud_signal += 1

    if velocity_ration > 1.5:
        fraud_signal += 1

    if amount_deviation > 3:
        fraud_signal += 1

    if new_device == 1 and country_change == 1:
        fraud_signal += 2

    if ip_risk == 1 and device_trusted == 0:
        fraud_signal += 2

    if rapid_repeat == 1:
        fraud_signal += 1
    
    # hybrid decision
    if fraud_signal >= 3:
        is_fraud = 1
    else: 
        is_fraud = 0

    # noise
    if is_fraud >= 1:
        is_fraud = np.random.choice([1, 0], p=[0.85, 0.15])
    else: 
        is_fraud = np.random.choice([0, 1], p=[0.97, 0.03])

    # append

    data.append([
        amount,
        frequency,
        time_since_last_tx,
        new_device,
        country_change,
        transactions_last_1min,
        velocity_ration,
        rapid_repeat,
        amount_deviation,
        device_trusted,
        ip_risk,
        is_fraud
    ])

df = pd.DataFrame(data, columns=[
    "amount",
    "frequency",
    "time_since_last_tx",
    "new_device",
    "country_change",
    "transactions_last_1min",
    "velocity_ration",
    "rapid_repeat",
    "amount_deviation",
    "device_trusted",
    "ip_risk",
    "class"
])

df.to_csv("data/raw/creditcard.csv", index =False)

print("CreditCard dataset generated successfully.")
print(df["class"].value_counts(normalize=True))