#!/usr/bin/python3
# coding: utf-8

import pandas as pd
from dl_torrent import get_torrent
from get_filesnames_from_torrent import get_files_names_from_torrent


def get_torrents_from_csv(csv, year):
    """
    get torrents from csv
    """
    df = pd.read_csv(csv, sep=';')
    df = df.astype(str)
    df0 = df[df['year'] == year]
    df['dl_output'] = ''
    df['files'] = ''
    for i in df0.index:  # à améliorer
        if df.loc[i, 'original title'] != '':
            df.loc[i, 'dl_output'] = get_torrent(
                df.loc[i, 'title'], df.loc[i, 'original title'], path=str(year)
            )
            if '/' in df.loc[i, 'dl_output']:
                df.loc[i, 'files'] = str(
                    get_files_names_from_torrent(df.loc[i, 'dl_output'])
                )
        else:
            df.loc[i, 'dl_output'] = get_torrent(
                df.loc[i, 'title'], path=str(year)
            )
            if '/' in df.loc[i, 'dl_output']:
                df.loc[i, 'files'] = str(
                    get_files_names_from_torrent(df.loc[i, 'dl_output'])
                )
    df.to_csv(csv, sep=';', header=True, index=False)
    dfpct = df[df['year'] == year]
    pourcentage = len(
        [x for x in dfpct['dl_output'].values if '/' in x]
    ) / len(dfpct['dl_output'])
    print('pourcentage de torrent téléchargés: {} %'.format(pourcentage * 100))


if __name__ == '__main__':
    get_torrents_from_csv('films_senscritique.csv', '2010')
