from generate_realistic_data_2 import amount_deviation, device_trusted, frequency, rapid_repeat, time_since_last_tx, transactions_last_1min


def transform_transaction(transaction: dict):
    amount = transaction["amount"]
    frequency = transaction["frequency"]
    time_since_last_tx = transaction["time_since_last_tx"]
    new_device = int(transaction["new_device"])
    country_change = int(transaction["country_change"])
    transactions_last_1min = transaction["transactions_last_1min"]
    
    velocity_ratio = transactions_last_1min / (frequency + 1)
    rapid_repeat = 1 if time_since_last_tx < 10 else 0

    #user baseline
    avg_amount_7d = 120 # const for now
    amount_deviation = amount / (avg_amount_7d + 1)
    
    device_trusted = 0 if new_device == 1 else 0
    ip_risk = 1 if country_change == 1 else 0
    
    # feature's vector
    features = {
        "amount": amount,
        "frequency": frequency,
        "time_since_last_tx": time_since_last_tx,
        "new_device": new_device,
        "country_change": country_change,
        "transactions_last_1min": transactions_last_1min,
        "velocity_ratio": velocity_ratio,
        "rapid_repeat": rapid_repeat,
        "amount_deviation": amount_deviation,
        "device_trusted": device_trusted,
        "ip_risk": ip_risk


    }

    return features