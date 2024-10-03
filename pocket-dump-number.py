#!/usr/bin/env python3

from datetime import datetime
import requests
import argparse
import json
import sys
import os


def get_data(key, token, number):
    off = 0
    res = {}
    while off < number:
        r = requests.post('https://getpocket.com/v3/get',
                          json={'consumer_key': key, 'access_token': token,
                                'detailType': 'complete', 'offset': off})
        data = r.json()
        if not ('list' in data):
            return res
        lst = data['list']
        for k in lst:
            elt = lst[k]
            off = off + 1
            if not elt['item_id'] in res:
                res[elt['item_id']] = elt
    return res


def get_data_since(key, token, date):
    off = 0
    res = {}
    stamp = parse_timestamp(date)
    while off < number:
        r = requests.post('https://getpocket.com/v3/get',
                          json={'consumer_key': key, 'access_token': token,
                                'detailType': 'complete', 'offset': off, 'since': stamp})
        data = r.json()
        if not ('list' in data):
            return res
        lst = data['list']
        for k in lst:
            elt = lst[k]
            off = off + 1
            if not elt['item_id'] in res:
                res[elt['item_id']] = elt
    return res


def dump_data(data):
    print(json.dumps({'list': data}))


def parse_timestamp(stamp):
    return int(datetime.fromisoformat(stamp).timestamp())

parser = argparse.ArgumentParser(description="Get the last specified number of (default 5000) URLs saved to Pocket")

parser.add_argument('-k', '--consumer-key', metavar='CONSUMER_KEY', nargs=1,
                    type=str, help='Consumer key')
parser.add_argument('-t', '--access-token', metavar='ACCESS_TOKEN', nargs=1,
                    type=str, help='Access token')
parser.add_argument('-n', '--number', metavar='NUMBER', default=5000,
                    type=int, help='Number of saves to retrieve, rounded up to next multiple of 30')
parser.add_argument('-d', '--date', metavar='ISO_DATE', type=str,
                    help='Retrieve URLs since date time, in ISO format (like 2024-10-03T10:15:30-06:00)')

args = parser.parse_args()

if (args.consumer_key is None) or (args.access_token is None) or (len(args.consumer_key) == 0)  or (len(args.access_token) == 0):
    parser.print_help()
    sys.exit(0)

if (not (args.number is None)) and (not (args.date is None)):
    print("Can't specify maximum number of results and results since datetime", file=sys.stderr)
    parser.print_help()
    sys.exit(1)

if not (args.date is None):
    dump_data(get_data_since(args.consumer_key[0], args.access_token[0], args.date[0]))
else:
    dump_data(get_data(args.consumer_key[0], args.access_token[0], args.number))
