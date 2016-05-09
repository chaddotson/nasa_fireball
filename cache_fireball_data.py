
from datetime import date
from os.path import exists, join
import re
from requests import get


url = "http://fireballs.ndc.nasa.gov/"
cache_dir = "./fireball_data_cache/"
main_index = get(url)


source_of_index = main_index.text


pattern = re.compile("(\d{8}.html)")

#pages = pattern.findall(source_of_index)

orbit_pattern = re.compile("(evcorr/\d{8}/\d{8}_\d{6}[A-Z]/orbit.txt)")


def get_file(url, filename):
    r = get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


current_date = date.today()

while current_date >= date(year=1980, month=1, day=1):

    current_date_partial_url = current_date.strftime("%Y%m%d") + ".html"

    print("Getting date summary page {0}".format(current_date_partial_url))

    day_page_source = get(url + current_date_partial_url)

    event_orbit_partial_urls = orbit_pattern.findall(day_page_source.text)

    for event in event_orbit_partial_urls:
            filename = join(cache_dir, event.replace("/", "_"))
            if not exists(filename):
                print("Caching file:", event)
                get_file(url+event, filename)

    current_date = date.fromordinal(current_date.toordinal()-1)

