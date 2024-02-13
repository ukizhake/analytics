import uvicorn
from fastapi.logger import logger
import logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": "%(levelname)s %(name)s@%(lineno)d %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "uvicorn.log",
            "formatter": "default"
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "": {"handlers": ["default", "file"], "level": "ERROR"},
    },
}

class IgnoreChangeDetectedFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
       return '%d change%s detected: %s' != record.msg

if __name__ == "__main__":
    logging.basicConfig(format='{levelname:7} {message}', style='{', level=logging.ERROR)
    uvicorn.run("app.app:app", port=8080,  host='0.0.0.0', reload=True, reload_excludes="*.log", log_level='debug')


