# Spammer script

import logging

logger = logging.getLogger(__name__)


def spam_debug():
    logger.debug("Je spam le debug !")


def spam_info():
    logger.info("Je spam l'info !")


def spam_error():
    logger.error("Je spam l'erreur !")