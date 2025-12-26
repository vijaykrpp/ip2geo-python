import requests


class Ip2Geo:
    BASE_URL = "https://api.ip2geoapi.com/ip"

    def __init__(self, api_key: str | None = None, timeout: int = 60):
        self.api_key = api_key
        self.timeout = timeout

    def lookup(
        self,
        ip: str | None = None,
        format: str | None = None,
        callback: str | None = None,
    ):
        params = {}

        if self.api_key:
            params["key"] = self.api_key

        if format:
            params["format"] = format

        if callback:
            if format != "jsonp":
                raise ValueError("callback can only be used when format='jsonp'")
            params["callback"] = callback

        url = f"{self.BASE_URL}/{ip}" if ip else self.BASE_URL

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            # TRUE transport failure
            raise RuntimeError("Unable to reach Ip2Geo API") from e

        # If JSON is expected (default or explicit)
        if format is None or format == "json":
            try:
                return response.json()
            except ValueError:
                raise RuntimeError("Expected JSON but received invalid response")

        # XML / YAML / JSONP → raw text
        return response.text
