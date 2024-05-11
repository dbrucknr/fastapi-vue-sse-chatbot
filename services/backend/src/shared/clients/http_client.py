from httpx import AsyncClient, Request, Response, URL


class BaseNetworkClient(AsyncClient):
    """
        Provides a base HTTP client with automatic error handling and logging.
    """

    def __init__(self) -> None:
        self.base_url = URL()

        self.event_hooks = {
            "request": [self.log_request],
            "response": [self.log_response, self.raise_on_4xx_5xx],
        }

    async def log_request(self, request: Request) -> None:
        print(
            "Method: %s\nURL: %s\nStatus: Waiting for response",
            request.method,
            request.url,
        )

    async def log_response(self, response: Response) -> None:
        print(
            "Method: %s\nURL: %s\nStatus: %s",
            response.request.method,
            response.request.url,
            response.status_code,
        )

    async def raise_on_4xx_5xx(self, response: Response) -> None:
        response.raise_for_status()