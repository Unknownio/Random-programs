# YouTube Media Downloader 🎥🎶

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-v14+-green.svg)](https://nodejs.org/)

A simple yet powerful Node.js script that allows you to download **YouTube videos** and **audio** files effortlessly! Whether you need a high-quality **MP4 video** or just the **MP3 audio**, this script has you covered. It offers a clean interface and real-time download progress, so you can keep track of your downloads in style.

## ✨ Features
- **Download YouTube videos in MP4 format** 🎥
- **Extract and download audio in MP3 format** 🎶
- **Real-time download progress**, including speed and ETA ⏳
- Automatically sanitizes video titles for safe file names
- Saves media files to a `Downloads` folder for easy access
- Supports downloading multiple videos in one session

## 🚀 Quick Start

```bash
# 1. Clone the repository:
git@github.com:Unknownio/Random-programs.git
cd Random-program

# 2. Install dependencies:
npm install

# 3. Install yt-dlp:
# For Windows:
# Download yt-dlp with the install.bat
# For Linux:
sudo curl -L https://yt-dlp.org/downloads/latest/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# 4. Run the script:
node main.js
```
## 🎮 How It Works
URL Input: The script will prompt you to paste a YouTube video URL.
Format Choice: After entering the URL, you'll be asked to choose the format:
- MP4 for video downloads
- MP3 for audio downloads
Download Progress: The script displays download progress, including percentage, speed, and estimated time remaining.
File Storage: The media is saved in a Downloads folder in the same directory as the script.
## Example Output:
- Paste the YouTube video URL: https://www.youtube.com/watch?v=example
- Do you want to download MP4 (video) or MP3 (audio)? (Enter "mp4" or "mp3"): mp3
- Downloading MP3...
- [download]  45.3% of 5.60MiB at 550.00KiB/s ETA 00:05
- [download]  100% of 5.60MiB in 00:12
- Audio downloaded: ./Downloads/video_title.mp3

## ⚙️ Customization
Feel free to modify the script to suit your needs:

Change the download directory: Modify the line where the filePath is set to change where the downloads are saved.
Add more formats: If you want to support more formats, modify the yt-dlp commands in the script.
## 🔧 Requirements
- Node.js v14+ (Install from Node.js official site)
- yt-dlp for video/audio downloading (See the installation guide above)
- Internet connection to download the media from YouTube
## 📜 License
- This project is licensed under the MIT License - see the LICENSE file for details.

## ✨ Contributions
- Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Unknownio/Random-programs/issues) or submit a pull request.

## 💬 Contact
- If you have any questions or feedback, please feel free to reach out at gamerpubg1008@gmail.com.

Made with ❤️ by Unknownio

