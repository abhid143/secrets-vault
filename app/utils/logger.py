import logging
import sys
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Simple JSON structured log
        log = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        if hasattr(record, "request_id"):
            log["request_id"] = record.request_id
        if hasattr(record, "service"):
            log["service"] = record.service
        return json.dumps(log)

def configure_logging():
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root.setLevel(logging.INFO)
    if not root.handlers:
        root.addHandler(handler)
    else:
        # replace handlers to avoid duplicate logs in test environments
        root.handlers = [handler]
