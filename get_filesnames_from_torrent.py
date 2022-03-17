import libtorrent as lt
import warnings


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
