import pandas as pd


# clean data from csv file, drop missing data , etc...
def transform_sales(df: pd.DataFrame) -> pd.DataFrame:

    df = df.dropna(subset=["order_id", "amount"])
    df["order_id"] = df["order_id"].astype(int)
    df["amount"] = df["amount"].astype(float)


    def usd_to_eur(row):
        if str(row.get("currency")).upper() == "USD":
            return row["amount"] * 0.85
        return row["amount"]

    df["amount_eur"] = df.apply(usd_to_eur, axis=1)
    return df
