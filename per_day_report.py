cache_dir = "./fireball_data_cache/"

import re
from os import listdir
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta

event_date_pattern = re.compile("evcorr_\d{8}_(\d{8})_\d{6}[A-Z]_orbit.txt")

events_per_day = Counter()

for file in listdir(cache_dir):
    match = event_date_pattern.match(file)

    if not match:
        continue

    events_per_day[datetime.strptime(match.groups()[0],"%Y%m%d").date()] += 1


for key in sorted(events_per_day.keys()):

    last_year = key - relativedelta(years=1)

    print(key, events_per_day[key], "Last:", last_year, events_per_day.get(last_year, 0))

