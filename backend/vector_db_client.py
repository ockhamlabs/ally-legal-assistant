import os
import requests


class VectorDBClient:
    """Simple HTTP client for a configurable vector database API."""

    def __init__(self):
        self.endpoint = os.getenv("VECTOR_API_ENDPOINT", "http://localhost:8000")
        self.api_key = os.getenv("VECTOR_API_KEY")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def query(self, text, vector=None, top_k=3, index="default", filters=None):
        payload = {
            "text": text,
            "vector": vector,
            "top_k": top_k,
            "index": index,
            "filters": filters or {},
        }
        resp = requests.post(
            f"{self.endpoint}/query",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def vector_search(self, vector, top_k=3, index="default", filters=None):
        return self.query("", vector=vector, top_k=top_k, index=index, filters=filters)

    def insert(self, documents, index="default"):
        payload = {"documents": documents, "index": index}
        resp = requests.post(
            f"{self.endpoint}/insert",
            json=payload,
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
