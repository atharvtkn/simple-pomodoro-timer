import customtkinter as ctk
import threading
import time
from main import Pomodoro


class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🍅 Pomodoro Timer")
        self.geometry("400x400")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.timer = Pomodoro()

        ctk.CTkLabel(self, text="Pomodoro Timer", font=("Arial", 22, "bold")).pack(pady=10)


        self.session_label = ctk.CTkLabel(self, text=self.timer.session_type, font=("Arial", 18))
        self.session_label.pack(pady=5)


        self.time_label = ctk.CTkLabel(self, text=self.timer.get_time_formatted(), font=("Arial", 36, "bold"))
        self.time_label.pack(pady=10)


        self.count_label = ctk.CTkLabel(self, text=f"Sessions Completed: {self.timer.session_count}")
        self.count_label.pack(pady=5)


        duration_frame = ctk.CTkFrame(self)
        duration_frame.pack(pady=5)

        self.work_entry = ctk.CTkEntry(duration_frame, width=60)
        self.work_entry.insert(0, str(self.timer.work_minutes))
        self.work_entry.pack(side="left", padx=5)
        ctk.CTkLabel(duration_frame, text="min Work").pack(side="left")

        self.break_entry = ctk.CTkEntry(duration_frame, width=60)
        self.break_entry.insert(0, str(self.timer.break_minutes))
        self.break_entry.pack(side="left", padx=5)
        ctk.CTkLabel(duration_frame, text="min Break").pack(side="left")

        ctk.CTkButton(duration_frame, text="Set", command=self.update_durations).pack(side="left", padx=5)


        ctk.CTkButton(self, text="Start", command=self.timer.start).pack(pady=5)
        ctk.CTkButton(self, text="Pause", command=self.timer.pause).pack(pady=5)
        ctk.CTkButton(self, text="Reset", command=self.timer.reset).pack(pady=5)
        ctk.CTkButton(self, text="Show Stats", command=self.timer.show_stats_plot).pack(pady=5)


        self.running = True
        threading.Thread(target=self.update_display, daemon=True).start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_display(self):
        while self.running:
            self.timer.tick()
            self.session_label.configure(text=self.timer.session_type)
            self.time_label.configure(text=self.timer.get_time_formatted())
            self.count_label.configure(text=f"Sessions Completed: {self.timer.session_count}")
            time.sleep(1)

    def update_durations(self):
        try:
            work_m = int(self.work_entry.get())
            break_m = int(self.break_entry.get())
            self.timer.set_durations(work_m, break_m)
        except ValueError:
            print("Invalid duration entered.")

    def on_close(self):
        self.running = False
        self.destroy()


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
