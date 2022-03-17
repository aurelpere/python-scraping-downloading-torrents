#!/usr/bin/python3
# coding: utf-8
from get_filesnames_from_torrent import get_files_names_from_torrent
import libtorrent as lt
import os


def test_get_files_names_from_torrent():
    # os.mkdir('test')
    fo = open('test.txt', 'w', encoding='utf-8')
    writelist = ['blabla'] * 10000
    for i in writelist:
        fo.write(i)
    fo.close()
    # print(dir(lt.create_torrent))

    print(dir(lt.file_entry))
    # print(dir(lt.operation_name))
    # print(dir(lt.file_storage))
    fs = lt.file_storage()
    size = os.path.getsize('test.txt')
    fs.add_file('test.txt', size)
    # fs.set_name('test.txt')
    print(dir(lt.torrent_info.name.__doc__))
    t = lt.create_torrent(fs)
    t.add_tracker('udp://tracker.openbittorrent.com:80/announce', 0)
    t.set_creator('libtorrent %s' % lt.version)
    t.set_comment('Test')
    t.set_priv(True)
    # print(t.torrent_info.name())
    # print(t.torrent_info.files())
    # print(lt.set_piece_hashes.__doc__)
    lt.set_piece_hashes(t, '.')
    # t.__setattr__('test/text.txt','test/text.txt')
    f = open('./mytorrent.torrent', 'wb')
    f.write(lt.bencode(t.generate()))
    f.close()
    # print (lt.torrent_info('mytorrent.torrent').name())
    # print(list(lt.torrent_info('dune-2021-truefrench-720p-web-x264-fck.torrent').files().path))
    result = get_files_names_from_torrent('mytorrent.torrent')
    assert 'test.txt' in result
    os.remove('test.txt')
    # os.rmdir('test')
    os.remove('mytorrent.torrent')


if __name__ == '__main__':
    test_get_files_names_from_torrent()
