# ScheduleSource Shift Scraper

A python web scraper using the BeautifulSoup4 library to scrape shift data from ScheduleSource. It then parses the data and imports the shifts into a google calendar invoking the Google Calendar API. Furthermore, it creates an ics file containing the shifts if you wanted to import the shifts into other calendars, e.g. Outlook, Apple Calendar, etc.