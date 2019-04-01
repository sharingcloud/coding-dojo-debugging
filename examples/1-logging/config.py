LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(name)s] %(levelname)s %(asctime)s %(message)s"},
        "simple": {"format": "[%(name)s] %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "ERROR", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG"},
        "spammer": {"handlers": [], "level": "DEBUG", "propagate": False},
        "counter": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "__main__": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}
