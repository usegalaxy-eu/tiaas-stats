#!/usr/bin/env python
import pytz
import csv

from dateutil.parser import parse
from icalendar import Calendar, Event


def events():
    with open('tiaas.tsv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        header = next(spamreader)
        header = ['timestamp', 'email', 'title', 'overview', 'start', 'end',
                  'location', 'official', 'people', 'advert', 'blog', 'website', 'materials',
                  'identifier', 'name', 'urls']
        for row in spamreader:
            q = dict(zip(header, row))

            for x in ('start', 'end', 'timestamp'):
                q[x] = parse(q[x])
            yield q


def fix(date):
    w = pytz.utc.localize(date).date()
    return w


if __name__ == '__main__':
    cal = Calendar()
    cal.add('prodid', '-//TIaaS Calendar//mxm.dk//')
    cal.add('version', '2.0')

    for event in events():
        e = Event()
        e.add('summary', 'TIaaS Training: %s' % event['identifier'])
        e.add('dtstart', fix(event['start']))
        e.add('dtend', fix(event['end']))
        # e.add('dtstamp', fix(event['timestamp']))
        cal.add_component(e)


    with open('tiaas.ics', 'wb') as f:
        f.write(cal.to_ical())
