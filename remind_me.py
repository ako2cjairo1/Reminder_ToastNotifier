# this module will allow the user to create a reminder toast notification
# for any purpose it may serve.
# Features:
# 1. set time of notification, start and end date, frequencies of a reminder.
# 2. TODO: be able to delete existing reminders.
# 3. be able to save these data on a JSON file.

import os
import json
import time
from datetime import datetime as dt
from win10toast import ToastNotifier

from reminder import *
import constants as const


class RemindMe:
    def __init__(self, reminders):
        self.reminder_list = reminders

    def get_reminders_from_json(self):
        json_data = []

        try:
            # check if json file is present
            if os.path.isfile(const.JSON_FILE_NAME):
                # open and load the json file content
                with open(const.JSON_FILE_NAME, "r") as json_file:
                    json_data = json.load(json_file)

                # get reminders from json_data to the main list
                self.reminder_list = [
                    reminder for reminder in json_data["reminders"]]

        except Exception as e:
            print(
                f"**Contents of \"{const.JSON_FILE_NAME}\" is not in a correct format.\n")

        return self.reminder_list

    def get_reminders(self):
        reminders = []
        # create a reminder object and then serialize content
        for item in self.reminder_list:
            reminders.append(Reminder(item).serialize())

        return reminders

    def serialize(self):
        return {"reminders": self.get_reminders()}

    def create(self, title, message, start_date, reminder_time, frequency):
        # get reminders from json file before creating a new one
        consolidated_reminders = self.get_reminders_from_json()

        try:
            # create dictionary format of the reminder
            reminder_dict = {
                "title": title,
                "message": message,
                "start_date": dt.strptime(start_date, const.DATE_FORMAT).strftime(const.SDATE_FORMAT),
                "reminder_time": reminder_time,
                "frequency": frequency
            }

            # TODO: check if there is duplicate reminder
            # append the new reminder to the consolidated list
            consolidated_reminders.append(Reminder(reminder_dict).serialize())

            # overwrite the json file using the consolidated list (previous and newly created)
            with open(const.JSON_FILE_NAME, "w", encoding="utf-8") as writer:
                json.dump(RemindMe(consolidated_reminders).serialize(),
                          writer, indent=4)

            print(f"\n**Created! ({title})\n")
        except Exception as e:
            print("Error while creating the reminder.")

    def show_toast_notification(self, title, message):
        # initialize toast notifier class
        toast = ToastNotifier()

        # show reminder notification
        toast.show_toast(title, message, threaded=True,
                         duration=15, icon_path="brenda.ico")

        # wait until notification is done
        while toast.notification_active():
            time.sleep(0.01)

    def is_unique(self, title):
        return title.strip().lower() in [ti["title"].strip().lower() for ti in self.get_reminders_from_json()]

    def show_reminder_list(self):
        print("\n", "=" * 30, " Reminders List ", "=" * 30)

        for idx, reminder in enumerate(self.get_reminders_from_json()):
            # get details of title, message and date from reminder dictionary
            title = [reminder[t] for t in reminder if "title" in t]
            message = [reminder[m] for m in reminder if "message" in m]
            date = [reminder[d] for d in reminder if "start_date" in d]

            print(
                f"({date[0]}) {title[0]}:- {message[0]}")

        print("=" * 78, "\n")
