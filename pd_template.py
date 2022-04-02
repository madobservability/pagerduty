#!/usr/bin/env python
# dave@madobservability.com
import os
from pdpyras import APISession
import csv

api_key = os.environ['PD_API_KEY'] # Must set OS variable of PD_API_Key
session = APISession(api_key, default_from="EMAIL ADDRESS HERE")

x = input('Events, Incidents, Services, Users?  ').capitalize()

def main():
    if x == 'Services':
        services()
    elif x == 'Users':
        users()
    elif x == 'Incidents':
        incidents()
    elif x == 'Event':
        event_rules()
    print("Export.csv has been created in working directory")

def write_rows(column1, column2, column3):
    with open('export.csv', mode='a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([column1, column2, column3])

def users():
    for user in session.iter_all('users'):
            write_rows(user['name'], user['email'], user['role'])
            print(user['name'],user['email'],user['role'])
            

def services():
    for service in session.iter_all('services'):
        write_rows(service['name'], service['last_incident_timestamp'],service['summary'])
        print(service['name'],'Last Incident:',service['last_incident_timestamp'])

def incidents():
    for incident in session.list_all('incidents', params={'statuses[]': 'acknowledged'}):
        write_rows(incident['summary'],incident['status'],incident['html_url'])
        print(incident['summary'],incident['status'],incident['html_url'])

def event_rules():
    for event in session.iter_all('rulesets'):
        print(event['name'],event['type'],event['routing_keys'])
main()
