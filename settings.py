# generic settings for analysis

day_periods = ['night', 'morning', 'afternoon', 'evening']

def get_day_period(dt):
    """
    Determines which period of the day a datetime falls into.
    
    Parameters:
    dt (datetime): The datetime to check
    
    Returns:
    str: Period name ('night', 'morning', 'afternoon', or 'evening')
    """
    if 7 <= dt.hour < 12:
        return 'morning'
    elif 12 <= dt.hour < 17:
        return 'afternoon'
    elif 17 <= dt.hour < 23:
        return 'evening'
    else:  # dt.hour 23 or 0-6
        return 'night'

# discount plans offered by utility providers
# must include discount rates (0 <= rate <= 1) for each defined day period
plans = {
    'night_only': {
        'details': '20% discount between 23:00 and 7:00',
        'discounts': {
          'night': .8,
          'morning': 1,
          'afternoon': 1,
          'evening': 1
        }
    },
    'day_only': {
        'details': '15% discount between 7:00 and 17:00',
        'discounts': {
          'night': 1,
          'morning': .85,
          'afternoon': .85,
          'evening': 1
        }
    },
    'all_day': {
        'details': '7% discount across the entire day',
        'discounts': {
          'night': .93,
          'morning': .93,
          'afternoon': .93,
          'evening': .93
        }
    }
}