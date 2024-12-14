import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the webhook URL from .env file
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Set the URL for the webpage to scrape
url = "https://www.coinbase.com/blog/increasing-transparency-for-new-asset-listings-on-coinbase"

# Path to the file where new assets will be logged
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
log_file = os.path.join(script_dir, "new_asset.txt")  # Create the full path for the log file

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=525,150")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Additional options to reduce CPU usage and optimize performance
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def check_for_updates():
    driver.get(url)
    time.sleep(10)  # Wait for the page to load completely
    
    try:
        # Find paragraphs that contain 'Contract address:'
        paragraphs = driver.find_elements(By.XPATH, "//p[contains(text(), 'Contract address:')]")

        # Regex pattern to extract asset info from lines like:
        # "QCAD (QCAD) - Contract address: 0x4a16baf414b8e637ed12019fad5dd705735db2e0"
        pattern = re.compile(r"^(.*?)\s*\((.*?)\)\s*-\s*Contract address:\s*(\S+)$")

        new_assets = []
        for p in paragraphs:
            line = p.text.strip()
            match = pattern.match(line)
            if match:
                asset_name, asset_symbol, contract_address = match.groups()
                asset_info = f"{asset_name} ({asset_symbol}) - {contract_address}"

                if not is_asset_logged(asset_info):
                    log_new_asset(asset_info)
                    new_assets.append(asset_info)
                    print(f"New asset detected: {asset_info}")

        if new_assets:
            send_discord_notification(new_assets)
        else:
            print("No new assets found.")
    except Exception as e:
        print(f"Error occurred: {e}")

def is_asset_logged(asset_name):
    # Check if the asset is already logged
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logged_assets = f.read().splitlines()
            return asset_name in logged_assets
    return False

def log_new_asset(asset_name):
    # Log the new asset to the file
    with open(log_file, 'a') as f:
        f.write(asset_name + '\n')

def send_discord_notification(new_assets):
    # Send a notification to Discord with the new assets
    message = "Coinbase has added another asset to their roadmap: <@&1258605945248813117>\n"
    for asset in new_assets:
        message += f"{asset}\n"

    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()

if __name__ == "__main__":
    try:
        while True:
            check_for_updates()
            time.sleep(60)  # Wait for 60 seconds before checking again
    finally:
        driver.quit()  # Close the browser when the script ends
