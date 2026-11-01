import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

EMAIL = os.environ.get("NAUKRI_EMAIL")
PASSWORD = os.environ.get("NAUKRI_PASSWORD")

RESUME_PATH = os.path.abspath("Ajit Behera_DE.pdf")

options = Options()

# Run Chrome without opening a visible window
options.add_argument("--headless=new")

# Required for GitHub Actions Ubuntu
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Additional stability options
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Navigating to Naukri login...")
    driver.get("https://www.naukri.com/nlogin/login")
    time.sleep(3)

    # Fill credentials
    username_input = driver.find_element(By.ID, "usernameField")
    password_input = driver.find_element(By.ID, "passwordField")
    username_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)

    # Click login
    login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_btn.click()
    time.sleep(5)

    # Navigate to profile edit page
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(4)

    # Find the hidden file input for resume attachment and upload
    file_input = driver.find_element(By.XPATH, "//input[@type='file' and contains(@id, 'attachCV')]")
    file_input.send_keys(RESUME_PATH)
    time.sleep(5)

    print("Resume successfully Updated!")

except Exception as e:
    print(f"Error occurred: {e}")
    driver.save_screenshot("error.png")
    raise e

finally:
    driver.quit()
