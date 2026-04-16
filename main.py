import customtkinter as ctk
from playsound3 import playsound

# Выносим константы, чтобы менять всё в одном месте
WORK_TIME = 25 * 60
BREAK_TIME = 5 * 60
FONT_NAME = "Liga SFMono Nerd Font"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hikodoro")
        self.geometry("400x300")
        self.resizable(False, False)

        # Состояние приложения
        self.time_left = WORK_TIME
        self.is_running = False
        self.is_paused = False
        self.is_break = False
        self.sessions_count = 0
        self._timer_job = None # Для контроля после .after()

        self.setup_ui()

    def setup_ui(self):
        """Создаем все виджеты здесь, чтобы не захламлять __init__"""
        self.session_label = ctk.CTkLabel(self, text=" ", font=(FONT_NAME, 15))
        self.session_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        timer_font = ctk.CTkFont(family=FONT_NAME, size=85, weight="bold")
        self.timer_label = ctk.CTkLabel(self, text=self.format_time(), font=timer_font, text_color="gray")
        self.timer_label.grid(row=1, column=0, columnspan=2, padx=20, pady=0)

        self.start_button = ctk.CTkButton(self, text="  ", font=(FONT_NAME, 24), 
                                          command=self.handle_start_click, fg_color="red", hover_color="darkred")
        self.start_button.grid(row=2, column=0, padx=20, pady=20)

        self.pause_button = ctk.CTkButton(self, text="  ", font=(FONT_NAME, 24), 
                                          command=self.toggle_pause, state="disabled", 
                                          fg_color="darkgray", hover_color="gray")
        self.pause_button.grid(row=2, column=1, padx=20, pady=20)

    def format_time(self):
        """Метод-помощник для превращения секунд в 00:00"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02d}:{seconds:02d}"

    def handle_start_click(self):
        """Логика кнопки старт/сброс"""
        if not self.is_running:
            self.start_timer()
        elif self.is_paused:
            self.reset_timer()

    def start_timer(self):
        self.is_running = True
        self.is_paused = False
        self.timer_label.configure(text_color="white")
        self.pause_button.configure(state="normal", text="  ")
        self.start_button.configure(text="  ", state="disabled")
        self.tick()

    def toggle_pause(self):
        if not self.is_running: return
        
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.start_button.configure(text="  ", state="normal")
            self.pause_button.configure(text="  ")
            self.timer_label.configure(text_color="gray")
            if self._timer_job: self.after_cancel(self._timer_job)
        else:
            self.timer_label.configure(text_color="white")
            self.pause_button.configure(text="  ")
            self.start_button.configure(state="disabled")
            self.tick()

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.is_break = False
        self.sessions_count = 0
        self.time_left = WORK_TIME
        
        self.timer_label.configure(text=self.format_time(), text_color="gray")
        self.start_button.configure(text="  ", state="normal")
        self.pause_button.configure(state="disabled", text="  ")
        self.session_label.configure(text=" ")

    def tick(self):
        """Чистая логика тика таймера"""
        if not self.is_running or self.is_paused:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.configure(text=self.format_time())
            self._timer_job = self.after(1000, self.tick)
        else:
            self.switch_mode()

    def switch_mode(self):
        """Переключение между работой и отдыхом"""
        if self.is_break:
            playsound("breakover.mp3", block=False)
            self.time_left = WORK_TIME
            self.is_break = False
        else:
            playsound("timeover.mp3", block=False)
            self.sessions_count += 1
            self.session_label.configure(text=" " * self.sessions_count)
            self.time_left = BREAK_TIME
            self.is_break = True
        
        self.timer_label.configure(text=self.format_time())
        self.tick()

if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()