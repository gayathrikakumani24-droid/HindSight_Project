"""Hindsight Cloud Service for ResolveIQ.

Initializes the Hindsight client using credentials loaded from the environment.
Provides health check and memory operations (retain, recall, reflect).
"""

from typing import Any, Dict, Optional, Tuple
import config

try:
    from hindsight_client import Hindsight
except ImportError:
    Hindsight = None  # type: ignore


class HindsightService:
    """Wrapper around Hindsight client with diagnostic and helper methods."""

    def __init__(self):
        self.api_key = config.HINDSIGHT_API_KEY
        self.bank_id = config.HINDSIGHT_BANK_ID
        self.base_url = config.HINDSIGHT_BASE_URL
        self._client: Optional[Any] = None

    def is_configured(self) -> bool:
        """Check if required Hindsight credentials are provided."""
        return bool(self.api_key) and bool(self.bank_id)

    def get_client(self) -> Optional[Any]:
        """Lazy-initialize and return the Hindsight client."""
        if not self.is_configured():
            return None

        if self._client is None and Hindsight is not None:
            self._client = Hindsight(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        return self._client

    def test_connection(self) -> Tuple[bool, str]:
        """Perform a health check against Hindsight Cloud."""
        if Hindsight is None:
            return False, "hindsight-client package is not installed."

        if not self.is_configured():
            return False, "HINDSIGHT_API_KEY or HINDSIGHT_BANK_ID is missing from the environment."

        try:
            client = self.get_client()
            if not client:
                return False, "Failed to initialize Hindsight client instance."

            # Verify connection by calling get_version()
            version_info = client.get_version()
            return True, f"Connected to Hindsight Cloud successfully! Server version: {version_info}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def retain_resolution(self, content: str, customer_id: Optional[str] = None) -> Tuple[bool, str]:
        """Retain a support resolution memory into Hindsight."""
        client = self.get_client()
        if not client:
            return False, "Hindsight client is not configured."

        try:
            payload = content
            if customer_id:
                payload = f"[Customer: {customer_id}] {content}"

            client.retain(bank_id=self.bank_id, content=payload)
            return True, "Resolution memory retained successfully!"
        except Exception as e:
            return False, f"Failed to retain memory: {str(e)}"

    def recall_memory(self, query: str) -> Tuple[bool, Any]:
        """Recall relevant past resolutions and context for a customer query."""
        client = self.get_client()
        if not client:
            return False, "Hindsight client is not configured."

        try:
            results = client.recall(bank_id=self.bank_id, query=query)
            return True, results
        except Exception as e:
            return False, f"Recall failed: {str(e)}"


# Singleton instance for simple app-wide usage
hindsight_service = HindsightService()
