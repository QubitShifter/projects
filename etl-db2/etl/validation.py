import logging
import pandas as pd

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

def validate_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    validation of the transformed data.
     - order_id should be positive
     -ammount should not be negative
     -currency must be non- empty
    """

    errors = []

    if df["order_id"].le(0).any():
        bad_ids = df.loc[df["order_id"] <= 0, "order_id"].tolist()
        errors.append(f"Negative order_id values: {bad_ids}")

    if df["amount"].lt(0).any():
        bad_rows = df.loc[df["amount"] < 0, ["order_id", "amount"]].to_dict("records")
        errors.append(f"Negative amounts: {bad_rows}")

    if df["currency"].isna().any() or (df["currency"].astype(str).str.strip() == "").any():
        errors.append("Empty currency values found")

    if errors:
        for e in errors:
            logger.error(e)
        raise ValidationError("Validation failed. See log for details.")

    logger.info("Validation passed on %d rows", len(df))
    return df