#!/usr/bin/python3
# coding: utf-8
import requests
import datetime
import re
import json
import os
import time
import argparse


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


def get_torrent(keywords, keywords2='', path='.', file='._'):
    """
    usage : get_torrent file.torrent -a "author"
    get torrent from sharewood tracker
    return str(Exception) if Errors
    or 'no torrent' if not found
    or 'path/filename' if downloaded correctly
    or else '(r1.statuscode,r2.statuscode)'
    save file in path/filename
    save passkey in ._ file
    """
    fo = open(file, 'r', encoding='utf-8')
    _ = str(fo.read()).strip()

    # INITIALISATION
    print('-- Initialisation --')
    print('\n')
    start = datetime.datetime.now()
    session = requests.session()

    # dl dictionnary
    try:
        base_url = 'https://www.sharewood.tv/api/{}/search?name={}'.format(
            _, keywords
        )
        print(base_url)
        print('\n')
        r1 = requests_retry_session(session=session).get(
            url=base_url
        )  # ,headers=header)
        print('API request status code: {}'.format(str(r1.status_code)))
        print('\n')
        if r1.status_code == 200:
            dataList = json.loads(r1.text)
            if len(dataList) == 0:
                if keywords2 == '':
                    print('no torrent')
                    print('\n')
                    time.sleep(3)
                    return 'no torrent'
                else:
                    time.sleep(3)
                    base_url = 'https://www.sharewood.tv/api/{}/search?name={}'.format(
                        _, keywords2
                    )
                    print(base_url)
                    print('\n')
                    r1 = requests_retry_session(session=session).get(
                        url=base_url
                    )  # ,headers=header)
                    print(
                        'API request status code: {}'.format(
                            str(r1.status_code)
                        )
                    )
                    print('\n')
                    if r1.status_code == 200:
                        dataList = json.loads(r1.text)
                        if len(dataList) == 0:
                            print('no torrent')
                            print('\n')
                            time.sleep(3)
                            return 'no torrent'
            filter_size_list = []
            for dict_i in dataList:
                if (
                    dict_i['size'] >= 700000000
                    and dict_i['size'] <= 10000000000
                ):
                    filter_size_list.append(dict_i)
            if len(filter_size_list) == 0:
                print('pas de torrent entre 700Mo et 10Go')
                print('\n')
                time.sleep(3)
                return 'pas de torrent entre 700Mo et 10Go'
            else:
                filter_seed_list = []
                for dict_k in filter_size_list:
                    filter_seed_list.append(dict_k['seeders'])
                torrent_index = filter_seed_list.index(max(filter_seed_list))
                dict_torrent = filter_size_list[torrent_index]

            print(dict_torrent)
            print('\n')
            torrent_slug = dict_torrent['slug']
            torrent_id = str(dict_torrent['id'])
            torrent_url = 'https://www.sharewood.tv/api/{}/{}/download'.format(
                _, torrent_id
            )
            print('torrent url: {}'.format(torrent_url))
            print('torrent slug: {}'.format(torrent_slug))
            print('\n')
    except (Exception,) as e1:
        print('erreur de telechargement {}'.format(str(e1)))
        print('\n')
        time.sleep(3)
        return str(e1)

    # dl torrent
    try:
        r2 = requests_retry_session(session=session).get(
            torrent_url, allow_redirects=True
        )  # headers=header)
        print('download status code: {}'.format(str(r2.status_code)))
        if r2.status_code == 200:
            name = r2.headers['content-disposition']
            fname = re.findall('filename=(.+)', name)[0]
            if path != '.':
                if not os.path.isdir(path):
                    os.mkdir(path)
            with open('{}/{}'.format(path, fname), 'wb') as out_file:
                out_file.write(r2.content)
            print('{}/{} téléchargé'.format(path, fname))
            print('\n')
            time.sleep(3)
            return '{}/{}'.format(path, fname)

    except (Exception,) as e2:
        print('erreur de telechargement {}'.format(str(e2)))
        print('\n')
        time.sleep(3)
        return str(e2)
    end = datetime.datetime.now()
    time_elapsed = str(end - start)
    print('-- TIME ELAPSED --')
    print(time_elapsed)
    print(str((r1.status_code, r2)))
    time.sleep(3)
    return str((r1.status_code, r2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python dl_torrents_from_csv.py csvfile year')
    parser.add_argument('-k','--keywords',nargs='+',required=True, metavar='keywords', type=str,
                        help='keywords to search for .torrent file to download')
    args = vars(parser.parse_args())
    get_torrent(' '.join(args['keywords']))

