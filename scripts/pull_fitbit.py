#!/usr/bin/env python3

import datetime
import json
import os

import fitbit

import rewind7am

CONSUMER_KEY = '22CJPS'
CONSUMER_SECRET = '1ab0a13b222053bb4fe831b97206f0b8'

LOGDIR = os.getenv('LOGDIR')

def refresh(token):
    print("Refreshing token: ", token)
    with open('token.json', 'w') as f:
        f.write(json.dumps(token))

if __name__ == '__main__':
    access_token = None
    refresh_token = None

    with open('token.json', 'r') as f:
        data = json.loads(f.read())

    client = fitbit.Fitbit(CONSUMER_KEY, CONSUMER_SECRET,
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expires_at=data['expires_at'],
            refresh_cb=refresh)

    today = datetime.date.today()

    all_times = []

    for ii in range(0, 7):
        date = today - datetime.timedelta(days=ii)
        datef = date.strftime('%Y-%m-%d')
        steps = client.intraday_time_series('activities/steps',
                                            base_date=datef)
        data = steps['activities-steps-intraday']['dataset']


        for entry in data:
            t = entry['time'].split(':')
            dt = datetime.datetime(year=date.year,
                                   month=date.month,
                                   day=date.day,
                                   hour=int(t[0]),
                                   minute=int(t[1]),
                                   second=int(t[2]))
            all_times.append((dt, entry['value']))

    all_times = sorted(all_times, key=lambda x: x[0])
    steps = {}

    for t, v in all_times:
        tt = int(t.strftime('%s'))
        rt = rewind7am.rewindTime(tt)
        if rt not in steps:
            steps[rt] = []
        steps[rt].append((tt, v))

    for vals in steps.values():
        print(sum([v[1] for v in vals]))

    ii = 0
    for k, vv in steps.items():
        with open(os.path.join(LOGDIR, 'steps_{}.txt'.format(k)), 'w') as f:
            if ii == 0 and len(vv) < 1440:
                ii += 1
                continue
            for tt, v in vv:
                f.write('{} {}\n'.format(tt, v))
