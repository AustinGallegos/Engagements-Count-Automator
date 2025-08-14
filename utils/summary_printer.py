from utils.interfaces import SummaryPrinterInterface


class SummaryPrinter(SummaryPrinterInterface):
    def __init__(self, shifts):
        self.shifts = shifts

    def print_summary(self):
        """Prints a summary of compiled engagements data."""
        for shift, data in self.shifts.items():
            print(f"{shift}:")
            print(f"  {data["Clean and Recovers"]} Clean and Recovers")
            print(f"  {data["Audit Outliers"]} Audit Outliers")
            print(f"  {data["Sellable Yields"]} Sellable Yields")
            print(f"  {data["Verbal Positives"]} Verbal Positives")
            print(f"  {data["WHDs"]} WHDs\n")
