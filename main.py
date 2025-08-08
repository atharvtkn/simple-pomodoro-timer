import json
import os
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import threading

try:
    import winsound
except ImportError:
    winsound = None


class Pomodoro:
    def __init__(self, work_minutes=25, break_minutes=5, data_file="pomodoro_data.json"):
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.data_file = data_file
        self.is_running = False
        self.remaining_seconds = work_minutes * 60
        self.session_type = "Work"  # or break (when sesh complete)
        self.session_count = 0
        self.load_data()

    def start(self):
        self.is_running = True

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.session_type = "Work"
        self.remaining_seconds = self.work_minutes * 60
        self.session_count = 0

    def tick(self):
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.remaining_seconds == 0:
                self.complete_session()

    def complete_session(self):
        self.play_sound()
        if self.session_type == "Work":
            self.log_session("Work")
            self.session_type = "Break"
            self.remaining_seconds = self.break_minutes * 60
        else:
            self.log_session("Break")
            self.session_type = "Work"
            self.remaining_seconds = self.work_minutes * 60
        self.session_count += 1

    def log_session(self, session_kind):
        today_str = str(date.today())
        if today_str not in self.data:
            self.data[today_str] = {"Work": 0, "Break": 0}
        self.data[today_str][session_kind] += 1
        self.save_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_time_formatted(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def set_durations(self, work_minutes, break_minutes):
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.reset()

    def play_sound(self):
        def _play():
            if winsound:
                winsound.Beep(1000, 500)
            else:
                print("\a", end="") 

        threading.Thread(target=_play, daemon=True).start()

    def show_stats_plot(self):
        if not self.data:
            return "No data yet. Complete a session first!"

        df = pd.DataFrame(self.data).T.fillna(0)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        plt.figure(figsize=(7, 4))
        plt.bar(df.index.strftime("%Y-%m-%d"), df["Work"], color="salmon", label="Work")
        plt.bar(df.index.strftime("%Y-%m-%d"), df["Break"], bottom=df["Work"], color="lightblue", label="Break")
        plt.xticks(rotation=45)
        plt.title("Pomodoros Completed Per Day")
        plt.ylabel("Sessions")
        plt.legend()
        plt.tight_layout()
        plt.show()

        return "Stats shown successfully."
