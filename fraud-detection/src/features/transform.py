def transform_transaction(transaction):
    return[
        transaction.get("amount", 0),
        transaction.get("frequency", 0),
        transaction.get("time_since_last_tx", 0),
        int(transaction.get("new_device", False)),
        int(transaction.get("country_change", False)),
        transaction.get("transactions_last_1min", 0),
    ]