import time
from typing import Any, Literal
import requests


class Request_Handler:
    def __init__(self, delay: float) -> None:
        self.url_base = "https://www.speedrun.com/api/v"
        self.delay = delay  # delay to not exceed rate limit
        self.RATE_LIMIT = time.time()

    def rate_limit(self) -> None:
        now = time.time()
        duration = now - self.RATE_LIMIT
        if duration < self.delay:
            time.sleep(self.delay - duration)
        self.RATE_LIMIT = now

    def build_url(self, requestText: str, v: Literal[1] | Literal[2]) -> str:
        return f"{self.url_base}{v}/{requestText}"

    def handle_response_status(
        self, data: dict[str, Any]
    ) -> dict[str, Any] | Literal[False] | None:
        if "error" in data:
            raise Exception(data["message"])
        if "status" not in data:
            return data
        if data["status"] == 404:
            return False
        print(f"sleep 10 secs : {data}")
        time.sleep(10)

    def fetch_data(
        self, url: str, mute_exceptions: bool
    ) -> dict[str, Any] | Literal[False] | None:
        while True:
            self.rate_limit()
            try:
                response = requests.get(url, timeout=60)
                data = response.json()
                status_result = self.handle_response_status(data)
                if status_result is not None:
                    return status_result
            except TimeoutError:
                print("TimeoutError. Retrying after 10 seconds...")
                time.sleep(10)
            except Exception as e:
                if mute_exceptions:
                    return
                print(f"Error: {e}. Retrying after 10 seconds...")
                time.sleep(10)

    def request(
        self,
        requestText: str,
        v: Literal[1] | Literal[2] = 1,
        mute_exceptions: bool = False,
    ) -> dict[str, Any] | Literal[False] | None:
        url = self.build_url(requestText, v)
        return self.fetch_data(url, mute_exceptions)


request_handler = Request_Handler(0.7)
