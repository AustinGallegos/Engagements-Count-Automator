from abc import ABC, abstractmethod


class EngagementsSiteInterface(ABC):
    @abstractmethod
    def find_engagements(self, driver):
        pass


class DriverInterface(ABC):
    @abstractmethod
    def setup_driver(self):
        pass


class BusinessLogicInterface(ABC):
    @abstractmethod
    def __init__(self, driver, summary_printer):
        self.driver = driver
        self.summary_printer = summary_printer

    @abstractmethod
    def get_engagements(self):
        pass

    @abstractmethod
    def report_summary(self):
        pass


class SummaryPrinterInterface(ABC):
    @abstractmethod
    def __init__(self, shifts):
        self.shifts = shifts

    @abstractmethod
    def print_summary(self):
        pass
