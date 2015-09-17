#!/usr/bin/python

"""
This script it meant to read in CSV files from an AllGuard security system
and do an analysis of what day of week individuals come in...

This can help with office space planning.

example input format:

"Gen Time","Seq ID","Type","Status","P","Reader","Site","Card Number","Account","Name","Operator","Message"
"6/1/2015 12:48:00 AM","4395401","Card","Valid Card","79","Lobby","Readers","50783","NCI","Cat, Garfield","Allguard",""
"6/1/2015 6:43:00 AM","4395781","Card","Valid Card","79","Hall","Readers","8131","NCI","Dog, Snoopy ","Allguard",""
"6/1/2015 6:46:00 AM","4395782","Card","Valid Card","79","Stairs","Readers","8131","NCI","Mouse, Jerry ","Allguard",""


example output  (lastname, firstname, mondays, tuesdays, ..., total)
Mouse, Jerry, 8, 10, 12, 11, 7, 0, 0, 48
Dog, Snoopy, 0, 1, 0, 0, 1, 0, 0, 2
Cat, Garfield, 2, 6, 2, 6, 1, 0, 0, 17

"""

import datetime
from dateutil import parser
from collections import Counter
import csv
import sys


# First pass -- unique users per date
date2user={}
f = open(sys.argv[1], 'rt')
try:
    reader = csv.DictReader(f)
    for row in reader:

        # Skip rows that aren't good card reads
        if 'Valid Card' not in row['Status']:
            continue

        # Create a user id name based on name and card number
        #userid="%s-%s" % (row['Name'].strip(), row['Card Number'])
        userid="%s" % (row['Name'].strip())

        if userid == '':
            userid = 'Unknown'

        # Parse the time string
        timeparsed = parser.parse(row['Gen Time'])

        # If we don't have this date yet
        if timeparsed.strftime("%x") not in date2user:
                # Create an entry using this date and this single user
                date2user[timeparsed.strftime("%x")]=[userid]
        # If we already have this date
        elif userid not in date2user[timeparsed.strftime("%x")]:
                # Add/append a user to this date
                date2user[timeparsed.strftime("%x")].append(userid)

# Stop reading the csv
finally:
    f.close()

# Second Pass - Store day of week counter for each user
user2dayofweek={}

for date in date2user:

    # Parse the date and get Day of Week
    dt = parser.parse(date)
    dayofweek = dt.strftime("%A")

    # Walk each user for a given date
    for userid in date2user[date]:
        # If we don't aleady have this user
        if userid not in user2dayofweek:
            cnt=Counter()
            cnt[dayofweek] += 1
            cnt['Total'] += 1
            # Create a new counter list
            user2dayofweek[userid] = cnt
        else:
            user2dayofweek[userid][dayofweek] += 1
            user2dayofweek[userid]['Total'] += 1

# Last pass, pretty print in collumns
for user in user2dayofweek:
    print "%s, %s, %s, %s, %s, %s, %s, %s, %s"  % (user,
        user2dayofweek[user]['Monday'] or 0,
        user2dayofweek[user]['Tuesday'] or 0,
        user2dayofweek[user]['Wednesday'] or 0,
        user2dayofweek[user]['Thursday'] or 0,
        user2dayofweek[user]['Friday'] or 0,
        user2dayofweek[user]['Saturday'] or 0,
        user2dayofweek[user]['Sunday'] or 0,
        user2dayofweek[user]['Total'] or 0,
)
