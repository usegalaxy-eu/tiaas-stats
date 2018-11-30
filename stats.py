#!/usr/bin/env python
import argparse
import csv
import yaml

from influxdb import InfluxDBClient
from dateutil.parser import parse

secrets = yaml.load(open('secret.yml', 'r'))


def measure(metric, time, values, tags=None):
    m = {
        'measurement': metric,
        'time': time,
        'fields': values,
    }
    if tags:
        m['tags'] = tags
    return m


def events():
    with open('tiaas.tsv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        header = next(spamreader)
        header = ['timestamp', 'email', 'title', 'overview', 'start', 'end',
                  'location', 'official', 'people', 'advert', 'blog', 'website', 'materials',
                  'identifier', 'name', 'urls']
        for row in spamreader:
            q = dict(zip(header, row))
            # Split locations out and take first two chars.
            q['location'] = [x.strip()[0:2] for x in q['location'].split(',')]

            for x in ('start', 'end', 'timestamp'):
                q[x] = parse(q[x])
            yield q

def points(date):
    fmt_date = date + 'T03:00:00Z'
    pdate = parse(date)

    for event in events():
        s = event['start']
        e = event['end']

        # If not started, or already ended
        if pdate < s or pdate > e:
            continue

        tags = {
            'event': event['identifier'],
        }

        values = {
            'students': int(event['people']),
            'status': 1,
        }

        for location in event['location']:
            tags['location'] = location
            yield measure('tiaas', fmt_date, values, tags=tags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Translate Galaxy DB stats from PostgreSQL to InfluxDB")
    parser.add_argument('date', help="Day to calculate statistics for, yyyy-mm-dd format please.")
    args = parser.parse_args()

    client = InfluxDBClient(**secrets['influxdb'])
    client.write_points(points(args.date))
