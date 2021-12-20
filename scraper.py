#!/usr/bin/env python
"""Scraper.py: this is a web scrapper."""

import mechanicalsoup
#import pandas as pd
#import sqlite3

__author__ = "Nader Jemaa"
__copyright__ = "Copyright 2021, Tunisia"

BASE_URL = "https://nationaltoday.com"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december"]

BROWSER = mechanicalsoup.StatefulBrowser()

def get_holidays_by_month(month_str, day_int):
    """get all holidays by month and day"""
    final_url = ""
    if month_str.lower() in MONTHS:
        final_url = BASE_URL + "/" + month_str.lower() + "-" + str(day_int) + "-holidays"
    BROWSER.open(final_url)
    holiday_title = BROWSER.page.find_all("h3", attrs={"class":"holiday-title"})
    holiday_title_array = [value.text for value in holiday_title]
    holiday_desc = BROWSER.page.find_all("p", attrs={"class":"excerpt"})
    holiday_desc_array = [value.text for value in holiday_desc]

    for i, title in enumerate(holiday_title_array):
        print(title + ": " + holiday_desc_array[i])
    print(" ")

for month in MONTHS:
    for day in range(31):
        print(month + "," + str(day) + ": ")
        get_holidays_by_month("january", day)
