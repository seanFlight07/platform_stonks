from utils import logger

logger = logger.setup_logger(__name__)

def validation(data):
    errors = 0
    columns_needed = ["open",
                    "high",
                    "low",
                    "close",
                    "change_dollar",
                    "change_pct",
                    "volume",
                    "date",
                    "code"]
    extra_columns = [
        column for column in data.columns
        if column not in columns_needed
    ]
    if extra_columns:
        logger.warning("Unexpected columns: %s",extra_columns)
        errors += 1

    for column in columns_needed:
        if column not in data.columns:
            logger.warning("Missing required column: %s",column)
            errors += 1

    columns_with_no_missing = data.notna().all()

    for col_name, is_clean in columns_with_no_missing.items():
        if not is_clean:
            logger.warning("Column %s has missing data.",col_name)
            errors += 1

    if errors > 0:
        return False

    return True
