#!/usr/bin/python3
# coding: utf-8
"""
this is dl_torrents_from_csv.py
"""
import argparse
import pandas as pd
from dl_torrent import get_torrent
from get_filesnames_from_torrent import get_files_names_from_torrent


def get_torrents_from_csv(csv, year):
    """
    get torrents from csv
    """
    df0 = pd.read_csv(csv, sep=';')
    df0 = df0.astype(str)
    df1 = df0[df0['year'] == year]
    df0['dl_output'] = ''
    df0['files'] = ''
    for i in df1.index:  # à améliorer
        if df0.loc[i, 'original title'] != '':
            df0.loc[i, 'dl_output'] = get_torrent(df0.loc[i, 'title'],
                                                  df0.loc[i, 'original title'],
                                                  path=str(year))
            if '.torrent' in df0.loc[i, 'dl_output']:
                df0.loc[i, 'files'] = str(
                    get_files_names_from_torrent(df0.loc[i, 'dl_output']))
        else:
            df0.loc[i, 'dl_output'] = get_torrent(df0.loc[i, 'title'],
                                                  path=str(year))
            if '.torrent' in df0.loc[i, 'dl_output']:
                df0.loc[i, 'files'] = str(
                    get_files_names_from_torrent(df0.loc[i, 'dl_output']))
    df0.to_csv(csv, sep=';', header=True, index=False)
    dfpct = df0[df0['year'] == year]
    pourcentage = len([x for x in dfpct['dl_output'].values if '/' in x
                       ]) / len(dfpct['dl_output'])
    print(f'pourcentage de torrent téléchargés: {pourcentage * 100} %')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='python dl_torrents_from_csv.py csvfile year')
    parser.add_argument(
        '-csv',
        '--csv',
        required=True,
        metavar='csvfile.csv',
        type=str,
        help='csvfile to process from to download the .torrent files')
    parser.add_argument(
        '-year',
        '--year',
        required=True,
        metavar='year',
        type=str,
        help='year to process from to download the .torrent files')
    args = vars(parser.parse_args())
    get_torrents_from_csv(args['csv'], args['year'])
