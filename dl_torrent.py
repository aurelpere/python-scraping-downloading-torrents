#!/usr/bin/python3
# coding: utf-8
"""
this is dl_torrent.py
"""
import datetime
import re
import json
import os
import time
import argparse
import requests


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 503, 502, 504),
        session=None,
):
    """tweaking de requests.session pour eviter les erreuer 503"""
    session = session or requests.Session()
    retry = requests.packages.urllib3.util.retry.Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_torrent(keywords, keywords2='', path='.'):
    """
    usage : get_torrent file.torrent -a "author"
    get torrent from sharewood tracker
    return str(Exception) if Errors
    or 'no torrent' if not foundaé&a    q
    or 'path/filename' if downloaded correctly
    or else '(request1.statuscode,request2.statuscode)'
    save file in path/filename
    save passkey inbv                  ._ file
    """
    with open('._', 'r', encoding='utf-8') as file_open:
        _ = str(file_open.read()).strip()

    # INITIALISATION
    print('-- Initialisation --')
    print('\n')
    start = datetime.datetime.now()

    # dl dictionnary
    api_result1 = api_dlinfo_call(keywords, _, keywords2)

    # dl torrent
    if 'https://www.sharewood.tv' in api_result1:
        api_result2 = api_dltorrent_call(api_result1, path, _)
        print(api_result2)
        end = datetime.datetime.now()
        time_elapsed = str(end - start)
        print('-- TIME ELAPSED --')
        print(time_elapsed)
        return api_result2
    print(api_result1)
    end = datetime.datetime.now()
    time_elapsed = str(end - start)
    print('-- TIME ELAPSED --')
    print(time_elapsed)
    return api_result1


def api_dlinfo_call(keywords, _, keywords2=''):
    "download infos from sharewood api"
    try:
        session = requests.session()
        base_url = f'https://www.sharewood.tv/api/{_}/search?name={keywords}'
        print(base_url)
        print('\n')
        request1 = requests_retry_session(session=session).get(
            url=base_url)  # ,headers=header)
        #session.close()?
        print(f'API request status code: {request1.status_code}')
        print('\n')
        if request1.status_code == 200:
            datalist = json.loads(request1.text)
            if not datalist:
                if keywords2 == '':
                    print("no torrent")
                    print('\n')
                    return "no torrent"
                base_url = f'https://www.sharewood.tv/api/{_}/search?name={keywords2}'
                print(base_url)
                print('\n')
                request1_keyword2 = requests_retry_session(session=session).get(
                    url=base_url)
                print(f'API request status code: {request1_keyword2.status_code}')
                print('\n')
                if request1_keyword2.status_code == 200:
                    datalist = json.loads(request1_keyword2.text)
                    request1_keyword2.close()
                    if len(datalist) == 0:
                        print("no torrent")
                        print('\n')
                        return "no torrent"
            filter_size_list = []
            for dict_i in datalist:
                if (dict_i['size'] >= 700000000
                        and dict_i['size'] <= 10000000000):
                    filter_size_list.append(dict_i)
            if len(filter_size_list) == 0:
                print('pas de torrent entre 700Mo et 10Go')
                print('\n')
                return 'pas de torrent entre 700Mo et 10Go'
            filter_seed_list = []
            for dict_k in filter_size_list:
                filter_seed_list.append(dict_k['seeders'])
            torrent_index = filter_seed_list.index(max(filter_seed_list))
            dict_torrent = filter_size_list[torrent_index]
            print(dict_torrent)
            print('\n')
            print(
                f"torrent url: https://www.sharewood.tv/api/{_}/{dict_torrent['id']}/download"
            )
            print(f"torrent slug: {dict_torrent['slug']}")
            print('\n')
            return f"https://www.sharewood.tv/api/{_}/{dict_torrent['id']}/download"
    except (Exception, ) as error1:
        print(f'erreur de telechargement {error1}')
        print('\n')
        return str(error1)


def api_dltorrent_call(torrent_url, path, _):
    "download torrent from sharewood api"
    try:
        session = requests.session()
        request2 = requests_retry_session(session=session).get(
            torrent_url, allow_redirects=True)
        print(f'download status code: {request2.status_code}')
        if request2.status_code == 200:
            fname = re.findall('filename=(.+)',
                               request2.headers['content-disposition'])[0]
            if path != '.':
                if not os.path.isdir(path):
                    os.mkdir(path)
            with open(f'{path}/{fname}', 'wb') as out_file:
                out_file.write(request2.content)
            request2.close()
            print(f'{path}/{fname} téléchargé')
            print('\n')
            time.sleep(3)
            return f'{path}/{fname}'
        request2.close()

    except (Exception, ) as error2:
        request2.close()
        print(f'erreur de telechargement {error2}')
        print('\n')
        time.sleep(3)
        return str(error2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='python dl_torrents.py -k your keywords')
    parser.add_argument(
        '-k',
        '--keywords',
        nargs='+',
        required=True,
        metavar='keywords',
        type=str,
        help='keywords to search for .torrent file to download')
    args = vars(parser.parse_args())
    get_torrent(' '.join(args['keywords']))
