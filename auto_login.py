# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001163D380766485CE2AC59A43FC463206A9E6549EF9DF4C68A1E5A2DE2EBD707726E8FC4D55AFCB1A1E76BE5C41B82E62A5D0C1E50790480594AFE41D29B7CAC16614D43AB8A89EF5C4350B588F920C12E448068FD70E9D0103AC60FBDDF5CE9ED86B0725389811E28FFA9B4150DC8D24024371A76BC1A2D94B544367EFC443A8431553AF4E79D61CA78B5D9C9AC7C639D8B979CFB174CBB9DFB7BFFE5FEBD2AED9D89524EC06C4DD112E7C8C048151A213F596CE8119CB59786E4F49D4B0D7A9B233BD7388CC6AC3A3447E42021ABE08F89311068563A03580AB3BB3E3EB25096A81FBE86E6881E2C07F613CA1C3DAB263F10DD090FBEE6ACDAD44326E43AEF2F9FA7A734B4528BF687970753726CA6489F42E98E8751A0BAF112C26864964F18571AA129C2DDCB0DCD1D5C468486BA6252A953AF086EE89117DD823521583171248D2F04BA2EACEEBA1E8F0AF9FD3468042B5F8DB00484EECBD097DCB915D2946FF9842E6AF6222542F701537A92143"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
