import logging 
import sys
from app.core.config import settings

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level = getattr(logging, settings.log_level.upper()),
        format= log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    api_logger = logging.getLogger("api")
    api_logger.setLevel(getattr(logging, settings.log_level.upper()))