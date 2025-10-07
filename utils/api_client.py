# api_client/client.py
from typing import Optional, Dict, Any
import requests
from urllib.parse import urljoin
import data


class APIClient:
    def __init__(self, base_url: Optional[str] = None, session: Optional[requests.Session] = None, timeout: int = 10):
        self.base_url = (base_url or data.constants.EndPoints.BASE_URL).rstrip('/')
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update({"Cache-Control": "no-cache", "Pragma": "no-cache"})

    def _url(self, path: str) -> str:
        return urljoin(f"{self.base_url}/", path.lstrip('/'))

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs):
        return self.session.get(self._url(path), params=params, timeout=self.timeout, **kwargs)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, **kwargs):
        return self.session.post(self._url(path), json=json, data=data, timeout=self.timeout, **kwargs)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.session.put(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass
