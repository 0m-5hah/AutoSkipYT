# AutoSkipYT

A simple Python script that automates skipping YouTube ads using Selenium by jumping to the end of the video ad. It simulates a real user session in Chrome and avoids bot detection to ensure smooth video playback

PROFILE CREATED WHEN FILE IS RUN

---

## Features

- Detects when an ad is playing
- Skips ads by seeking to the final second of the ad video
- Avoids YouTube automation detection (`navigator.webdriver` patch)
- Runs in visible Chrome window (not headless) for demo purposes
- Uses a clean temporary Chrome profile to avoid session issues

---

## How It Works

1. Launches a Chrome browser with a temporary profile
2. Navigates to YouTube and waits for a video to load
3. Detects ad overlays using YouTube’s internal class names
4. Jumps to the last second of the ad to skip it
5. Continues playback at normal speed if no ad is playing

---

## Requirements

- Python 3.8+
- Google Chrome installed
- ChromeDriver matching your Chrome version ([download here](https://googlechromelabs.github.io/chrome-for-testing/))
- Install dependencies:
  ```bash
  pip install selenium
