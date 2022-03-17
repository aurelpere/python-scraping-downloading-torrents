# scraping-downloading-torrents
a scraping script to download films best of features and a download script to get the torrents

##usage:

##install
to install all dependencies, type:
`make install`

##scraping
to scrape film listings to csv files, type:
`python3 scraping_bestof_films_allocine.py`
`python3 scraping_bestof_films_senscritique.py`

##downloading
to download torrents, type:

`python3 dl_torrent.py -k your keywords`
>download one torrent at a time

`python3 dl_torrents_from_csv.py -csv csvfile.csv -year year`
>download all torrents of films csv listings of year 

