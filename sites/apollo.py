import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.interfaces import EngagementsSiteInterface


class Apollo(EngagementsSiteInterface):
    def __init__(self, shifts, dates, audits):
        self.driver = None
        self.shifts = shifts
        self.dates = dates
        self.audits = audits

    def find_engagements(self, driver):
        self.driver = driver

        for audit_name, audit_id in self.audits.items():
            self.goto_apollo()
            self.click_apollo_audit(audit_id)

            for shift in self.shifts:
                print(f"Looking up {shift} {audit_name}...")
                self.handle_date_entry(shift)

                self.submit_apollo_query()
                engagements = self.process_apollo_results()

                if not engagements:
                    self.handle_no_results()

                self.shifts[shift][audit_name] = len(engagements)  # record engagement results

    def goto_apollo(self):
        """Navigates to the Apollo dashboard."""
        self.driver.get(os.getenv("APOLLO_LINK"))

    def click_apollo_audit(self, audit_id):
        """Clicks on the specific audit type by ID."""
        self.driver.find_element(By.ID, audit_id).click()

    def handle_date_entry(self, shift):
        """Enters start and end dates for a given shift."""
        start_field = self.driver.find_element(By.ID, "start_date")
        end_field = self.driver.find_element(By.ID, "end_date")

        start_time, end_time = self.get_date_range(shift)
        self.clear_and_set_date_input(start_field, start_time)
        self.clear_and_set_date_input(end_field, end_time)

    def clear_and_set_date_input(self, input_element, date_str):
        """Clears an input element and enter a formatted date string."""
        input_element.click()
        for _ in range(8):
            input_element.send_keys(Keys.RIGHT)
        for _ in range(19):
            input_element.send_keys(Keys.BACKSPACE)
        input_element.send_keys(date_str)

    def get_date_range(self, shift):
        """Gets the start and end datetime strings for the given shift."""
        start_time = f"{self.dates["yesterday"]} {self.shifts[shift]["Start"]}"
        if shift == "NIT":
            end_time = f"{self.dates["today"]} {self.shifts[shift]["End"]}"
        else:
            end_time = f"{self.dates["yesterday"]} {self.shifts[shift]["End"]}"
        return start_time, end_time

    def submit_apollo_query(self):
        """Click the "Search" button and wait for results to load."""
        self.driver.find_element(By.NAME, "commit").click()
        time.sleep(2)

    def handle_no_results(self):
        """Handle case where no results were found."""
        back_button = self.driver.find_element(By.LINK_TEXT, "Go Back")
        back_button.click()

    def process_apollo_results(self):
        """Retrieve and return engagement elements from Apollo results."""
        return self.driver.find_elements(By.CLASS_NAME, "col-md-6.d-flex")
