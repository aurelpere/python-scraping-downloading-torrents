"""
this is scraping_bestof_films_allocine.py
"""
#!/usr/bin/python3
# coding: utf-8

import datetime
import re
import html
import time
import requests
import bs4
import pandas as pd


def souptitle(soup):
    """find titles in soup object"""
    souptitlelist = soup.find_all(attrs={'class': 'meta-title-link'})
    result = []
    for k in souptitlelist:
        titles = re.findall('(?<=">)(.+)(?=<)', html.unescape(str(k)))
        result.append(str(titles[0]))
    print(result)
    print('\n')
    return result


def soupduration(soup, decennie, annee, page_nb):
    """find authors in soup object"""
    soupdurationlist = soup.find_all(
        attrs={'class': 'meta-body-item meta-body-info'})
    soupdurationtxt = ''
    for k in soupdurationlist:
        soupdurationtxt = html.unescape(str(k))
    durations = re.findall('(.+)(?=min)', soupdurationtxt)
    if page_nb == 6 and str(int(decennie) + annee) == '2000':
        durations.insert(4, '-')
    return durations


def soupgenre(soup):
    """find genres in soup object"""
    soupgenrelist = soup.find_all(
        attrs={'class': 'meta-body-item meta-body-info'})
    result = []
    for k in soupgenrelist:
        genres = re.findall('(?<===">)(.+?)(?=<)', html.unescape(str(k)))
        genres = ', '.join(genres)
        result.append(genres)
    return result


def soupauthor(soup):
    """find authors in soup object"""
    soupauthorlist = soup.find_all(
        attrs={'class': 'meta-body-item meta-body-direction'})
    result = []
    for k in soupauthorlist:
        authors = re.findall('(?<=">)(.+?)(?=</a)', html.unescape(str(k)))
        authors = ', '.join(authors)
        result.append(authors)
    return result


def soupactors(soup, decennie, annee, page_nb):
    """find actors in soup object"""
    soupactorlist = soup.find_all(
        attrs={'class': 'meta-body-item meta-body-actor'})
    result = []
    for k in soupactorlist:
        actors = re.findall('(?<=">)(.+?)(?=</a)', html.unescape(str(k)))
        actors = ', '.join(actors)
        result.append(actors)
    if page_nb == 5 and str(int(decennie) + annee) == '2009':
        result.insert(6, '-')
    if page_nb == 1 and str(int(decennie) + annee) == '2013':
        result.insert(8, '-')
    if page_nb == 2 and str(int(decennie) + annee) == '2013':
        result.insert(0, '-')
    if page_nb == 2 and str(int(decennie) + annee) == '2015':
        result.insert(3, '-')
    if page_nb == 3 and str(int(decennie) + annee) == '2017':
        result.insert(1, '-')
    return result


def soupdescription(soup):
    """find descriptions in soup object"""
    soupdescriptionlist = soup.find_all('div', {'class': 'content-txt'})
    result = []
    for k in soupdescriptionlist:
        desc = str(k.text).replace('\n', ' ')
        result.append(desc)
    return result


def get_film_names_allocine(decennie):
    """
    get film names from best of in allocine.com
    decennie is a string ('1990','2010', etc.)
    """

    # INITIALISATION
    print('-- Initialisation --')
    start = datetime.datetime.now()
    years_list = []
    titles_list = []
    durations_list = []
    genres_list = []
    authors_list = []
    actors_list = []
    descriptions_list = []
    annee = 0
    seuil_page = 7
    if str(decennie) == '2020':
        seuil_annee = 2
    else:
        seuil_annee = 10
    while annee < seuil_annee:
        page_nb = 1
        url_to_get = (
            f'https://www.allocine.fr/film/meilleurs/presse/decennie-{decennie}/annee-{int(decennie) + annee}/?page={page_nb}'
        )
        if annee == 1 and str(decennie) == '2020':
            seuil_page = 6
        while page_nb < seuil_page:
            print(f'Page: {page_nb}')
            print(url_to_get)

            # CRAWLING ET PARSEING
            req = requests.session()
            response = req.get(url=url_to_get)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.text, features='html.parser')
                # title
                titles = souptitle(soup)
                titles_list.extend(titles)

                # duration
                durations_list.extend(
                    soupduration(soup, decennie, annee, page_nb))

                # genre
                genres_list.extend(soupgenre(soup))

                # author
                authors_list.extend(soupauthor(soup))

                # actors
                actors_list.extend(soupactors(soup, decennie, annee, page_nb))

                # description
                descriptions_list.extend(soupdescription(soup))

                # years
                years_list.extend([str(int(decennie) + annee)] * len(titles))

                page_nb += 1
                url_to_get = (
                    f'https://www.allocine.fr/film/meilleurs/presse/decennie-{decennie}/annee-{int(decennie) + annee}/?page={page_nb}'
                )
            else:
                print(
                    f'probleme pour scraper la page {page_nb} : status code {response.status_code}'
                )
                time.sleep(10)
        original_list = [''] * len(years_list)
        df0 = pd.DataFrame(
            data={
                'year': years_list,
                'title': titles_list,
                'original title': original_list,
                'author': authors_list,
                'actors': actors_list,
                'duration': durations_list,
                'genre': genres_list,
                'synopsis': descriptions_list,
            })
        annee += 1
    # TEMPS PASSE
    df0.to_csv(f'films_allocine_{decennie}.csv',
               header=True,
               sep=';',
               index=False)
    end = datetime.datetime.now()
    time_elapsed = str(end - start)
    print(f'listing téléchargé dans films_allocine_{decennie}.csv')
    print('\n')
    print('-- TIME ELAPSED --')
    print(time_elapsed)
    return 1


if __name__ == '__main__':
    get_film_names_allocine('2000')
    get_film_names_allocine('2010')
    get_film_names_allocine('2020')
