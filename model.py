from flask import Markup
from pytz import timezone
import pytz

def time_to_readable(utc_dt):
    eastern = timezone('US/Eastern')
    loc_dt = utc_dt.astimezone(eastern)
    return Markup(loc_dt.strftime('%m-%d-%y %I:%M:%S %p %Z%z'))

def replace_backslash(ending):
    return ending.replace('/','|')