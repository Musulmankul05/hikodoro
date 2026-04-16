from pydoc import text

import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hikodoro")
        self.geometry("400x300")
        self.resizable(False, False)
        self.NERD_FONT = "Liga SFMono Nerd Font"

        self.time = 25 * 60
        self.running = False
        self.paused = False
        self.breaktime = False
        self.sessions = 0

        self.session = ctk.CTkLabel(self, text=" ", font=(self.NERD_FONT, 15))
        self.session.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.timer_font = ctk.CTkFont(family=self.NERD_FONT, size=85, weight="bold")

        self.timer = ctk.CTkLabel(self, text=f"{self.time // 60:02d}:{self.time % 60:02d}", font=self.timer_font, text_color="gray")
        self.timer.grid(row=1, column=0, columnspan=2, padx=20, pady=0)


        self.start_button = ctk.CTkButton(self, text="  ", font=(self.NERD_FONT, 24), 
                                          command=self.start_timer, fg_color="red", hover_color="darkred")
        self.start_button.grid(row=2, column=0, padx=20, pady=20)

        self.pause_button = ctk.CTkButton(self, text="  ", font=(self.NERD_FONT, 24), 
                                          command=self.pause_timer, state="disabled", 
                                          fg_color="darkgray", hover_color="gray")
        self.pause_button.grid(row=2, column=1, padx=20, pady=20)
        self.debug_button = ctk.CTkButton(self, text="Print", font=("Arial", 24), command=lambda: print(self.running))
        self.debug_button.grid(row=3, column=0, columnspan=2)
        

    def start_timer(self):
        if not self.running:
            self.running = True
            self.timer.configure(text_color="white")
            self.pause_button.configure(state="normal")
            self.start_button.configure(self, text="  ")
            self.update_timer()


    def pause_timer(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.configure(text="  ")
                self.timer.configure(text_color="gray")
            else:
                self.timer.configure(text_color="white")
                self.pause_button.configure(text="  ")
                self.update_timer()

    def update_timer(self):
        if self.running and not self.paused:
            if self.time > 0:
                self.time -= 1
                self.timer.configure(text=f"{self.time // 60:02d}:{self.time % 60:02d}")
                self.after(1000, self.update_timer)
            elif self.breaktime:
                self.breaktime = False
                self.time = (25 * 60) + 1
                self.after(1000, self.update_timer)
            else:
                self.breaktime = True
                self.time = (5 * 60) + 1
                self.sessions += 1
                print(self.sessions)
                self.session.configure(text="" + (" " * self.sessions))
                self.after(0, self.update_timer)


if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()