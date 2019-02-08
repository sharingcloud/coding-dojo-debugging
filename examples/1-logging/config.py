LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {"format": "[%(name)s] %(levelname)s %(asctime)s %(message)s"},
        "simple": {"format": "[%(name)s] %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "__main__": {"handlers": ["console"], "level": "DEBUG"},
        "spammer": {"handlers": ["console"], "level": "DEBUG"},
        "counter": {"handlers": ["console"], "level": "DEBUG"},
    },
}