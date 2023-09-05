from ics import Event, Calendar
import datetime
import requests
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import credentials


def main():
    try:
        google_cal = scrape_shifts()
        add_to_google_calendar(google_cal, credentials.calendar)
        print('Your shifts for the month have been added to your Google Calendar!')

    except Exception as error:
        print('Error: ', error)


def scrape_shifts():
    login_url = ('https://v2can.schedulesource.com/teamwork/logon/chkLogon.aspx')
    secure_url = ('https://v2can.schedulesource.com/teamwork/Employee/sch/schedule.aspx?view=month&layout=list')
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
        'portal': credentials.portal,
        'code': credentials.code,
        'user': credentials.username,
        'pswd': credentials.password
    }
    
    with requests.session() as s:
        try:
            s.post(login_url, headers = headers, data = payload)
            r = s.get(secure_url)
            soup = BeautifulSoup(r.content, 'lxml')

        except:
            print('Error: Please try again')

    soup = BeautifulSoup(r.text, 'lxml')
    shifts_scraped = soup.findAll('tr', id=lambda x: x and x.startswith('sftList_ctl'))

    # Parse shift data into a list of dictionaries formatted for the Google Calendar API and create ICS file containing those shifts
    google_cal = parse_shifts(shifts_scraped)
    return google_cal


def parse_shifts(shifts_scraped):
    # Create a calendar
    cal = Calendar()
    # Initialize empty list for google calendar API
    cal_list = []
    
    for tag in shifts_scraped:
        data = [td.get_text(strip=True) for td in tag.find_all('td')]

        # Formatting data into ICS format
        if len(data) >= 7:
            date = data[0]
            start_time = data[5]
            end_time = data[6]

            start_datetime_str = date + ' ' + start_time
            end_datetime_str = date + ' ' + end_time
            start_datetime = datetime.datetime.strptime(start_datetime_str, '%m/%d/%Y %I:%M%p')
            end_datetime = datetime.datetime.strptime(end_datetime_str, '%m/%d/%Y %I:%M%p')

            e = Event()
            e.name = "Work Shift"
            e.begin = start_datetime
            e.end = end_datetime
            e.description = "Shift from {} to {}".format(start_time, end_time)

            cal.events.add(e)

            # Add to list formatted for Google Calendar API
            cal_list.append({
                'summary': 'Work Shift',
                'description': f"Shift from {start_time} to {end_time}",
                'start': {
                    'dateTime': f'{start_datetime.isoformat()}-08:00',
                    'timeZone': 'America/Vancouver',
                },
                'end': {
                    'dateTime': f'{end_datetime.isoformat()}-08:00',
                    'timeZone': 'America/Vancouver',
                },
            })

    # Write the calendar to an .ics file
    with open('shifts.ics', 'w') as f:
        f.writelines(cal)
    return cal_list


def add_to_google_calendar(google_cal, cal_id):  
    client_secrets = 'credentials.json'
    scopes = ['https://www.googleapis.com/auth/calendar']

    # Initializing Google Calendar API service
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets, scopes)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)

    for event in google_cal:

        try:
                service.events().insert(calendarId=cal_id, body=event).execute()
        
        except Exception as error:
            print(f'Error: ', error)


if __name__ == '__main__':
    main()