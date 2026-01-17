import customtkinter as ctk
import yt_dlp
import threading
import os
import re
import json
from tkinter import filedialog

# --- CONFIGURATION ---
SETTINGS_FILE = "settings.json"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("ProStream Downloader v3.0")
        self.geometry("650x580")

        # Load Saved Path
        self.download_path = self.load_settings()

        # --- UI LAYOUT ---
        self.label = ctk.CTkLabel(self, text="YouTube Pro Downloader", font=("Arial", 22, "bold"))
        self.label.pack(pady=20)

        # URL Input
        self.url_entry = ctk.CTkEntry(self, width=520, height=35, placeholder_text="Paste YouTube link here...")
        self.url_entry.pack(pady=10)

        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.pack(pady=10, fill="x", padx=65)
        
        self.path_label = ctk.CTkLabel(self.path_frame, text=f"Save to: {self.truncate_path(self.download_path)}", font=("Arial", 12))
        self.path_label.pack(side="left")
        
        self.path_btn = ctk.CTkButton(self.path_frame, text="Change Folder", width=120, height=28, command=self.change_path)
        self.path_btn.pack(side="right")

        # Progress Section
        self.status_label = ctk.CTkLabel(self, text="Ready to Download", text_color="gray")
        self.status_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Live Process Notes (Log Box)
        self.log_box = ctk.CTkTextbox(self, width=520, height=150, font=("Consolas", 12))
        self.log_box.pack(pady=10)

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.video_btn = ctk.CTkButton(self.btn_frame, text="Download Video (MP4)", width=200, height=40, 
                                      fg_color="#1f538d", hover_color="#14375e", 
                                      command=lambda: self.start_thread('video'))
        self.video_btn.pack(side="left", padx=10)

        self.audio_btn = ctk.CTkButton(self.btn_frame, text="Download Audio (MP3)", width=200, height=40, 
                                      fg_color="#2b733f", hover_color="#1e522d", 
                                      command=lambda: self.start_thread('audio'))
        self.audio_btn.pack(side="left", padx=10)

    # --- HELPERS ---
    def truncate_path(self, path):
        if len(path) > 40:
            return "..." + path[-37:]
        return path

    def log(self, message):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f).get("path", os.path.expanduser("~/Downloads"))
            except:
                pass
        return os.path.expanduser("~/Downloads")

    def save_settings(self, new_path):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"path": new_path}, f)

    def change_path(self):
        new_dir = filedialog.askdirectory()
        if new_dir:
            self.download_path = new_dir
            self.save_settings(new_dir)
            self.path_label.configure(text=f"Save to: {self.truncate_path(new_dir)}")
            self.log(f"📁 Path changed to: {new_dir}")

    # --- CORE LOGIC ---
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            # Clean ANSI escape codes from percent string
            clean_p = re.sub(r'\x1b\[[0-9;]*m', '', percent).strip().replace('%', '')
            
            try:
                p_float = float(clean_p) / 100
                self.progress_bar.set(p_float)
                self.status_label.configure(text=f"Downloading: {clean_p}% | Speed: {speed} | ETA: {eta}")
            except:
                pass

    def start_thread(self, mode):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="Please enter a URL!", text_color="red")
            return
            
        self.log_box.delete("0.0", "end")
        self.progress_bar.set(0)
        # Daemon=True ensures the thread closes if you exit the app
        threading.Thread(target=self.download, args=(url, mode), daemon=True).start()

    def download(self, url, mode):
        try:
            self.log("🔍 Analyzing link and fetching metadata...")
            self.status_label.configure(text="Initializing...", text_color="yellow")

            ydl_opts = {
                'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
                'noplaylist': True,  # Ensures only the single video is grabbed
                'progress_hooks': [self.progress_hook],
                'ffmpeg_location': os.getcwd(), # Looks for ffmpeg.exe in the current folder
            }

            if mode == 'audio':
                self.log("🎵 Setting mode: MP3 Extraction")
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                self.log("🎬 Setting mode: Video (Best Quality)")
                ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.log(f"📦 Title: {info.get('title')}")
                self.log(f"⏱️ Duration: {info.get('duration_string')}")
                
                ydl.download([url])
            
            self.log("💿 Finalizing and converting file...")
            self.log("✨ Success! Download Complete.")
            self.status_label.configure(text="Download Successful!", text_color="green")
            
        except Exception as e:
            error_msg = str(e).split('\n')[0] # Get only the first line of error
            self.log(f"❌ Error: {error_msg}")
            self.status_label.configure(text="Download Failed", text_color="red")

if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()