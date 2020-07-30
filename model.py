from flask import Markup
from pytz import timezone
import pytz

def time_to_readable(utc_dt):
    eastern = timezone('US/Eastern')
    loc_dt = utc_dt.astimezone(eastern)
    return Markup(loc_dt.strftime('%m-%d-%y %I:%M:%S %p %Z%z'))

def replace_backslash(ending):
    return ending.replace('/','|')

def add_log(if_log_in):
    if if_log_in:
        return Markup('<a class="btn bg-secondary text-light" href="{{url_for("logout")}}"><h4 class="mb-0">Log Out</h4></a>')
    else:
        return Markup('<a class="btn bg-secondary text-light" href="{{url_for("login")}}"><h4 class="mb-0">Log In</h4></a>')