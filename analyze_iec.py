
import settings
import sys
import csv
from datetime import datetime, time

def parse_datetime(date_string, time_string):
    """Parses the date and time strings into a single datetime object."""
    try:
        return datetime.strptime(f"{date_string} {time_string}", "%d/%m/%Y %H:%M")
    except ValueError as e:
        raise ValueError(f"Unable to parse date and time: {date_string} {time_string}") from e

def process_consumption_csv(file_path):
    """Processes the consumption data from the new CSV format."""
    consumption_data = []
    
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        
        # Skip initial irrelevant rows to get to the data
        for _ in range(12):  # Adjust based on the new format structure
            next(reader, None)
        
        # Process consumption data
        for row in reader:
            if len(row) < 3 or not row[0].strip():
                continue
            
            date = row[0].strip()
            time = row[1].strip()
            consumption = float(row[2].strip())
            
            try:
                timestamp = parse_datetime(date, time)
                consumption_data.append((timestamp, consumption))
            except ValueError as e:
                print(f"Skipping invalid row: {row}. Error: {e}")
    
    return consumption_data

def aggregate_usage_by_period(consumption_data):
    """Aggregates consumption data"""
    total_consumption = 0
    period_consumption = {period: 0 for period in settings.day_periods}
    month_consumption = {month: 0 for month in range(1, 13)}
    
    for timestamp, consumption in consumption_data:
        day_period = settings.get_day_period(timestamp)
        total_consumption += consumption
        period_consumption[day_period] += consumption
        month_consumption[timestamp.month] += consumption
        
    return total_consumption, period_consumption, month_consumption

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        input_file = "examples/iec.csv"
    else:
        input_file = sys.argv[1]

    print(f"Analyzing {input_file}")
    normalized_usage_data = process_consumption_csv(input_file)
    total_consumption, period_data, month_data = aggregate_usage_by_period(normalized_usage_data)
    
    print("\nEnergy Usage by Day Period:")
    print("-" * 80)
    print(f"{'Period':<25} {'Total consumption (kWh)':<25}")
    print("-" * 80)
    for period in settings.day_periods:
        print(f"{period:<25} {period_data[period]:,.3f}")
    
    print("\nEnergy Usage by Month:")
    print("-" * 80)
    print(f"{'Month':<25} {'Total consumption (kWh)':<25}")
    print("-" * 80)
    for month in range(1, 13):
        if month_data[month] > 0:
            print(f"{month:<25} {month_data[month]:,.3f}")

    print("\nCalculated cost reduction by plan:")
    print("-" * 80)
    print(f"{'Plan':<40} {'Overall cost reduction':<10}")
    print("-" * 80)
    for plan in settings.plans.keys():
        plan_weighted_usage = 0
        for period in settings.day_periods:
            plan_weighted_usage += period_data[period] * settings.plans[plan]['discounts'][period]
        print(f"{settings.plans[plan]['details']:<40} {100 * (1 - plan_weighted_usage / total_consumption):,.2f}%")
