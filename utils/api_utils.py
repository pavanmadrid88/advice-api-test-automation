import logging
import sys
from pathlib import Path
from typing import Type, Any

from pydantic import ValidationError


def get_logger(name: str = "api_test_logger"):
    """Returns a configured logger that writes to both console and file."""
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if logger is reused
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create logs directory if needed
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "test_log.log"

    # File handler
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    # Stream handler (console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(stream_handler)

    return logger

def validate_schema(model_cls: Type, data: Any) -> bool:
    """
    Validates if the given data matches the provided Pydantic model schema.

    Args:
        model_cls: The Pydantic model class to validate against.
        data: The response JSON/dict to validate.

    Returns:
        bool: True if data conforms to model schema, False otherwise.
    """
    try:
        model_cls(**data)
        return True
    except ValidationError as e:
        # Optional: log or print the validation error if you want visibility
        print(f"[Schema Validation Failed] {e}")
        return False

def parse_model(model_cls: Type, data: Any):
    """
    Validates and returns the parsed Pydantic model instance.
    Returns None if validation fails.
    """
    try:
        return model_cls(**data)
    except ValidationError as e:
        print(f"[Model Parse Failed] {e}")
        return None