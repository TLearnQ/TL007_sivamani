# src/client.py
import requests
from dataclasses import dataclass
from typing import Optional
from logger import get_logger

log = get_logger(__name__)

@dataclass
class APIResponseError(Exception):
    status_code: int
    method: str
    url: str
    body: Optional[str] = None
    def __str__(self):
        return f"{self.method} {self.url} -> {self.status_code}"

class APIClient:
    def __init__(self, base_url: str, timeout: int = 20, headers: Optional[dict] = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = self.session.request(method.upper(), url, timeout=self.timeout, **kwargs)
            log.info("api_request", extra={
                "event":"api_request","method":method,"url":url,"status":resp.status_code
            })
        except requests.RequestException as exc:
            log.error("api_transport_error", extra={
                "event":"api_transport_error","method":method,"url":url,
                "exception":exc.__class__.__name__,"message":str(exc)
            })
            raise
        if not (200 <= resp.status_code < 300):
            body_snip = (resp.text[:300] if getattr(resp, "text", None) else None)
            log.error("api_response_error", extra={
                "event":"api_response_error","method":method,"url":url,
                "status":resp.status_code,"body_snippet":body_snip
            })
            raise APIResponseError(status_code=resp.status_code, method=method, url=url, body=body_snip)
        return resp