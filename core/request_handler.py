import time
from typing import Any, TypeVar, Type
import requests
from common.speedrun_types import ApiVersions
from random import randint

T = TypeVar("T")


class Request_Handler:
    MAX_RETRIES = 7

    def __init__(self, delay: float) -> None:
        self.url_base = "https://www.speedrun.com/api/v"
        self.delay = delay  # delay to not exceed rate limit
        self.last_execution = time.time()
        self.retries = 0

    def rate_limit(self) -> None:
        now = time.time()
        duration = now - self.last_execution
        if duration < self.delay:
            time.sleep(self.delay - duration)
        self.last_execution = now

    def build_url(self, requestText: str, v: ApiVersions) -> str:
        return f"{self.url_base}{v}/{requestText}"

    def handle_response_status(self, data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            raise ConnectionError(data["message"])
        if "status" not in data:
            return data
        if data["status"] == 404:
            raise ResourceWarning("Not found")
        raise Exception(
            f"API returned status={data.get('status', 'no status')} with data={data}"
        )

    def sleep_retry(self, e: Exception) -> None:
        print(f"Error: {e}. Retrying after 10 seconds...")
        time_sleep = 2**self.retries + randint(0, 999) / 1000
        time.sleep(time_sleep)
        self.retries += 1
        if self.retries > self.MAX_RETRIES:
            self.retries = 0

    def fetch_data(self, url: str, mute_exceptions: bool) -> dict[str, Any]:
        self.retries = 0
        while True:
            self.rate_limit()
            try:
                response = requests.get(url, timeout=60)
                data = response.json()
                status_result = self.handle_response_status(data)
                return status_result
            except ConnectionError as e:
                self.sleep_retry(e)
            except requests.Timeout as e:
                self.sleep_retry(e)
            except ResourceWarning as e:
                raise e
            except Exception as e:
                if not mute_exceptions:
                    raise e
                self.sleep_retry(e)

    def request(
        self,
        request_text: str,
        v: ApiVersions = 1,
        *,
        response_type: Type[T],
        mute_exceptions: bool = True,
    ) -> T:
        url = self.build_url(request_text, v)
        data = self.fetch_data(url, mute_exceptions)
        parsed = response_type(**data)
        return parsed


request_handler = Request_Handler(0.7)
