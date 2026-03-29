import customtkinter as ctk
import threading
import time
import random
import sys
from pynput import keyboard as pk
from pynput.keyboard import Controller
from PIL import Image, ImageDraw 
import pystray

# --- UI Styling ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

class AutoTyperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Typer Pro: Ghost Mode")
        self.geometry("1100x850")

        self.keyboard = Controller()
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.stop_event = threading.Event()

        self.is_typing = False
        
        # Tray setup
        self.protocol('WM_DELETE_WINDOW', self.withdraw_to_tray)
        self._create_tray_icon()

        self._build_ui()
        self._register_hotkeys()

    def _build_ui(self):
        header = ctk.CTkLabel(self, text="🚀 AUTO TYPER PRO", font=("Segoe UI Black", 28), text_color="#00fbff")
        header.pack(pady=20)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=10)
        body.columnconfigure(0, weight=4)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # --- LEFT SIDE ---
        left = ctk.CTkFrame(body, corner_radius=15, border_width=2, border_color="#333333")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(left, font=("Consolas", 14), fg_color="#1a1a1a")
        self.textbox.grid(row=1, sticky="nsew", padx=15, pady=10)
        self.textbox.tag_config("typed", background="#ff007f") 

        self.progress = ctk.CTkProgressBar(left, progress_color="#00fbff", height=12)
        self.progress.grid(row=2, sticky="ew", padx=20, pady=(10, 0))
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(left, text="0% Done.", font=("Segoe UI", 12))
        self.progress_label.grid(row=3, pady=(0, 10))

        # --- RIGHT SIDE ---
        right = ctk.CTkScrollableFrame(body, width=300, label_text="COMMAND CENTER")
        right.grid(row=0, column=1, sticky="nsew")

        self.status = ctk.CTkLabel(right, text="Status: Idle", font=("Segoe UI", 14, "italic"), text_color="#ffcc00")
        self.status.pack(pady=10)

        self.speed = ctk.DoubleVar(value=0.6)
        ctk.CTkSlider(right, from_=0.01, to=1.0, variable=self.speed).pack(fill="x", pady=5)
        
        self.delay = ctk.CTkEntry(right, justify="center")
        self.delay.insert(0, "3")
        self.delay.pack(pady=5)

        ctk.CTkButton(right, text="▶ START", command=self.start_typing, fg_color="#28a745").pack(fill="x", pady=5)
        ctk.CTkButton(right, text="⏸ PAUSE/RESUME", command=self._toggle, fg_color="#17a2b8").pack(fill="x", pady=5)
        ctk.CTkButton(right, text="⏹ STOP", command=self.stop_typing, fg_color="#dc3545").pack(fill="x", pady=5)
        ctk.CTkButton(right, text="↺ RESTART", command=self.restart_typing, fg_color="#6c757d").pack(fill="x", pady=5)
        ctk.CTkButton(right, text="🗑 RESET", command=self.reset_all, fg_color="transparent", border_width=1).pack(fill="x", pady=5)

        # Instructions Section
        instr_frame = ctk.CTkFrame(right, fg_color="#2b2b2b", corner_radius=10)
        instr_frame.pack(fill="x", pady=20, padx=5)
        ctk.CTkLabel(instr_frame, text="📖 QUICK GUIDE", font=("Segoe UI", 12, "bold"), text_color="#00fbff").pack(pady=5)
        guide_text = "🔥 HOTKEYS (Ctrl + Shift):\n• [F9]  : Start / Pause\n• [F10] : Stop\n• [F11] : Reset\n• [F12] : Restart"
        ctk.CTkLabel(instr_frame, text=guide_text, font=("Consolas", 11), justify="left").pack(pady=10, padx=10)

    # ================= TRAY LOGIC =================

    def _create_tray_icon(self):
        width, height = 64, 64
        image = Image.new('RGB', (width, height), color=(0, 251, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill=(26, 26, 26))
        
        menu = (pystray.MenuItem('Show App', self.show_app, default=True),
                pystray.MenuItem('Quit Completely', self.quit_app))
        
        self.tray_icon = pystray.Icon("AutoTyper", image, "Auto Typer Pro", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def withdraw_to_tray(self):
        self.withdraw() 

    def show_app(self, icon=None, item=None):
        self.deiconify() 
        self.focus_force()

    def quit_app(self, icon=None, item=None):
        self.tray_icon.stop()
        self.quit()
        sys.exit()

    # ================= TYPING LOGIC =================

    def _press_release(self, key, hold=0.008):
        self.keyboard.press(key)
        time.sleep(hold)
        self.keyboard.release(key)

    def _type_character(self, char):
        try:
            if char == "\n": self._press_release(pk.Key.enter, 0.015)
            elif char == " ": self._press_release(pk.Key.space, 0.006)
            else:
                self.keyboard.press(char)
                time.sleep(random.uniform(0.006, 0.012))
                self.keyboard.release(char)
        except: pass

    def _typing_worker(self, text):
        lines = text.replace("\t", "    ").split("\n")
        total_chars = len(text)
        typed_chars = 0

        for line in lines:
            if self.stop_event.is_set(): return
            self.pause_event.wait()
            
            # Preserve indentation
            leading_spaces = len(line) - len(line.lstrip(" "))
            content = line.lstrip(" ")

            for char in content:
                if self.stop_event.is_set(): return
                self.pause_event.wait()
                self._type_character(char)
                typed_chars += 1
                self.after(0, self._update_progress, typed_chars, total_chars)
                
                # Speed Calculation
                delay = (1.1 - self.speed.get()) ** 2 * 0.4 
                time.sleep(delay + random.uniform(0.01, 0.03))

            self._type_character("\n")
            typed_chars += 1
        self.after(0, self._completed)

    def _update_progress(self, typed, total):
        # Prevent division by zero if textbox is somehow empty
        if total <= 0: return
        percent = min(typed / total, 1.0)
        self.progress.set(percent)
        self.progress_label.configure(text=f"{int(percent * 100)}% - Typing...")
        self.textbox.tag_remove("typed", "1.0", "end")
        self.textbox.tag_add("typed", "1.0", f"1.0+{typed}c")

    def _completed(self):
        self.status.configure(text="Status: Done!", text_color="#00fbff")
        self.is_typing = False

    def start_typing(self):
        if self.is_typing: return
        text = self.textbox.get("1.0", "end-1c").replace("\t", "    ")
        if not text.strip(): return
        
        self.stop_event.clear()
        self.pause_event.set()
        self.is_typing = True
        
        try: d = float(self.delay.get())
        except: d = 0
        
        def run_with_delay():
            time.sleep(d)
            if not self.stop_event.is_set():
                self._typing_worker(text)

        threading.Thread(target=run_with_delay, daemon=True).start()
        self.status.configure(text="Status: Typing...", text_color="#00fbff")

    def stop_typing(self):
        self.stop_event.set()
        self.pause_event.set()
        self.is_typing = False
        self.status.configure(text="Status: Stopped.", text_color="#dc3545")

    def reset_all(self):
        self.stop_typing()
        self.textbox.tag_remove("typed", "1.0", "end")
        self.textbox.delete("1.0", "end")
        self.progress.set(0)
        self.progress_label.configure(text="0% Done.")
        self.status.configure(text="Status: Reset.", text_color="gray")

    def restart_typing(self):
        """Fixes the glitch where progress and highlights didn't reset on restart."""
        self.stop_typing()
        # Explicit UI cleanup
        self.progress.set(0)
        self.progress_label.configure(text="0% Done.")
        self.textbox.tag_remove("typed", "1.0", "end")
        self.status.configure(text="Status: Restarting...", text_color="#ffcc00")
        
        # Short sleep to allow thread termination before starting new one
        time.sleep(0.5)
        self.start_typing()

    def _register_hotkeys(self):
        pressed = set()
        def press(key):
            pressed.add(key)
            ctrl = any(k in pressed for k in [pk.Key.ctrl_l, pk.Key.ctrl_r])
            shift = any(k in pressed for k in [pk.Key.shift_l, pk.Key.shift_r])
            if ctrl and shift:
                if key == pk.Key.f9: self.after(0, self._toggle)
                elif key == pk.Key.f10: self.after(0, self.stop_typing)
                elif key == pk.Key.f11: self.after(0, self.reset_all)
                elif key == pk.Key.f12: self.after(0, self.restart_typing)
        def release(key): pressed.discard(key)
        pk.Listener(on_press=press, on_release=release, daemon=True).start()

    def _toggle(self):
        if not self.is_typing: self.start_typing()
        elif self.pause_event.is_set(): 
            self.pause_event.clear()
            self.status.configure(text="Status: Paused", text_color="#ffcc00")
        else: 
            self.pause_event.set()
            self.status.configure(text="Status: Typing...", text_color="#00fbff")

if __name__ == "__main__":
    app = AutoTyperApp()
    app.mainloop()