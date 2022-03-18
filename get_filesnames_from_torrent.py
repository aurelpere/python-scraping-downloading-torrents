#!/usr/bin/python3
# coding: utf-8
"""
this is get_filesnames_from_torrent.py
"""
import warnings
import libtorrent as lt


def get_files_names_from_torrent(torrentfile):
    """return list of files in torrentfile\n"""
    info = lt.torrent_info(str(torrentfile))
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    path_list = [x.path for x in list(info.files())]
    return path_list


if __name__ == '__main__':
    a = get_files_names_from_torrent('mytorrent.torrent')
    print(a)
    # print('main')
