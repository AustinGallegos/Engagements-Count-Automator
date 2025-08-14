import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.interfaces import EngagementsSiteInterface


class Durable(EngagementsSiteInterface):
    def __init__(self, shifts, dates):
        self.driver = None
        self.shifts = shifts
        self.dates = dates

    def find_engagements(self, driver):
        self.driver = driver
        self.goto_durable()
        self.click_report_button()

        for shift in self.shifts:
            print(f"Looking up {shift} Durables...")
            self.handle_date_entry(shift)

            self.submit_report()
            positives, whd = self.parse_engagements()

            self.shifts[shift]["Verbal Positives"] = positives  # record verbal positive results
            self.shifts[shift]["WHDs"] = whd  # record whd results

    def goto_durable(self):
        """Navigate to the Durable reporting website."""
        durable_link = os.getenv("DURABLE_LINK")
        self.driver.get(durable_link)

    def click_report_button(self):
        """Click the report button on the Durable site."""
        report_button = self.driver.find_element(By.ID, "report")
        report_button.click()

    def handle_date_entry(self, shift):
        start_field = self.driver.find_element(By.ID, "start_date")
        end_field = self.driver.find_element(By.ID, "end_date")

        start_datetime, end_datetime = self.get_date_range(shift)
        self.set_date_field(start_field, start_datetime)
        self.set_date_field(end_field, end_datetime)

    def set_date_field(self, field_element, date_string):
        """Clear and input a date/time string into a date field."""
        field_element.click()

        for _ in range(8):
            field_element.send_keys(Keys.RIGHT)

        for _ in range(19):
            field_element.send_keys(Keys.BACKSPACE)

        field_element.send_keys(date_string)

    def get_date_range(self, shift):
        """Generate start and end datetime strings for a given shift."""
        start_datetime = f"{self.dates["yesterday"]} {self.shifts[shift]["Start"]}"
        if shift == "NIT":
            end_datetime = f"{self.dates["today"]} {self.shifts[shift]["End"]}"
        else:
            end_datetime = f"{self.dates["yesterday"]} {self.shifts[shift]["End"]}"
        return start_datetime, end_datetime

    def submit_report(self):
        """Click the submit button to generate the report."""
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

    def parse_engagements(self):
        """Retrieve and return the relevant engagement elements."""
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr td")
        positives = [el for el in elements if el.text == "REVERSE_LOGISTICS_VERBAL_POSITIVE"]
        whd = [el for el in elements if el.text == "WHD"]
        return len(positives), len(whd)
