from typing import List


class MessageDTO:
    def __init__(self, message: str, files: List[str] = None):
        self.message = message
        self.files = files
