"""Counter."""

import logging

import spammer

logger = logging.getLogger(__name__)


def count_up_to(n):
    if n < 1:
        logger.error("Je ne sais pas compter les nombres inférieurs à 1")
        return

    logger.info(f"Je vais compter de 1 à {n}")

    for i in range(n):
        logger.debug(f"Je dis {i}...")

    logger.debug("J'ai fini de compter !")


def count_and_spam():
    count_up_to(2)
    spammer.spam_debug()
    spammer.spam_info()
    count_up_to(-1)
    spammer.spam_error()
    count_up_to(10)