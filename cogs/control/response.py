from typing import Any


class Response:
    def __init__(self, output: str, result: Any):
        self.output = output
        self.result = result
