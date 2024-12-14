# Coinbase Asset Watcher Script

This script monitors the Coinbase blog page for updates regarding new asset listings. When a new asset is detected, it logs the asset details in a file and sends a notification to a specified Discord webhook.

## Features
- Scrapes the Coinbase blog page for new asset announcements.
- Logs new assets in a local file to avoid duplicate notifications.
- Sends Discord notifications with asset details.
- Optimized for low CPU usage with Chrome WebDriver settings.

## Prerequisites
1. Install Python 3.x.
2. Install the required Python packages:
   ```bash
   pip install selenium webdriver-manager discord-webhook python-dotenv
   ```
   Download and install ChromeDriver compatible with your Chrome browser version
   
### Setup
1. **Environment Variables:**
   - Create a `.env` file in the script directory.
   - Add the following line with your Discord webhook URL:
     ```env
     DISCORD_WEBHOOK_URL=https://your-webhook-url-here
     ```

2. **Log File:**
   - Ensure the script directory is writable, as the script will create a file named `new_asset.txt` to log detected assets.

3. **Run the Script:**
   - Execute the script with Python:
     ```bash
     python roadmap_scanner.py
     ```

### Usage
- The script runs in a continuous loop, checking for updates every 60 seconds.
- Any new assets found are logged to `new_asset.txt` and notified via the Discord webhook.

### Customization
- **Check Interval:**
  Adjust the `time.sleep(60)` value in the `__main__` section to change how often the script checks for updates.
- **Discord Notification Message:**
  Modify the `message` content in the `send_discord_notification` function to customize the alert format.
