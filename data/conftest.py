import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = r"C:\Users\george\Downloads\chromedriver_win32\chromedriver.exe"  # Change this to your actual path

@pytest.fixture(scope='session')
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    yield driver_instance

    driver_instance.quit()
