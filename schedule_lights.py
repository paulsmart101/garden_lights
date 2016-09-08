# Paul Smart, 2016
# Turn on the garden lights when it gets dusk and turn them off again when it's properly dark.

import time, json, os, requests
import datetime

debug = True
minutes_on_before_sunset = 10
minutes_duration_on = 45
minutes_early_for_cloud = 20

if debug:
	print "minutes_on_before_sunset",minutes_on_before_sunset
	print "minutes_duration_on",minutes_duration_on
	print "minutes_early_for_cloud",minutes_early_for_cloud

# Request sunrise and sunset times from sunrise-sunset.org with lat and long of garden
if debug: print "Making request for surise and sunset times"
sunrise_sunset_url = 'http://api.sunrise-sunset.org/json?lat=51.150719&lng=-0.973177&formatted=0'
r = requests.get(sunrise_sunset_url)

today = r.json()
if debug: print "today:",today

# Extract the sunrise and sunset times from the response.
sunrise = today['results']['sunrise']
sunset = today['results']['sunset']

# Chop up the date and time so it can be used as a datetime
sunset_year = int(sunset[0:4])
sunset_month = int(sunset[5:7])
sunset_day = int(sunset[8:10])
sunset_hour = int(sunset[11:13])
sunset_min = int(sunset[14:16])
sunset_second = int(sunset[17:19])
sunset_microsecond = 0
sunset_tzinfo = sunset[19:25]

# Create a datetime object for the chopped up sunsest time
sunset_time = datetime.datetime(sunset_year,sunset_month,sunset_day,sunset_hour,sunset_min,sunset_second)
if debug:
	print "Results from the surise suset service:"
	print "sunrise",sunrise
	print "sunset",sunset
	print "sunset year",sunset_year
	print "sunset month",sunset_month
	print "sunset day",sunset_day
	print "sunset_hours",sunset_hour
	print "sunset_mins",sunset_min
	print "sunset_seconds",sunset_second
	print "sunset_microseconds",sunset_microsecond
	print "sunset_tzinfo",sunset_tzinfo
	print "sunset_time",sunset_time

# Create a variable of type datetime for the number of minutes before sunset the lights should come on
early_delta = datetime.timedelta(minutes=minutes_on_before_sunset)
if debug: print "early_delta",early_delta

# Take the early time minutes off the sunset time
on_time = sunset_time - early_delta
if debug: print "on_time",on_time

# Find the timezone offset for the current location and time from Google maps
timestamp_now = int(time.time())
url = 'https://maps.googleapis.com/maps/api/timezone/json?location=51.150719,-0.973177&timestamp='+str(timestamp_now)+'&key=AIzaSyDt4CqScO30JJoHGv-XEaGlYSI5ycHvKg4'
if debug: print "URL for timezone:",url
t = requests.get(url)
timezone = t.json()
if debug: print "timezone response",timezone

# Extract just the timezone offset in seconds from the response
offset_seconds = int(timezone['dstOffset'])
if debug: print "offset_seconds",offset_seconds

# Create a variable of type datetime to hold the offset is seconds
timezone_delta = datetime.timedelta(seconds=timezone['dstOffset'])
if debug: print "timezone_delta",timezone_delta

# Add the timezone offset to the on time
on_time = on_time + timezone_delta
if debug: print "on_time",on_time

# Find if it will be overcast by calling openweathermap with a city (needs changing to 2657408)
weather_url = "http://api.openweathermap.org/data/2.5/weather?id=2657408&appid=89a48914b23af2d6a788a8f298caaf7c"
w = requests.get(weather_url)
weather = w.json()
if debug: print "weather",weather

# Extract cloud cover percentage
cloud_cover = weather['clouds']['all']
# One minute for every 2 percent of cloud cover
cloud_cover_mins = int(cloud_cover/5)
if debug:
	print "cloud_cover",cloud_cover
	print "cloud_cover_mins",cloud_cover_mins

# Create a datetime delta of the number of minutes to be early for cloud cover
cloud_delta = datetime.timedelta(minutes=minutes_early_for_cloud)
# Subtract the cloud minutes from the switch on time
on_time = on_time - cloud_delta
if debug: print "on_time",on_time

# Set the off time
duration_delta = datetime.timedelta(minutes=minutes_duration_on)
if debug:
	print "minutes_duration_on",minutes_duration_on
	print "duration_delta",duration_delta

off_time = on_time + duration_delta + cloud_delta
if debug: print "off_time",off_time

# Make the time strings to be passed to at jobs
on_time_string = on_time.strftime("%H:%M %x")
off_time_string = off_time.strftime("%H:%M %x")
if debug:
	print on_time_string
	print off_time_string

# Make the full at job strings for calls to create the at jobs, calling a shell script to switch the socket on and off
on_string = "at "+on_time_string+" -f /home/pi/garden_lights/switch_on.sh"
off_string = "at "+off_time_string+" -f /home/pi/garden_lights/switch_off.sh"

if debug:
	print "Strings being sent to the system"
	print on_string
	print off_string

# Make system calls
os.system(on_string)
os.system(off_string)

#Call to Zapier to trigger emails, sms, zombie apocalypse, whatever
send = requests.post('https://hooks.zapier.com/hooks/catch/295110/6yphdr/',data = {'on':on_time,'off':off_time})
if debug: print send

