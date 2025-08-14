import os
import datetime
import utils
from sites.apollo import Apollo
from sites.durable import Durable
from webdrivers.chrome_driver import ChromeDriver


def main():

    shifts = {
        "MOR": {"Start": "04:00", "End": "09:00"},
        "DAY": {"Start": "09:00", "End": "15:00"},
        "TWI": {"Start": "15:00", "End": "20:00"},
        "NIT": {"Start": "20:00", "End": "04:00"}
    }

    today = datetime.date.today()
    dates = {
        "today": today,
        "yesterday": today - datetime.timedelta(days=1)
    }

    audits = {
        "Clean and Recovers": os.getenv("CLEAN"),
        "Audit Outliers": os.getenv("OUTLIER"),
        "Sellable Yields": os.getenv("YIELD")
    }

    driver_obj = ChromeDriver()
    driver = driver_obj.setup_driver()

    apollo = Apollo(shifts, dates, audits)
    durable = Durable(shifts, dates)
    summary_printer = utils.SummaryPrinter(shifts)

    business_logic = utils.TwoSiteLogic(driver, apollo, durable, summary_printer)
    business_logic.get_engagements()
    business_logic.report_summary()

    driver.quit()


if __name__ == "__main__":
    main()
