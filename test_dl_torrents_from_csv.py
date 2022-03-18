#!/usr/bin/python3
# coding: utf-8
from dl_torrents_from_csv import get_torrents_from_csv
import pandas as pd
import os


def test_get_torrents_from_csv():
    year = '2010'
    title = 'The Ghost Writer'
    original_title = ''
    author = 'Roman Polanski'
    actors = 'Ewan McGregor, Pierce Brosnan, Kim Cattrall'
    df = pd.DataFrame(
        {
            'year': year,
            'title': title,
            'original title': original_title,
            'author': author,
            'actors': actors,
        },
        index=[0],
    )  ###
    df.to_csv('csvfile.csv', sep=';', header=True, index=False)
    get_torrents_from_csv('csvfile.csv', year)
    assert (os.path.isfile(
        '{}/the-ghost-writer-2010-multi-bluray-1080p-x264-ac3-re-at-2.torrent'.
        format(year)) == True)  ###
    os.remove('csvfile.csv')
    os.remove(
        '{}/the-ghost-writer-2010-multi-bluray-1080p-x264-ac3-re-at-2.torrent'.
        format(year))


if __name__ == '__main__':
    test_get_torrents_from_csv()
