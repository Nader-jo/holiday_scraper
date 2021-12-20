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

class Category():
    """Category"""
    name = ""
    def __init__(self, name_str, description_text):
        self.name = name_str
        self.description = description_text

    def print(self):
        """print"""
        print(self.name + "|" + self.description)

    def to_string(self):
        """to_string"""
        return self.name

class Holiday():
    """Holiday"""
    title = ""
    date = ""
    description = ""

    def __init__(self, title_str, date, description_text, category):
        self.title = title_str
        self.date = date
        self.description = description_text
        self.category = category

    def print(self):
        """print"""
        print(self.to_string())

    def to_string(self):
        """to_string"""
        string = self.date+"|"+self.title+"|"+self.description+"|"+self.category.to_string()
        return string

def get_holidays_by_month_and_day(month, day, categories_object_list, holidays_list):
    """get all holidays by month and day"""
    holiday_list = holidays_list.copy()
    if month.lower() in MONTHS:
        BROWSER.open(BASE_URL + "/" + month.lower() + "-" + str(day) + "-holidays")
    holiday_title = BROWSER.page.find_all("h3", attrs={"class":"holiday-title"})
    holiday_title_array = [value.text.strip() for value in holiday_title]
    holiday_desc = BROWSER.page.find_all("p", attrs={"class":"excerpt"})
    holiday_desc_array = [value.text.strip() for value in holiday_desc]
    categories_array, holidays_array = get_holiday_category(month)

    for i, title in enumerate(holiday_title_array):
        category = categories_array[holidays_array.index(title)]
        category_obj = next(cat for cat in categories_object_list if cat.name == category.strip())
        holiday_list.append(Holiday(title, month+" "+str(day), holiday_desc_array[i], category_obj))
    return holiday_list

def get_holiday_category(month_str):
    """get categories"""
    holiday_category_url = ""
    if month_str.lower() in MONTHS:
        holiday_category_url = BASE_URL + "/" + month_str.lower() + "-holidays"
    BROWSER.open(holiday_category_url)
    holidays = BROWSER.page.find_all("td", attrs={"class":"title"})
    holidays_array = [value.text.strip() for value in holidays]
    categories = BROWSER.page.find_all("td", attrs={"class":"category"})
    categories_array = [value.text.strip() for value in categories]
    return categories_array, holidays_array


def get_categories():
    """get all categories"""
    categories_list = []
    categories_url = BASE_URL + "/national-day-topics"
    BROWSER.open(categories_url)
    categories_title = BROWSER.page.find_all("h2", attrs={"class":"daycal-month-name"})
    categories_title_array = [value.text.strip() for value in categories_title]
    categories_desc = BROWSER.page.find_all("div", attrs={"class":"daycal-month-descr"})
    categories_desc_array = [value.text.strip() for value in categories_desc]
    for i, title in enumerate(categories_title_array):
        new_categories = Category(title, categories_desc_array[i])
        categories_list.append(new_categories)
    return categories_list

def get_holidays_by_category(holiday_list, categories_list, category_string):
    """get all holidays by category"""
    filtered_holiday_list = []
    category_obj = next(cat for cat in categories_list if cat.name == category_string.strip())
    for holiday_item in holiday_list:
        if holiday_item.category.name.lower().strip() == category_obj.name.lower().strip():
            filtered_holiday_list.append(holiday_item)
    return filtered_holiday_list

HOLIDAYS = []
CATEGORIES = get_categories()

for selected_month in ["january"]:
    for day_nbr in range(32):
        HOLIDAYS = get_holidays_by_month_and_day(selected_month, day_nbr, CATEGORIES, HOLIDAYS)

for holiday in HOLIDAYS:
    holiday.print()

print()
FILTERED_HOLIDAYS = get_holidays_by_category(HOLIDAYS, CATEGORIES, "Fun")

for holiday in FILTERED_HOLIDAYS:
    holiday.print()
