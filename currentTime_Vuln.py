import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Setup ChromeDriver path
CHROMEDRIVER_PATH = r"C:\PATH TO YOUR CHROMEDRIVER\chromedriver.exe"
TEMP_PROFILE_PATH = os.path.join(os.getcwd(), "lightweight_profile")

# ✅ Chrome options
options = Options()
options.add_argument(f"--user-data-dir={TEMP_PROFILE_PATH}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_argument("--enable-features=AutoplayIgnoreWebAudio")
options.add_argument("start-maximized")
options.add_argument("window-size=1280,800")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ✅ Setup WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# ✅ Bypass `navigator.webdriver` detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# ✅ Open YouTube
driver.get("https://www.youtube.com")

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player"))
    )

    while True:
        try:
            ad_container = driver.find_elements(By.CLASS_NAME, "ad-showing")
            skip_buttons = driver.find_elements(By.CLASS_NAME, "ytp-skip-ad-button")

            if ad_container and len(ad_container) > 0:
                if any(skip_button.is_displayed() and skip_button.is_enabled() for skip_button in skip_buttons):
                    skip_buttons[0].click()
                else:
                    # Jump to last 0.5 sec of ad
                    total_ad_time = driver.execute_script(
                        "return document.querySelector('.html5-main-video').duration;"
                    )
                    if total_ad_time:
                        driver.execute_script(
                            "document.querySelector('.html5-main-video').currentTime = arguments[0];",
                            total_ad_time - 0.5
                        )

                    # Try clicking skip ad for up to 5 seconds
                    for _ in range(10):  # 10 tries * 0.5s = 5 seconds max
                        skip_buttons = driver.find_elements(By.CLASS_NAME, "ytp-skip-ad-button")
                        for skip_button in skip_buttons:
                            if skip_button.is_displayed() and skip_button.is_enabled():
                                skip_button.click()
                                print("Skip button clicked after jump.")
                                break
                        time.sleep(0.5)


            else:
                driver.execute_script(
                    "document.querySelector('.html5-main-video').playbackRate = 1;"
                )

            time.sleep(2)

        except Exception:
            time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    driver.quit()
