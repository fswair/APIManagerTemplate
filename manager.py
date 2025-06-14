import user_agent

from pydantic import BaseModel, Field
from aiohttp import ClientSession, BasicAuth
from typing import Optional


class URL(str):
    """
    Custom URL class that extends Path to handle URL-like strings.
    This can be used to validate and manipulate URLs in a more structured way.
    """

    def __truediv__(self, other: str):
        """
        Override the division operator to allow for URL path concatenation.
        This is useful for constructing API endpoints.
        """
        return URL(f"{self.rstrip('/')}/{other.lstrip('/')}")


class AuthManager(BaseModel):
    username: Optional[str] = Field(None, description="API Username")
    token: str = Field(..., description="API Access Token")
    base_url: Optional[str] = Field("https://api.url", description="API Base URL")

    @property
    def user_agent(self):
        """
        Returns the User-Agent string for your API requests.
        This can be customized as needed.
        """
        return user_agent.generate_user_agent()

    @property
    def api_url(self):
        """
        Returns the base URL for your API requests.
        This is constructed from the base URL and the API path.
        """
        api_prefix = "api/v1"  # Adjust this if your API version is different
        return URL(f"{self.base_url}/{api_prefix}")

    def headers(self, bearer: bool = False):
        """
        Returns the headers required for your API requests.
        This includes the Authorization header with the Bearer token and other necessary headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            **(dict(Authorization=f"Bearer {self.token}") if bearer else {})
        }


class RequestManager(AuthManager):
    def __init__(self, auth: AuthManager):
        super().__init__(username=auth.username, token=auth.token, base_url=auth.base_url)

    async def request(self, endpoint: str, method: str = "GET", params: dict = None):
        """
        Makes a request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            method (str, optional): HTTP method to use. Defaults to "GET".
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the API.
        """
        url = self.api_url / endpoint.lstrip('/')
        auth = BasicAuth(self.username, self.token) if self.username and self.token else None
        headers = self.headers(bearer=not bool(auth))
        async with ClientSession(auth=auth) as session:
            requester = getattr(session, method.lower(), session.get)
            async with requester(url, headers=headers, params=params) as response:
                return await response.json()
