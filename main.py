
from remind_me import *
from datetime import datetime as dt
import constants as const
import time

reminder = RemindMe([])


def check_reminders():
    print("\n*** Reminder is ACTIVE ***\n")
    try:
        while True:
            for item in reminder.get_reminders_from_json():
                todays_date = dt.now().strftime(const.SDATE_FORMAT)[4:]
                current_time = dt.now().strftime(const.TIME_FORMAT)
                reminder_date = item['start_date'][4:]
                reminder_time = item["reminder_time"]

                if todays_date == reminder_date and current_time == reminder_time:
                    print(f"{item['title']}: {item['message']}")
                    reminder.show_toast_notification(
                        item["title"], item["message"])

            time.sleep(31)  # check reminders list every 30 seconds

    except KeyboardInterrupt:
        reminder.show_reminder_list()
        title = input("Title (max of 20 chars.): ")
        message = input("Message (max of 60 chars.): ")
        date = input("Date (mm-dd): ")
        reminder_time = input("Time (hh:mm am/pm): ")
        frequency = input("Frequency (in days): ")

        if title and message and date and time and frequency:
            reminder.create(title, message, date, reminder_time, frequency)

        reminder.show_reminder_list()
        check_reminders()


if __name__ == "__main__":
    check_reminders()
