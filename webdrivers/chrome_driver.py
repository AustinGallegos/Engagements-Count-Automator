from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.interfaces import DriverInterface


class ChromeDriver(DriverInterface):
    def setup_driver(self):
        """Set up and return a Selenium WebDriver object."""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        return driver
