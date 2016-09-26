# garden_lights
Raspberry Pi in my shed switches my garden lights on when it gets dark and off some time later.
Uses an Energenie controller https://energenie4u.co.uk/catalogue/product/ENER002-2PI

Cron job on Raspberry Pi running as 'pi' calls the scheduling python program at noon.
See crontab.txt for settings.

schedule_lights_on.py makes calls to various services to determin sunset time, time zone and cloud cover then makes two system calls creating at jobs to turn the lights on and off.

