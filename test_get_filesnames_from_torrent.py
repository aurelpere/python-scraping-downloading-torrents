#!/usr/bin/python3
# coding: utf-8
from get_filesnames_from_torrent import get_files_names_from_torrent
import libtorrent as lt
import os


def test_get_files_names_from_torrent():
    fo = open('test.txt', 'w', encoding='utf-8')
    writelist = ['blabla'] * 10000
    for i in writelist:
        fo.write(i)
    fo.close()
    fs = lt.file_storage()
    size = os.path.getsize('test.txt')
    fs.add_file('test.txt', size)
    t = lt.create_torrent(fs)
    t.add_tracker('udp://tracker.openbittorrent.com:80/announce', 0)
    t.set_creator('libtorrent %s' % lt.version)
    t.set_comment('Test')
    t.set_priv(True)
    lt.set_piece_hashes(t, '.')
    f = open('./mytorrent.torrent', 'wb')
    f.write(lt.bencode(t.generate()))
    f.close()
    result = get_files_names_from_torrent('mytorrent.torrent')
    assert 'test.txt' in result
    os.remove('test.txt')
    os.remove('mytorrent.torrent')


if __name__ == '__main__':
    test_get_files_names_from_torrent()
