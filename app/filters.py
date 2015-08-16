import time
import datetime
from pytz import timezone, utc

def jinja2_filter_formatepoch(epoch, tz=None, format='%m-%d-%Y %I:%M:%S %p'):
#     format = '%m-%d-%Y %I:%M:%S %p'
    try:
        epoch = int(epoch)
    except:
        return "-"
    
    if tz:
        if type(tz) == str or type(tz) == unicode:
            zone = timezone(tz)
        else:
            zone = tz
        
        utc_dt = datetime.datetime.utcfromtimestamp(epoch).replace(tzinfo=utc)
        dt = zone.normalize(utc_dt.astimezone(zone))
        return dt.strftime(format)
        
    else:
    	return time.strftime(format, time.localtime(epoch))

# Short datetime format
#   Day MM/DD HH:MI AM
def jinja2_filter_formatepochshort(epoch, tz=None):
    format = '%a %m/%d %I:%M %p'
    epoch = int(epoch)
    
    if tz:
        if type(tz) == str or type(tz) == unicode:
            zone = timezone(tz)
        else:
            zone = tz
        
        utc_dt = datetime.datetime.utcfromtimestamp(epoch).replace(tzinfo=utc)
        dt = zone.normalize(utc_dt.astimezone(zone))
        return dt.strftime(format)
        
    else:
    	return time.strftime(format, time.localtime(epoch))

# epoch date range
def jinja2_filter_formatepochrange(start_epoch, end_epoch, tz=None):
    start_epoch = int(start_epoch)
    end_epoch   = int(end_epoch)
    
    if tz:
        if type(tz) == str or type(tz) == unicode:
            zone = timezone(tz)
        else:
            zone = tz
        
        start_utc_dt = datetime.datetime.utcfromtimestamp(start_epoch).replace(tzinfo=utc)
        start_dt = zone.normalize(start_utc_dt.astimezone(zone))
        end_utc_dt = datetime.datetime.utcfromtimestamp(end_epoch).replace(tzinfo=utc)
        end_dt = zone.normalize(end_utc_dt.astimezone(zone))

        if end_dt.day == start_dt.day and end_dt.month == start_dt.month:
            return start_dt.strftime('%a %m/%d %I:%M %p') + ' - ' + end_dt.strftime('%I:%M %p')

        return start_dt.strftime('%a %m/%d %I:%M %p') + ' - ' + end_dt.strftime('%a %m/%d %I:%M %p')
        
    else:
        if time.strftime('%m/%d', time.localtime(epoch_start)) == time.strftime('%m/%d', time.localtime(epoch_end)):
        	return time.strftime('%a %m/%d %I:%M %p', time.localtime(epoch_start)) + ' - ' + time.strftime('%I:%M %p', time.localtime(epoch_end))
        else:
        	return time.strftime('%a %m/%d %I:%M %p', time.localtime(epoch_start)) + ' - ' + time.strftime('%a %m/%d %I:%M %p', time.localtime(epoch_end))



def jinja2_filter_formatepochdate(epoch, tz=None):
    format = '%m-%d-%Y'
    
    if tz:
        if type(tz) == str or type(tz) == unicode:
            zone = timezone(tz)
        else:
            zone = tz
        
        utc_dt = datetime.datetime.utcfromtimestamp(epoch).replace(tzinfo=utc)
        dt = zone.normalize(utc_dt.astimezone(zone))
        return dt.strftime(format)
        
    else:
    	return time.strftime(format, time.localtime(epoch))

