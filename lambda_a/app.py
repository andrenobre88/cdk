import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context: dict) -> dict:
    logger.info(event, context)
    return event
