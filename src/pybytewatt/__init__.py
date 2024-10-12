from typing import Any, Dict, Optional

import aiohttp

class ByteWattAPI:
    """Main class to interact with the Byte Watt API."""

    def __init__(self, username: str, password: str, auth_signature: str, auth_timestamp: str, timeout: Optional[float] = 5.0):
        """Initialize the API client.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
            auth_signature (str): The authentication signature.
            auth_timestamp (str): The authentication timestamp.
            timeout (float, optional): The timeout for API requests in seconds. Defaults to 5.0.
        """
        self.username = username
        self.password = password
        self.auth_signature = auth_signature
        self.auth_timestamp = auth_timestamp
        self.access_token = None
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def __aenter__(self):
        """Async enter method to support 'async with' syntax."""
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async exit method to support 'async with' syntax."""
        if self.session:
            await self.session.close()
            self.session = None

    async def authenticate(self) -> None:
        """Authenticate with the Byte Watt API and obtain an access token."""
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

        url = "https://monitor.byte-watt.com/api/Account/Login"
        params = {
            "authsignature": self.auth_signature,
            "authtimestamp": self.auth_timestamp,
        }
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "userName": self.username,
            "password": self.password
        }
        async with self.session.post(url, params=params, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            self.access_token = data["data"]["AccessToken"]


    async def get_battery_data(self) -> Dict[str, Any]:
        """Retrieve the latest battery data from the Byte Watt API."""
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

        if not self.access_token:
            await self.authenticate()

        url = "https://monitor.byte-watt.com/api/ESS/GetLastPowerDataBySN"
        params = {
            "sys_sn": "All",
            "noLoading": "true",
        }
        headers = {
            "Content-Type": "application/json",
            "authtimestamp": str(self.auth_timestamp),
            "authsignature": self.auth_signature,
            "Authorization": f"Bearer {self.access_token}",
        }

        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status == 401:
                # Token expired, re-authenticate and try again
                await self.authenticate()
                headers = {"Authorization": f"Bearer {self.access_token}"}
                async with self.session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
            else:
                response.raise_for_status()
                data = await response.json()

        if data.get("code") == 9007:
            raise ByteWattAPIError("Network error code 9007 from Byte Watt API")

        if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
            return data['data']  # Return the first system's data
        else:
            raise ByteWattAPIError("Unexpected data format from Byte Watt API")

    async def close(self):
        """Close the aiohttp ClientSession."""
        if self.session:
            await self.session.close()
            self.session = None

class ByteWattAPIError(Exception):
    """Raised when there is an error with the Byte Watt API."""
