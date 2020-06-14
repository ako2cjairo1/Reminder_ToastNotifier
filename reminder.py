import constants as const
from datetime import datetime as dt


class Reminder:
    def __init__(self, reminder):
        self.title = reminder["title"]
        self.message = reminder["message"]
        self.start_date = reminder["start_date"]
        self.reminder_time = reminder["reminder_time"]
        self.frequency = reminder["frequency"]

    def serialize(self):
        return {
            "title": self.title,
            "message": self.message,
            "start_date": self.start_date,
            "reminder_time": self.reminder_time,
            "frequency": self.frequency
        }
