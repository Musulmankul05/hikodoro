import os, json, pyglet, threading
import customtkinter as ctk
from playsound3 import playsound
from pathlib import Path


CONFIG_FILE = "conf.json"
def load_config():
    default_config = {
        "window-width": 200,
        "window-height": 120,
        "WORKTIME": 1500, 
        "BREAKTIME": 300,
    }
    
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        return default_config
        
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_config
    
conf = load_config()
font_path = Path(__file__).parent / "LigaSFMonoNerdFont-Bold.otf"
pyglet.font.add_file(str(font_path))

WORK_TIME = conf.get("WORKTIME", 1500)
BREAK_TIME = conf.get("BREAKTIME", 300)
WINDOW_WIDTH = conf.get("window-width", 200)
WINDOW_HEIGHT = conf.get("window-height", 180)
FONT_NAME = "Liga SFMono Nerd Font"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hikodoro")
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
        self.session_label = ctk.CTkLabel(self, text=" ", font=(FONT_NAME, 15), height=1)
        self.session_label.grid(row=0, column=0, padx=0, pady=(5, 0), sticky="ew")

        timer_font = ctk.CTkFont(family=FONT_NAME, size=45, weight="bold")
        self.timer_label = ctk.CTkLabel(self, text=self.format_time(), font=timer_font, text_color="gray")
        self.timer_label.grid(row=1, column=0, columnspan=2, padx=0, pady=0)

        self.start_button = ctk.CTkButton(self, text="  ", font=(FONT_NAME, 24), 
                                          command=self.handle_start_click, fg_color="red", 
                                          hover_color="darkred", width=70)
        self.start_button.grid(row=2, column=0, padx=(20, 5), pady=0)

        self.pause_button = ctk.CTkButton(self, text="  ", font=(FONT_NAME, 24), 
                                          command=self.toggle_pause, state="disabled", 
                                          fg_color="#595959", hover_color="#404040", width=70)
        self.pause_button.grid(row=2, column=1, padx=(5, 20), pady=0)

    def format_time(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def play_sound(self, file):
        threading.Thread(target=playsound, args=(file,), daemon=True).start()


    def handle_start_click(self):
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
        if not self.is_running or self.is_paused:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.configure(text=self.format_time())
            self._timer_job = self.after(1000, self.tick)
        else:
            self.switch_mode()

    def switch_mode(self):
        if self.is_break:
            self.play_sound("breakover.mp3")
            self.time_left = WORK_TIME
            self.is_break = False
        else:
            self.play_sound("timeover.mp3")
            self.sessions_count += 1
            self.session_label.configure(text=" " * self.sessions_count)
            self.time_left = BREAK_TIME
            self.is_break = True
        
        self.timer_label.configure(text=self.format_time())
        self.tick()

if __name__ == "__main__":
    app = App()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    app.grid_columnconfigure(0, weight=1)
    x = screen_width - WINDOW_WIDTH - 20
    y = screen_height - WINDOW_HEIGHT - 50 
    app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    app.mainloop()
