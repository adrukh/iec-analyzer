
import sys
import csv
from datetime import datetime, time

def parse_datetime(date_string, time_string):
    """Parses the date and time strings into a single datetime object."""
    try:
        return datetime.strptime(f"{date_string} {time_string}", "%d/%m/%Y %H:%M")
    except ValueError as e:
        raise ValueError(f"Unable to parse date and time: {date_string} {time_string}") from e

def determine_time_of_day(timestamp):
    """Determines the time of day based on the timestamp."""
    parts_of_day = {
        "morning": (time(6, 0), time(11, 59)),
        "afternoon": (time(12, 0), time(17, 59)),
        "evening": (time(18, 0), time(23, 59)),
        "night": (time(0, 0), time(5, 59)),
    }
    for part, (start, end) in parts_of_day.items():
        if start <= timestamp.time() <= end:
            return part
    return None

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
    """Aggregates consumption data by parts of the day."""
    total_consumption = {"morning": 0.0, "afternoon": 0.0, "evening": 0.0, "night": 0.0}
    
    for timestamp, consumption in consumption_data:
        day = timestamp.date()
        part_of_day = determine_time_of_day(timestamp)
        total_consumption[part_of_day] += consumption
        
    return total_consumption

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        input_file = "examples/iec.csv"
    else:
        input_file = sys.argv[1]

    print(f"Analyzing {input_file}")
    normalized_usage_data = process_consumption_csv(input_file)
    period_data = aggregate_usage_by_period(normalized_usage_data)
    
    # plans offer discounts per period, 1 means no discount, .95 is 5%, etc.
    plan_info = {
        'none': {
            'night': 1,
            'morning': 1,
            'afternoon': 1,
            'evening': 1
        },
        'night_only': {
            'night': .8,
            'morning': 1,
            'afternoon': 1,
            'evening': 1
        },
        'day_only': {
            'night': 1,
            'morning': .85,
            'afternoon': .85,
            'evening': 1
        },
        'all_day': {
            'night': .93,
            'morning': .93,
            'afternoon': .93,
            'evening': .93
        }
    }
    
    print("\nTotal Energy Usage:")
    print("-" * 80)
    print(f"{'Period':<25} {'Total consumption (kWh)':<25}")
    print("-" * 80)
    total_consumption = 0
    
    for period in ['night', 'morning', 'afternoon', 'evening']:
        print(f"{period:<25} {period_data[period]:,.3f}")
        total_consumption += period_data[period]
    
    print("-" * 80)
    print(f"{'Plan':<25} {'Cost reduction':<10}")
    for plan in plan_info.keys():
        plan_weighted_usage = 0
        for period in ['night', 'morning', 'afternoon', 'evening']:
            plan_weighted_usage += period_data[period] * plan_info[plan][period]
        print(f"{plan:<25} {100 * (1 - plan_weighted_usage / total_consumption):,.2f}%")
