import sys
import csv
from datetime import datetime, time
from collections import defaultdict

def parse_date(date_string):
    """
    Attempts to parse date string using multiple common formats.
    
    Parameters:
    date_string (str): Date string to parse
    
    Returns:
    datetime: Parsed datetime object
    """
    date_formats = [
        '%Y-%m-%dT%H:%M:%S',         # 2024-08-01T12:00:00
        '%b %d, %Y %I:%M:%S %p',     # Aug 1, 2024 12:00:00 AM
        '%B %d, %Y %I:%M:%S %p',     # August 1, 2024 12:00:00 AM
        '%Y-%m-%d %H:%M:%S',         # 2024-08-01 12:00:00
        '%m/%d/%Y %H:%M:%S',         # 08/01/2024 12:00:00
        '%d/%m/%Y %H:%M:%S',         # 01/08/2024 12:00:00
        '%d-%m-%Y %H:%M:%S',         # 01-08-2024 12:00:00
    ]
    
    for date_format in date_formats:
        try:
            return datetime.strptime(date_string.split('.')[0], date_format)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date string: {date_string}")

def get_day_period(dt):
    """
    Determines which period of the day a datetime falls into.
    
    Parameters:
    dt (datetime): The datetime to check
    
    Returns:
    str: Period name ('night', 'morning', 'afternoon', or 'evening')
    """
    hour = dt.hour
    
    if 7 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 23:
        return 'evening'
    else:  # hour 23 or 0-6
        return 'night'

def analyze_energy_data(input_file):
    """
    Analyzes energy data by day periods.
    
    Parameters:
    input_file (str): Path to input CSV file with 15-min data
    """
    # Dictionary to store period data
    # Structure: {period: {'consumption': total, 'production': total, 'readings': number_of_15min_readings}}
    period_data = defaultdict(lambda: {'consumption': 0.0, 'production': 0.0, 'readings': 0})
    
    # Read input file and process data
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Get field names from the reader
        date_field = None
        consumption_field = None
        production_field = None
        
        # Identify the relevant fields based on common names
        for field in reader.fieldnames:
            if 'תאריך' in field:
                date_field = field
            elif 'צריכה' in field:
                consumption_field = field
            elif 'הזרמה' in field:
                production_field = field
        
        if not all([date_field, consumption_field, production_field]):
            raise ValueError("Could not identify required fields in CSV. "
                           f"Found: date={date_field}, consumption={consumption_field}, "
                           f"production={production_field}")
        
        # Keep track of statistics
        total_rows = 0
        start_date = None
        end_date = None
        duplicate_count = 0
        error_count = 0
        previous_dt = None
        
        # Store unique 15-min readings
        fifteen_min_data = {}
        
        # First pass: collect deduplicated data
        for row in reader:
            total_rows += 1
            try:
                # Parse the datetime
                dt = parse_date(row[date_field])

                # keep track of statistics
                if (not start_date):
                    start_date = dt
                end_date = dt

                # Check if this is a duplicate (same timestamp as previous row)
                if previous_dt == dt:
                    duplicate_count += 1
                
                # Store this reading (will overwrite any previous reading for this timestamp)
                fifteen_min_data[dt] = {
                    'consumption': float(row[consumption_field]),
                    'production': float(row[production_field])
                }
                
                previous_dt = dt
                
            except ValueError as e:
                error_count += 1
                print(f"Warning: Skipping row due to invalid data: {row}. Error: {str(e)}")
                continue
            except Exception as e:
                error_count += 1
                print(f"Warning: Unexpected error processing row: {row}. Error: {str(e)}")
                continue
        
        # Second pass: analyze deduplicated data by period
        for dt, values in fifteen_min_data.items():
            period = get_day_period(dt)
            period_data[period]['consumption'] += values['consumption']
            period_data[period]['production'] += values['production']
            period_data[period]['readings'] += 1
    
    # Calculate and print hourly averages for each period
    period_info = {
        'night': {'name': 'Night (23:00-07:00)', 'hours': 8},
        'morning': {'name': 'Morning (07:00-12:00)', 'hours': 5},
        'afternoon': {'name': 'Afternoon (12:00-17:00)', 'hours': 5},
        'evening': {'name': 'Evening (17:00-23:00)', 'hours': 6}
    }

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
    print(f"{'Period':<25} {'Total consumption (kWh)':<25} {'Total production (kWh)':<25}")
    print("-" * 80)
    total_consumption = 0
    total_production = 0
    
    for period in ['night', 'morning', 'afternoon', 'evening']:
        data = period_data[period]
        info = period_info[period]
        
        if data['readings'] > 0:
            print(f"{info['name']:<25} {data['consumption']:,.3f} {' ':<20} {data['production']:,.3f}")
            total_consumption += data['consumption']
            total_production += data['production']
    
    print("-" * 80)
    print(f"{'Plan':<25} {'Cost reduction':<10}")
    for plan in plan_info.keys():
        plan_weighted_usage = 0
        for period in ['night', 'morning', 'afternoon', 'evening']:
            plan_weighted_usage += period_data[period]['consumption'] * plan_info[plan][period]
        print(f"{plan:<25} {100 * (1 - plan_weighted_usage / total_consumption):,.2f}%")

    print("-" * 80)
    print(f"\nData summary:")
    print(f"- Total readings processed: {total_rows}")
    print(f"- Readings start date: {start_date}")
    print(f"- Readings end date: {end_date}")
    print(f"- Duplicate entries found: {duplicate_count}")
    print(f"- Errors encountered: {error_count}")
    print(f"- Unique days in dataset: {len(set(dt.date() for dt in fifteen_min_data.keys()))}")
    
    # Return the period data for potential further analysis
    return period_data

# Example usage
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        input_file = "examples/cellcom.csv"
    else:
        input_file = sys.argv[1]
    
    print(f"Analyzing {input_file}")
    try:
        period_data = analyze_energy_data(input_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")