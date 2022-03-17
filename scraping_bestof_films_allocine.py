#!/usr/bin/python3
# coding: utf-8

import requests
import bs4
import datetime
import re
import pandas as pd
import html
import time


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
    base_url = (
        'https://www.allocine.fr/film/meilleurs/presse/decennie-{}/'.format(
            str(decennie)
        )
    )
    annee = 0
    seuil_page = 7
    if str(decennie) == '2020':
        seuil_annee = 2

    else:
        seuil_annee = 10
    while annee < seuil_annee:
        page_nb = 1
        url_to_get = (
            base_url
            + 'annee-{}/'.format(str(int(decennie) + annee))
            + '?page={}'.format(page_nb)
        )
        if annee == 1 and str(decennie) == '2020':
            seuil_page = 6
        while page_nb < seuil_page:
            print('Page: {}'.format(page_nb))
            print(url_to_get)

            pattern = '(?<=">)(.+)(?=<)'
            pattern_actors = '(?<=">)(.+?)(?=</a)'
            # CRAWLING ET PARSEING
            r = requests.session()
            response = r.get(url=url_to_get)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.text, features='html.parser')
                # title
                souptitle = soup.find_all(attrs={'class': 'meta-title-link'})
                templist00 = []
                for k in souptitle:
                    titles = re.findall(pattern, html.unescape(str(k)))
                    templist00.append(str(titles[0]))
                print(templist00)
                print('\n')
                titles_list.extend(templist00)

                # duration
                soupduration = soup.find_all(
                    attrs={'class': 'meta-body-item meta-body-info'}
                )
                soupdurationtxt = ''
                for k in soupduration:
                    soupdurationtxt += html.unescape(str(k))
                durations = re.findall('(.+)(?=min)', soupdurationtxt)
                if page_nb == 6 and str(int(decennie) + annee) == '2000':
                    durations.insert(4, '-')
                durations_list.extend(durations)

                # genre
                soupgenre = soup.find_all(
                    attrs={'class': 'meta-body-item meta-body-info'}
                )
                templist0 = []
                for k in soupgenre:
                    genres = re.findall(
                        '(?<===">)(.+?)(?=<)', html.unescape(str(k))
                    )
                    genres = ', '.join(genres)
                    templist0.append(genres)
                genres_list.extend(templist0)

                # author
                soupauthor = soup.find_all(
                    attrs={'class': 'meta-body-item meta-body-direction'}
                )
                templist1 = []
                for k in soupauthor:
                    authors = re.findall(pattern_actors, html.unescape(str(k)))
                    authors = ', '.join(authors)
                    templist1.append(authors)
                authors_list.extend(templist1)

                # actors
                soupactor = soup.find_all(
                    attrs={'class': 'meta-body-item meta-body-actor'}
                )
                templist2 = []
                for k in soupactor:
                    actors = re.findall(pattern_actors, html.unescape(str(k)))
                    actors = ', '.join(actors)
                    templist2.append(actors)
                if page_nb == 5 and str(int(decennie) + annee) == '2009':
                    templist2.insert(6, '-')
                if page_nb == 1 and str(int(decennie) + annee) == '2013':
                    templist2.insert(8, '-')
                if page_nb == 2 and str(int(decennie) + annee) == '2013':
                    templist2.insert(0, '-')
                if page_nb == 2 and str(int(decennie) + annee) == '2015':
                    templist2.insert(3, '-')
                if page_nb == 3 and str(int(decennie) + annee) == '2017':
                    templist2.insert(1, '-')
                actors_list.extend(templist2)

                # description
                soupdescription = soup.find_all(
                    'div', {'class': 'content-txt'}
                )
                templist3 = []
                for k in soupdescription:
                    desc = str(k.text).replace('\n', ' ')
                    templist3.append(desc)
                descriptions_list.extend(templist3)

                # years
                years = [str(int(decennie) + annee)] * len(templist00)
                years_list.extend(years)

                page_nb += 1
                url_to_get = (
                    base_url
                    + 'annee-{}/'.format(str(int(decennie) + annee))
                    + '?page={}'.format(page_nb)
                )
            else:
                print(
                    'probleme pour scraper la page {} : status code {}'.format(
                        page_nb, response.status_code
                    )
                )
                time.sleep(10)
        original_list = [''] * len(years_list)
        df = pd.DataFrame(
            data={
                'year': years_list,
                'title': titles_list,
                'original title': original_list,
                'author': authors_list,
                'actors': actors_list,
                'duration': durations_list,
                'genre': genres_list,
                'synopsis': descriptions_list,
            }
        )
        annee += 1
    # TEMPS PASSE
    df.to_csv(
        'films_allocine_{}.csv'.format(str(decennie)),
        header=True,
        sep=';',
        index=False,
    )
    end = datetime.datetime.now()
    time_elapsed = str(end - start)
    print(
        'listing téléchargé dans films_allocine_{}.csv'.format(str(decennie))
    )
    print('\n')
    print('-- TIME ELAPSED --')
    print(time_elapsed)
    return 1


if __name__ == '__main__':
    get_film_names_allocine('2000')
    get_film_names_allocine('2010')
    get_film_names_allocine('2020')
