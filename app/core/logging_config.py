import logging
import sys

def setup_logging():
    """
    Configures the root logger for the application.
    Sets standard output format and level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        stream=sys.stdout
    )

    # Disable noisy third-party loggers if necessary
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
