
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

def aggregate_consumption_by_parts_of_day(consumption_data):
    """Aggregates consumption data by day and parts of the day."""
    daily_consumption = {}
    
    for timestamp, consumption in consumption_data:
        day = timestamp.date()
        part_of_day = determine_time_of_day(timestamp)
        
        if day not in daily_consumption:
            daily_consumption[day] = {"morning": 0.0, "afternoon": 0.0, "evening": 0.0, "night": 0.0}
        
        if part_of_day:
            daily_consumption[day][part_of_day] += consumption
    
    return daily_consumption

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        input_file = "examples/iec.csv"
    else:
        input_file = sys.argv[1]

    print(f"Analyzing {input_file}")
    consumption_data = process_consumption_csv(input_file)
    daily_aggregates = aggregate_consumption_by_parts_of_day(consumption_data)
    
    for day, parts in daily_aggregates.items():
        print(f"Date: {day}")
        for part, total in parts.items():
            print(f"  {part.capitalize()}: {total:.3f} kWh")
