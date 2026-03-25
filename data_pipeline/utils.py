import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def validate_dataframe(df):
    if df.empty:
        raise ValueError("DataFrame is empty")

    if df.isnull().sum().sum() > 0:
        print("Warning: Data contains null values")

    return True
