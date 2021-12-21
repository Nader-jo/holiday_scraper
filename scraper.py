#!/usr/bin/env python
"""Scraper.py: this is a web scrapper."""

import mechanicalsoup

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
    category = ""
    tag = ""

    def __init__(self, title_str, date, description_text):
        self.title = title_str
        self.date = date
        self.description = description_text

    def add_category(self, category):
        """add_category"""
        self.category = category

    def add_tag(self, tag):
        """add_tag"""
        self.tag = tag

    def print(self):
        """print"""
        print(self.to_string())

    def to_string(self):
        """to_string"""
        month = self.date.split(" ")[0]
        month_date = month+"|"+self.date+"|"
        string = month_date+self.title+"|"+self.description+"|"+self.category+"|"+self.tag
        return string

def get_holidays_by_month_and_day(month, day, holidays_list):
    """get all holidays by month and day"""
    holiday_list = holidays_list.copy()
    if month.lower() in MONTHS:
        BROWSER.open(BASE_URL + "/" + month.lower() + "-" + str(day) + "-holidays")
    holiday_title = BROWSER.page.find_all("h3", attrs={"class":"holiday-title"})
    holiday_title_array = [value.text.strip() for value in holiday_title]
    holiday_desc = BROWSER.page.find_all("p", attrs={"class":"excerpt"})
    holiday_desc_array = [value.text.strip() for value in holiday_desc]
    categories_array, holidays_array, tags_array = get_holiday_category_and_tags(month)

    for i, title in enumerate(holiday_title_array):
        if title.strip() in holidays_array:
            category = categories_array[holidays_array.index(title)]
            tag = tags_array[holidays_array.index(title)]
        else:
            category = ""
            tag = ""
        holiday_list.append(
            Holiday(title, month+" "+str(day), holiday_desc_array[i])
            .add_category(category.strip())
            .add_tag(tag))
    return holiday_list

def get_holiday_category_and_tags(month_str):
    """get categories for holidays"""
    holiday_category_url = ""
    if month_str.lower() in MONTHS:
        holiday_category_url = BASE_URL + "/" + month_str.lower() + "-holidays"
    BROWSER.open(holiday_category_url)
    holidays = BROWSER.page.find_all("td", attrs={"class":"title"})
    holidays_array = [value.text.strip() for value in holidays]
    categories = BROWSER.page.find_all("td", attrs={"class":"category"})
    categories_array = [value.text.strip() for value in categories]
    tags = BROWSER.page.find_all("td", attrs={"class":"tags"})
    tags_array = [value.text.strip() for value in tags]
    return categories_array, holidays_array, tags_array

def get_holidays_by_category(holiday_list, categories_list, category_string):
    """get all holidays by category"""
    filtered_holiday_list = []
    category_obj = next(cat for cat in categories_list if cat.name == category_string.strip())
    for holiday_item in holiday_list:
        if holiday_item.category.name.lower().strip() == category_obj.name.lower().strip():
            filtered_holiday_list.append(holiday_item)
    return filtered_holiday_list

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

HOLIDAYS = []

for selected_month in MONTHS:
    for day_nbr in range(32):
        HOLIDAYS = get_holidays_by_month_and_day(selected_month, day_nbr, HOLIDAYS)
    for holiday in HOLIDAYS:
        holiday.print()
    HOLIDAYS = []
