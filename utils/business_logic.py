from .interfaces import (BusinessLogicInterface,
                         EngagementsSiteInterface,
                         SummaryPrinterInterface,
                         DriverInterface)


class TwoSiteLogic(BusinessLogicInterface):
    def __init__(self,
                 driver: DriverInterface,
                 site1: EngagementsSiteInterface,
                 site2: EngagementsSiteInterface,
                 summary_printer: SummaryPrinterInterface):
        self.driver = driver
        self.site1 = site1
        self.site2 = site2
        self.summary_printer = summary_printer

    def get_engagements(self):
        """Gets engagements for both given sites."""
        self.site1.find_engagements(self.driver)
        self.site2.find_engagements(self.driver)

    def report_summary(self):
        """Prints a summary of the engagements report from both given sites."""
        self.summary_printer.print_summary()
