
import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

EMAIL = os.environ.get("NAUKRI_EMAIL")
PASSWORD = os.environ.get("NAUKRI_PASSWORD")

RESUME_PATH = os.path.abspath("Ajit Behera_DE.pdf")

# Validate credentials
if not EMAIL or not PASSWORD:
    raise ValueError("Missing Naukri email or password")

# Validate resume file
if not os.path.isfile(RESUME_PATH):
    raise FileNotFoundError(f"Resume not found: {RESUME_PATH}")

# Chrome configuration
options = Options()

# Headless mode only on GitHub Actions
if os.getenv("GITHUB_ACTIONS") == "true":
    options.add_argument("--headless=new")
    print("GitHub Actions: Headless mode enabled")
else:
    print("Local execution: Visible Chrome")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")

driver = None

try:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    # STEP 1: Open login page
    print("Navigating to Naukri login...")

    driver.get("https://www.naukri.com/nlogin/login")

    time.sleep(5)

    print("Login URL:", driver.current_url)
    print("Login page title:", driver.title)

    # STEP 2: Find username and password
    username_input = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "usernameField")
        )
    )

    password_input = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "passwordField")
        )
    )

    username_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)

    # STEP 3: Login
    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )

    login_btn.click()

    print("Login submitted")

    time.sleep(5)

    print("URL after login:", driver.current_url)

    # STEP 4: Open profile
    print("Opening Naukri profile...")

    driver.get("https://www.naukri.com/mnjuser/profile")

    time.sleep(5)

    print("Profile URL:", driver.current_url)
    print("Profile title:", driver.title)

    # STEP 5: Find resume upload input
    print("Searching for file inputs...")

    file_inputs = driver.find_elements(
        By.XPATH,
        "//input[@type='file']"
    )

    print("File inputs found:", len(file_inputs))

    for index, element in enumerate(file_inputs):
        print(
            f"Input {index}: "
            f"ID={element.get_attribute('id')}, "
            f"Name={element.get_attribute('name')}"
        )

    # If no file input is found, save diagnostics
    if not file_inputs:
        driver.save_screenshot("upload_error.png")

        with open(
            "upload_debug.html",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(driver.page_source)

        raise Exception(
            "No file upload input found on Naukri profile"
        )

    # STEP 6: Upload resume
    file_input = file_inputs[0]

    print("Uploading resume...")

    file_input.send_keys(RESUME_PATH)

    time.sleep(5)

    driver.save_screenshot("upload_result.png")

    print("Resume file selected successfully")

except Exception:
    print("An error occurred during the Naukri update.")

    if driver:
        print("Current URL:", driver.current_url)

        try:
            driver.save_screenshot("error.png")
        except Exception as screenshot_error:
            print("Screenshot failed:", screenshot_error)

    raise

finally:
    if driver:
        driver.quit()
