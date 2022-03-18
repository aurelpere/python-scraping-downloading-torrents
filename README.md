[![Test-Lint-Format](https://github.com/aurelpere/python-scraping-downloading-torrents/actions/workflows/blank.yml/badge.svg)](https://github.com/aurelpere/python-scraping-downloading-torrents/actions/workflows/blank.yml) ![test-coverage badge](./coverage-badge.svg) [![Maintainability](https://api.codeclimate.com/v1/badges/e502e3b52b4f990dd355/maintainability)](https://codeclimate.com/github/aurelpere/python-scraping-downloading-torrents/maintainability)


# scraping-downloading-torrents
a scraping script to download films best of features and a download script to get the torrents


## install
to install all dependencies, type:
`make install`

## scraping
to scrape film listings to csv files, type:

`python3 scraping_bestof_films_allocine.py`
>download films best of infos from allocine.com in csv files in ./films_allocine_2000.csv
>./films_allocine_2010.csv and ./films_allocine_2020.csv

`python3 scraping_bestof_films_senscritique.py`
>download film best of infos from senscritique.com in ./films_senscritique.csv

## downloading
to download torrents, type:

`python3 dl_torrent.py -k your keywords`
>download one torrent at a time in ./

`python3 dl_torrents_from_csv.py -csv csvfile.csv -year year`
>download all .torrent files of films csv listings of year in ./year

you should replace the passkey with your passkey from sharewood in ._ file
