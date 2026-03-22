import pandas as pd

df = pd.read_csv("data/raw/creditcard.csv")
print(df.columns)
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.corr())
print(df.skew())
print(df.kurt())
print(df.mode())
print(df.median())