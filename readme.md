# 🚀 ProStream YouTube Downloader (MVP)

A professional, high-performance media downloader built with Python. ProStream provides a clean, ad-free alternative to web-based downloaders, focusing on user privacy and local processing power.

---

## 📖 Our Journey
ProStream started as a challenge to build a robust, desktop-based YouTube downloader that avoids the pitfalls of shady websites and bloatware. By leveraging the industry-standard **yt-dlp** engine and a modern **CustomTkinter** interface, we’ve created a tool that puts the power back into the user's hands. 

This MVP (Minimum Viable Product) represents the first milestone in building a full-scale media utility suite.

---

## 💎 Free vs. Premium Roadmap

We believe in keeping core features free forever while offering advanced power-user tools for those who want to support the project.

| Feature | Free Version (MVP) | Premium (v2.0) |
| :--- | :---: | :---: |
| Single Video Download (MP4) | ✅ | ✅ |
| High-Quality Audio (MP3) | ✅ | ✅ |
| Custom Save Path Memory | ✅ | ✅ |
| Live Progress Tracking | ✅ | ✅ |
| **4K & 8K Ultra-HD Support** | ❌ | ✅ |
| **Full Playlist/Channel Downloads** | ❌ | ✅ |
| **Multi-threaded Batch Queuing** | ❌ | ✅ |
| **Built-in MP4 to GIF Converter** | ❌ | ✅ |
| **Automatic Updates** | ❌ | ✅ |

---

## 🛠️ Installation & Setup (For Developers)

To run the source code locally, follow these steps:

### 1. Prerequisites
- **Python 3.10+**
- **FFmpeg binaries**: `ffmpeg.exe` and `ffprobe.exe` must be placed in the project root folder to handle media conversion.

### 2. Clone the Repository
git clone [https://github.com/VishalGajjar-GIT/YouTube-Pro-Downloader.git](https://github.com/VishalGajjar-GIT/YouTube-Pro-Downloader.git)
cd YouTube-Pro-Downloader

Technical Architecture
GUI Framework: CustomTkinter for a modern, Windows 11-style dark mode interface.

Download Engine: yt-dlp (The most frequently updated fork of youtube-dl).

Processing: FFmpeg for seamless audio extraction and video merging.

Data Persistence: JSON for saving user preferences (default paths).

Threading: Python Threading module to ensure the GUI remains responsive during large downloads.

🤝 Contributing & Feedback
As this is an MVP, we are actively looking for feedback!

Found a bug? Open an Issue.

Want a feature? Start a discussion in the repository.
