# ScheduleSource Shift Scraper

## Overview

This Python-based tool scrapes work shift data from ScheduleSource using BeautifulSoup4 and automatically populates the events into Google Calendar. It also generates an ICS file, making it easy to import your shifts into other calendar applications like Outlook or Apple Calendar.

## Features

- Scrapes shift data from ScheduleSource.
- Parses and formats the shift data for Google Calendar.
- Generates an ICS file for import into other calendar services.
- Handles authentication with Google Calendar API.

## Prerequisites

- Python 3.x
- BeautifulSoup4 library
- Google API client libraries for Python
- Valid ScheduleSource credentials

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/mloweng/web-scraper

   ```

2. Install required Python libraries:
   pip install -r requirements.txt

## Setup

1. Fill in your ScheduleSource credentials in the 'credentials.py' file
2. Obtain your 'credentials.json' file from the Google Developer Console for Google Calendar API and place it in the project directory

## Usage

Run the scraper with:
python3 main.py

Your shifts for the next month will be added to your specified Google Calendar and an ICS file will be created in the project directory.

## Contact

matthew.j.ng@gmail.com
