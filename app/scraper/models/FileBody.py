from datetime import datetime


class FileBody:
    def __init__(self, date_time: datetime, checked: set[str]) -> None:
        super().__init__()
        self.date_time: datetime = date_time
        self.checked: set[str] = checked
