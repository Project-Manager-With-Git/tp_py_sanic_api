class SSEEvent:
    _DEFAULT_SEPARATOR = "\r\n"

    def __init__(self, event_id: int, event_data: str, event_name: str = "message", retry: int = 1000) -> None:
        self.event_id = event_id
        self.event_data = event_data
        self.event_name = event_name
        self.retry = retry

    def __str__(self) -> str:
        return f"event: {self.event_name}{self._DEFAULT_SEPARATOR}data: {self.event_data}{self._DEFAULT_SEPARATOR}id: {self.event_id}{self._DEFAULT_SEPARATOR}retry: {self.retry}{self._DEFAULT_SEPARATOR}{self._DEFAULT_SEPARATOR}"
