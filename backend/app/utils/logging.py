import logging
from ..core.config import settings

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        logging.basicConfig(level=settings.LOG_LEVEL, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        _logger = logging.getLogger(settings.APP_NAME)
    return _logger
