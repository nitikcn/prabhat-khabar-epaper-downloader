## Prabhat Khabar E-Paper downloader
## 24-03-2024, Monday

import os
import sys
import requests
import re
import traceback

import bs4
import datetime as dt


today_isoformat_date = dt.date.isoformat(dt.datetime.now())     # like 2024-03-23

# Check if the argument date is correctly formatted
if len(sys.argv) > 1:
    if len(sys.argv[1]) == 10:
        date_regex = re.compile('\d{4}-\d{2}-\d{2}')
        mo = date_regex.search(sys.argv[1])
        if mo:
            today_isoformat_date = sys.argv[1]
        else:
            raise Exception('Could not understand the given date')
            
cwd = f'./Prabhat Khabar E-Papers/{today_isoformat_date}'
os.makedirs(cwd, exist_ok=True)
os.chdir(cwd)

# Full url is like https://epaper.prabhatkhabar.com/patna/patna-city/2024-03-23/1, the number after the last slash is page num
epaper_part_url = 'https://epaper.prabhatkhabar.com/patna/patna-city/' + today_isoformat_date
base_url_for_pic = 'https://epaper.prabhatkhabar.com/'


for i in range(1, 50):  # chose max page num to be 50 randomly
    page_url = f'{epaper_part_url}/{i}'

    # Download page url at first
    try_counter = 0
    while try_counter < 6:
        try:
            try_counter += 1;
            page_html = requests.get(page_url)
            page_html.raise_for_status()
        except:
            traceback_str = traceback.format_exc()
            if 'KeyboardInterrupt' in traceback_str:
                raise KeyboardInterrupt
            if try_counter == 5:
                raise Exception(f'Could not download page url: {page_url}')
            continue    # if the above code ran, the execution won't reach here
        else:
            break

    # Get epaper page's pic url
    page_soup = bs4.BeautifulSoup(page_html.text)
    pic_elem = page_soup.select_one('#main-image-page')
    if pic_elem is None:
        print('Last page has been downloaded.')
        sys.exit()
    pic_src = pic_elem.get('src')

    # Download the pic url
    try_counter = 0
    while try_counter < 6:
        try:
            try_counter += 1
            pic_url = base_url_for_pic + pic_src
            pic = requests.get(pic_url)
            pic.raise_for_status()
        except:
            traceback_str = traceback.format_exc()
            if 'KeyboardInterrupt' in traceback_str:
                raise KeyboardInterrupt
            if try_counter == 5:
                raise Exception(f'Could not download pic url: {pic_url}')
        else:
            break
        
    with open(f'{i}.jpg', 'wb') as f:
        for chunk in pic.iter_content(100,000):
            f.write(chunk)
