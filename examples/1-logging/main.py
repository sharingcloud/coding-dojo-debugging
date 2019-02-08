# Main

import logging
import logging.config

from config import LOGGING
import counter

logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)


def main():
    logger.info("Je démarre le script...")
    counter.count_and_spam()
    logger.info("J'ai fini le script...")

if __name__ == "__main__":
    main()