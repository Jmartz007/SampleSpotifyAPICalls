import logging
from logging.config import dictConfig


dictConfig(
    {
        "version": 1,
        "formatters": {
            "std": {
                "format": "[%(levelname)5s] %(module)s : %(message)s"
            },
            "stdtime": {
                "format": "%(asctime)s -- [%(levelname)5s] %(module)s : %(message)s",
                "datefmt": "%m-%d-%Y %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "formatter": "std",
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            },
            "file": {
                "formatter": "stdtime",
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "filename": "app.log",
            },
            "fileerrors": {
                "formatter": "stdtime",
                "class": "logging.FileHandler",
                "level": "WARNING",
                "filename": "errors.log"
            }
        },
        "loggers": {
            "main": {
                "handlers":["console", "file", "fileerrors"],
                "level": "DEBUG"
            }
        }
    }
)
