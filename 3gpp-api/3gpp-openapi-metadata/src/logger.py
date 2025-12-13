# src/logging_conf.py
import logging, json, sys
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event", None),
            "message": record.getMessage(),
        }
        # Merge extras if provided
        for key in ("event", "file", "title", "endpoint_count", "auth_methods",
                    "exception", "summary", "method", "url", "status", "body_snippet"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            exc_type, exc_val, _ = record.exc_info
            payload["exception"] = {"type": exc_type.__name__, "msg": str(exc_val)}
        return json.dumps(payload, ensure_ascii=False)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.propagate = False
    return logger