# Indee TV Automation Script

This Python script automates testing of the Indee TV demo website using Selenium WebDriver.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Chrome browser** installed
3. **ChromeDriver** installed and accessible at `/usr/local/bin/chromedriver`

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure ChromeDriver is installed and in your PATH:
   ```bash
   # On macOS with Homebrew:
   brew install chromedriver
   
   # Or download manually from: https://chromedriver.chromium.org/
   ```

## Usage

Run the automation script:
```bash
python indee_automation.py
```

## What the script does

1. **Login**: Opens the Indee TV demo site and logs in using the provided PIN
2. **Navigate**: Opens the "Test automation project"
3. **Video Playback**: Plays video for 10 seconds, then pauses
4. **Continue Watching**: Resumes video playback using the "Continue Watching" button
5. **Navigation**: Returns to the main titles page
6. **Logout**: Logs out of the application

## Configuration

- The script uses Chrome with various stability flags optimized for macOS
- Default wait time is 15 seconds for element interactions
- ChromeDriver path is set to `/usr/local/bin/chromedriver`

## Troubleshooting

- If ChromeDriver is not found, update the `driver_path` variable in the script
- For headless testing, uncomment the headless option in the Chrome options
- Ensure you have a stable internet connection for the demo site

## Notes

- The script includes comprehensive error handling and cleanup
- All interactions use explicit waits for better reliability
- The Chrome options are optimized for stability on macOS systems 
