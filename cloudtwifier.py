#!/bin/python3
#https://github.com/andrea-varesio/CloudTwifier

'''Given a geographical region or hashtag, create a word cloud of the most frequently used terms'''

import argparse
import datetime
import json
import os
import pathlib
import re
import shutil
import sys

import requests
import wordcloud

from auth import BEARER_TOKEN

now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def show_license():
    '''Show License'''

    print('\n**************************************************')
    print('"CloudTwifier": Generate word clouds based on Twitter content')
    print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/CloudTwifier')
    print('**************************************************\n\n')

def parse_arguments():
    '''Parse arguments'''

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-q', '--query', help='Search by specified query', type=str)
    #arg_parser.add_argument('-c', '--country', help='Search by specified country', type=str)
    #arg_parser.add_argument('-t', '--timeframe', help='Days', type=int)
    arg_parser.add_argument('-r', '--retweets', help='Include retweets', action='store_true')
    arg_parser.add_argument('-o', '--output', help='Specify output directory', type=str)
    arg_parser.add_argument('--quiet', help='Disable verbosity', action='store_true')

    return arg_parser.parse_args()

def get_output_filepath():
    '''Get output filepath from argument or use $HOME if output is not provided'''

    args = parse_arguments()

    if not args.output:
        output_dir = os.path.join(pathlib.Path.home(), f'CloudTwifier_{args.query}_{now}')
    elif os.path.isdir(args.output):
        output_dir = os.path.join(args.output, f'CloudTwifier_{args.query}_{now}')
    else:
        print('Invalid output path')
        sys.exit(1)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    return os.path.join(output_dir, f'CloudTwifier_{now}')

def get_timeframe():
    '''Get timeframe from arguments or fallback to default. Currently disabled'''

    args = parse_arguments()

    if args.timeframe:
        days = args.timeframe
    else:
        days = 365

    return (now - datetime.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')

def build_query():
    '''Build query from arguments'''

    args = parse_arguments()

    if args.retweets:
        retweets_query = 'is:retweet'
    else:
        retweets_query = '-is:retweet'

    if not args.query:
        print('Query required')
        sys.exit(1)
    if '#' not in args.query:
        user_query = f'#{args.query}'
    else:
        user_query = args.query

    return {'query': f'{user_query} {retweets_query}',
            'tweet.fields': 'text',
    }

def bearer_oauth(req):
    '''Method required by bearer token authentication'''

    req.headers['Authorization'] = f'Bearer {BEARER_TOKEN}'
    req.headers['User-Agent'] = 'v2FullArchiveSearchPython'
    return req

def connect_to_endpoint(url, params):
    '''Connect to Twitter endpoint'''

    response = requests.request('GET', url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()

def get_tweets():
    '''Get raw tweets, remove query, urls and non-ascii chars and return a clean str'''

    search_url = 'https://api.twitter.com/2/tweets/search/recent'
    search_query = build_query()

    json_response = connect_to_endpoint(search_url, search_query)

    with open(f'{get_output_filepath()}_tweets.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_response, indent=4, sort_keys=True))

    i = -1
    tweets = ''
    for _ in json_response['data']:
        i += 1
        tweets += json_response['data'][i]['text']
    tweets = re.sub(r'http\S+', '', tweets).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    tweets = tweets.replace(parse_arguments().query, '')

    return str(tweets)

def generate_cloud(tweets):
    '''Generate a word cloud and save it to a file'''

    filepath = get_output_filepath()

    cloud = wordcloud.WordCloud(background_color='white', width=800, height=600)
    cloud.generate(tweets).to_file(f'{filepath}_cloud.png')

def main():
    '''Main function'''

    args = parse_arguments()

    if not BEARER_TOKEN:
        print('Missing API token')
        sys.exit(1)

    if not args.quiet:
        show_license()

    generate_cloud(get_tweets())

    if not args.quiet:
        print('Files saved in the following location:')
        print(os.path.dirname(get_output_filepath()))

    if os.path.isdir('__pycache__'):
        shutil.rmtree('__pycache__')

if __name__ == '__main__':
    main()
    del BEARER_TOKEN
