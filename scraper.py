#!/usr/bin/env python
import mechanicalsoup
import pandas as pd
import sqlite3

"""Scraper.py: this is a web scrapper."""

__author__      = "Nader Jemaa"
__copyright__   = "Copyright 2021, Tunisia"

baseUrl = "https://nationaltoday.com"
months = ["january","february","march","april","may","june","july","august","september","october","november","december"]

browser = mechanicalsoup.StatefulBrowser()

def get_holidays_by_month(month, day):
    final_url = ""
    if month.lower() in months:
        final_url = baseUrl + "/" + month.lower() + "-" + str(day) + "-holidays"
    browser.open(final_url)
    holiday_title = browser.page.find_all("h3", attrs = {"class":"holiday-title"})
    holiday_title_array = [value.text for value in holiday_title]
    holiday_desc = browser.page.find_all("p", attrs = {"class":"excerpt"})
    holiday_desc_array = [value.text for value in holiday_desc]

    for i in range(len(holiday_title_array)):
        print(holiday_title_array[i] + ": " + holiday_desc_array[i])
    print(" ")
    

for month in months:
    for day in range(31):
        print(month + "," + str(day) + ": ")
        get_holidays_by_month("january", day)


