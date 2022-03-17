#!/usr/bin/python3
# coding: utf-8
import requests
import os
from dl_torrent import requests_retry_session
from dl_torrent import get_torrent


def test_requests_retry_session():
    s = requests.session()
    assert 'total=0' in str(s.adapters['http://'].max_retries)
    assert 'connect=None' in str(s.adapters['http://'].max_retries)
    assert 'read=False' in str(s.adapters['http://'].max_retries)
    s2 = requests_retry_session(session=s)
    assert 'total=3' in str(s2.adapters['http://'].max_retries)
    assert 'connect=3' in str(s2.adapters['http://'].max_retries)
    assert 'read=3' in str(s2.adapters['http://'].max_retries)


def test_get_torrent():
    get_torrent('dune')
    file = './dune-2021-truefrench-720p-web-x264-fck.torrent'
    assert os.path.isfile(file) == True
    os.remove('dune-2021-truefrench-720p-web-x264-fck.torrent')


if __name__ == '__main__':
    test_requests_retry_session()
    test_get_torrent()
