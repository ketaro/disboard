import os
import datetime
from pytz import timezone, utc
from time import mktime
from flask import flash
import json
import hmac
import hashlib
import time
import config
from base64 import urlsafe_b64encode, urlsafe_b64decode


# Convert a Date or Date/Time into Epoch
def datetime_to_epoch(dt, tz):
    localtz = timezone(os.environ.get('SYSTEM_TIMEZONE', "America/Los_Angeles")) # Local System Timezone
    
    if type(tz) == str or type(tz) == unicode:
        dttz = timezone(tz)                             # pytz Timezone object (if tz is a string)
    else:
        dttz = tz
    
    if type(dt) == datetime.date:
        dt = datetime.datetime.combine(dt, datetime.datetime.min.time())    # Add midnight timestamp
    
    dt_dt    = dttz.localize(dt)
    dt_loc   = localtz.normalize(dt_dt.astimezone(localtz))
    dt_epoch = mktime(dt_loc.timetuple())
    
    return dt_epoch

# Convert Epoch timestamp into a Python DateTime
def epoch_to_datetime(epoch, tz):
    #localtz = timezone("America/Los_Angeles")       # Local System Timezone
    
    if type(tz) == str or type(tz) == unicode:
        dttz = timezone(tz)                             # pytz Timezone object (if tz is a string)
    else:
        dttz = tz
    
    utcdt = datetime.datetime.utcfromtimestamp(int(epoch)).replace(tzinfo=utc)
    
    dt = dttz.normalize(utcdt.astimezone(dttz))
    
    return dt

# Update epoch based on a new localized hour/minute
def epoch_settime(epoch, hour, minute, ampm, tz):
    if type(tz) == str or type(tz) == unicode:
        dttz = timezone(tz) # pytz Timezone object (if tz is a string)
    else:
        dttz = tz

    # Convert to a datetime 
    dt = epoch_to_datetime(epoch, tz)
#     print "epoch: ", epoch
#     print "dt: ", dt
    
    if dt.hour < 6:
        # If the time is earlier than the start for the day, 
        #   assume the updated time we're passing is based
        #   on the previous day.
        dt -= datetime.timedelta(days=1)

    # Make sure we were passed integers
    hour   = int(hour)
    minute = int(minute)

    if ampm == 'pm':
        if hour < 12:
            hour += 12    # 24-hour clock
    else:
        if hour == 12:
            hour = 0    # midnight
        
        if hour < 6:
            # If the time we're updated is earlier than the start
            #   for the day, assume we're techincally referring
            #   to after midnight (the next day)
            dt += datetime.timedelta(days=1)        

    # Update the datetime object with the new hour/minute
    new_dt = datetime.datetime(dt.year, dt.month, dt.day, hour, minute)
#     print "new_dt", new_dt
    
    # Concert the new dt back to epoch
    new_epoch = datetime_to_epoch(new_dt, tz)
#     print "new_epoch: ", new_epoch
#     print "diff: ", ((epoch - new_epoch) /60/60)
    
    return new_epoch


# Return a "friendly" date range string
def date_range_str(start_epoch, end_epoch, tz):
    ret = epoch_to_datetime(start_epoch, tz).strftime('%a %m/%d %I:%M%p')
    ret += '-'
    
    if (epoch_to_datetime(start_epoch, tz).strftime('%m/%d') != epoch_to_datetime(end_epoch, tz).strftime('%m/%d')):
        ret += epoch_to_datetime(end_epoch, tz).strftime('%a %m/%d %I:%M%p')
    else:
        ret += epoch_to_datetime(end_epoch, tz).strftime('%I:%M%p')
    
    return ret
    

# Pass a data dictionary and a secret key, return a signed_request string
def create_signed_request(data, secret):
    data['method'] = 'HMAC-SHA256'
    data['ts'] = int(time.time())
    
    # Convert data into JSON
    datastr = json.dumps(data)
    # base64 encode json data
    dataenc = urlsafe_b64encode(datastr)
        
    # HMAC can only handle ascii (byte) strings
    # http://bugs.python.org/issue5285
    secret = secret.encode('ascii')
    payload = dataenc.encode('ascii')
    
    # Generate payload signature
    datasig = urlsafe_b64encode(
                hmac.new(secret, 
                       msg=payload,
                       digestmod=hashlib.sha256).digest()
            )
    
    signed_request = '.'.join((datasig, dataenc))
        
#    print "datastr: %r" % datastr
#    print "dataenc: %r" % dataenc
#    print "datasig: %r" % datasig
#    print "signed_request=%s" % signed_request
    
    return signed_request

# Pass a signed_request string, validate the signature and return the data payload dictionary
def parse_signed_request(signed_request, secret):
    
    try:
        # Split apart the signed_request
        encsig, payload = map(str, signed_request.split('.', 1))
        
        # Decode the payload (base64 encoded json)
#        data = base64.urlsafe_b64decode(payload + "=" *
#                                        ((4 - len(payload) % 4) % 4))
        datajson = urlsafe_b64decode(payload)
        
        data = json.loads(datajson)
        
    except ValueError:
        return None
    except IndexError:
        # Malformed signed_request
        return None
    except TypeError:
        # Malformed signed_request
        return None

    if data:
        # Determine which method was used to sign the request
        method  = data.get('method', 'HMAC-SHA256')
        datasig = None
        
        # Attempt to verify the request signature
        if method == 'md5':
            datasig = hashlib.md5(str(secret) + str(payload)).hexdigest()
            
        elif method == 'HMAC-SHA256':
            datasig = urlsafe_b64encode(
                        hmac.new(secret, 
                               msg=payload,
                               digestmod=hashlib.sha256).digest()
                    )
        
        # If the signatures do not match, return None    
        if encsig != datasig:
#             print "[parse_signed_request] request failed signature check"
#             print "[parse_signed_request] %s != %s" % (encsig, datasig)
            
            return None
        
        # Check the timestamp of the generated request.  If it's older than
        #    24 hours, expire it
        ts = data.get('ts', time.time())
        if (time.time() - int(ts)) > 60*60*24:
#             print "[parse_signed_request] stale request found (age: %d)" % (time.time() - int(ts))
            return None
    
    return data

# Create a password hash
def hash_password(password):
    return hashlib.md5( hashlib.md5(password).hexdigest() + config.PASSWORD_SALT + password).hexdigest()
    

# Flash Errors
def flash_errors(form):
    # If there were validation errors, flash them to the view
    for field, errors in form.errors.items():
        #print "flash: ", field
        if field == 'csrf_token':
            flash(('danger', 'Session timed out!  Please submit your request again (your information was not saved).'))
        else:
            for error in errors:
                flash(('danger', u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )))

# Converts a select menu list of tuples into a dictionary
def select_choices_dict(choices):
    d = {}
    
    for (key, value) in choices:
        d[key] = value
#        print "key: %s  value: %s" % (key, value)
    
    return d


