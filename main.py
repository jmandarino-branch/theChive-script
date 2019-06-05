import feedparser
import requests
import re

"""TheChive Automatic link creation

How does this work:

This script reads the data from https://thechive.com/feed/ and creates quick link on their dashboard for each post 

To do this we need to add type=2 and $marketing_title='asdfasfd' in order fo the links to appear on the dashboard

Examples before this script that was made by the og script that broke:
https://b.thechive.com/barrel-roll-562019
https://b.thechive.com/girl-goes-562019
https://b.thechive.com/clumsy-animals-562019
https://b.thechive.com/actors-who-562019

"""

BRANCH_API = 'https://api2.branch.io/v1/url'
FEED_URL = 'https://thechive.com/feed/'
THECHIVE_API_KEY = 'key_live_mmcvV3k1959IZ6WAJtc32kimqDbYcK6L'


def make_branch_link(app_key, d):
    url = BRANCH_API

    d['branch_key'] = app_key
    d['~channel'] = 'facebook'  # this is what was happening before -- keeping it consistent
    d['type'] = 2

    response = requests.post(url, json=d)

    print(response)


if __name__ == '__main__':

    d = feedparser.parse(FEED_URL)

    for x in d['entries']:
        d = dict()

        post_id = int(re.search('(?<=p=)\d+', x['id']).group(0)) # get the post id from the url (last group of nums)
        # branch tags
        d['$canonical_url'] = x['link']
        d['$marketing_title'] = x['title']
        #TODO: d['$alias'] = '-'.join(x['title'].lower().split(' ')[0:2]) + '-' + str(post_id)  # lord forgive me for my sins
        # branch fallback urls
        d['$canonical_url'] = x['link']
        d['$android_url'] = x['link']
        d['$ios_url'] = x['link']
        d['$desktop_url'] = x['link']
        # og tags
        d['$og_title'] = x['title']
        d['$og_app_id'] = '241047555179'
        d['$og_image_url'] = x['media_thumbnail'][0]['url']
        d['$og_type'] = 'article'
        # chive specific
        d['post_id'] = post_id
        #TODO: d['post_date'] = int(time.time())  #this use to be included
        make_branch_link(THECHIVE_API_KEY,  {'data': d})
