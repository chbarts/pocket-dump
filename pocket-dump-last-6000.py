#!/usr/bin/env python3

import requests
import argparse
import json
import sys
import os

def get_data(key, token):
    off = 0
    res = []
    while off < 6000:
        r = requests.post('https://getpocket.com/v3/get',
                          json={'consumer_key': key, 'access_token': token,
                                'detailType': 'complete', 'offset': off})
        data = r.json()
        for elt in data['list']:
            off = off + 1
            if not elt['item_id'] in res:
                res[elt['item_id']] = elt
    return res

def dump_data(data):
    print(json.dumps({'list': data}))

parser = argparse.ArgumentParser(description="Get the last 6000 URLs saved to Pocket")

parser.add_argument('-k', '--consumer-key', metavar='CONSUMER_KEY', nargs=1,
                    type=str, help='Consumer key')
parser.add_argument('-t', '--access-token', metavar='ACCESS_TOKEN', nargs=1,
                    type=str, help='Access token')

args = parser.parse_args()

if (len(args.consumer_key) == 0) or (len(args.access_token) == 0):
    parser.print_help()
    sys.exit(0)

dump_data(get_data(args.consumer_key[0], args.access_token[0]))
