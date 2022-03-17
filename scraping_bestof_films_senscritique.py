#!/usr/bin/python3
# coding: utf-8

import requests
import bs4
import datetime
import re
import pandas as pd
import html

dico_sc = {
    '2022': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2022/3167299',
    '2O21': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2021/2917616',
    '2020': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2020/2582670',
    '2019': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2019/2301802',
    '2018': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2018/1757790',
    '2017': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2017/1522840',
    '2016': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2016/1152822',
    '2015': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2015/703337',
    '2014': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2014/367137',
    '2013': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2013/173207',
    '2012': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2012/165123',
    '2011': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2011/748438',
    '2010': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2010/748463',
    '2009': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2009/748526',
    '2008': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2008/748538',
    '2007': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2007/748547',
    '2006': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2006/748549',
    '2005': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2005/748645',
    '2004': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2004/748655',
    '2003': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2003/748659',
    '2002': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2002/748666',
    '2001': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2001/748669',
    '2000': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_2000/748673',
    '1999': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1999/748712',
    '1998': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1998/748714',
    '1997': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1997/748720',
    '1996': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1996/748728',
    '1995': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1995/748732',
    '1994': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1994/748739',
    '1993': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1993/748746',
    '1992': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1992/748749',
    '1991': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1991/748753',
    '1990': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_de_1990/748756',
    'annees_2010': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_des_annees_2010/558512',
    'annees_80': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_des_annees_1980/558507',
    'annees_70': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_des_annees_1970/558503',
    'annees_60': 'https://www.senscritique.com/top/resultats/les_meilleurs_films_des_annees_1960/558502',
}


def get_film_names_sc():
    """
    get film names from best of in senscritique.com
    """

    # INITIALISATION
    print('-- Initialisation --')
    start = datetime.datetime.now()
    title_list = []
    authors_list = []
    actors_list = []
    years_list = []
    original_list = []
    for i in dico_sc:
        url_to_get = dico_sc[i]
        print(url_to_get)
        pattern_title = '(?<=">)(.+?)(?=</p)'
        pattern_author = '(?<=">)(.+?)(?=</a)'
        pattern_actors = '(?<=avec)(.+)'

        r = requests.session()
        response = r.get(url=url_to_get)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, features='html.parser')
            souplist_title = soup.find_all(
                True, {'class': ['elco-anchor', 'elco-original-title']}
            )
            souptxt_title = ''

            # title
            for k in souplist_title:
                souptxt_title += html.unescape(str(k))
            souptxt_title = souptxt_title.replace(
                '</a><a', '</p'
            )  # print(souptxt_author)
            souptxt_title = souptxt_title.replace(
                '</a><p', ''
            )  # print(souptxt_author)
            souptxt_title = souptxt_title.replace(
                '</a>', '</p'
            )  # print(souptxt_author)
            title = re.findall(pattern_title, souptxt_title)
            originals = []
            for k in range(len(title)):
                title[k] = title[k].replace(
                    'class="elco-original-title">', '--'
                )
                if '--' in title[k]:
                    originals.append(re.findall('(?<=--).+', title[k])[0])
                    pattern_to_remove = re.findall('--.+', title[k])[0]
                    title[k] = title[k].replace(pattern_to_remove, '')
                    title[k] = title[k].strip()
                else:
                    originals.append('')
            title_list.extend(title)
            print('films récupérés :\n{}'.format(str(title)))
            print('\n')
            original_list.extend(originals)

            # authors
            souplist_author = soup.find_all(attrs={'class': 'elco-baseline'})
            souptxt_author = ''
            for k in souplist_author:
                souptxt_author += html.unescape(str(k))
            souptxt_author = souptxt_author.replace('</a> et <a', '-')
            souptxt_author = souptxt_author.replace('</a>,', '-')
            authors = re.findall(pattern_author, souptxt_author)
            for k in range(len(authors)):
                authors[k] = re.sub(
                    '(?<=class=)(.+?)(?=">)', '-', authors[k], count=10
                )
                authors[k] = authors[k].replace('<a class=', '')
                authors[k] = authors[k].replace('">', '')
                authors[k] = authors[k].replace('class=', '')
            authors_list.extend(authors)

            # actors
            actors = re.findall(pattern_actors, souptxt_author)
            if i == '1992':
                actors.insert(29, '-')
            actors_list.extend(actors)

            years = [i] * len(actors)
            years_list.extend(years)

    df = pd.DataFrame(
        data={
            'year': years_list,
            'title': title_list,
            'original title': original_list,
            'author': authors_list,
            'actors': actors_list,
        }
    )
    df.to_csv('films_senscritique.csv', sep=';', header=True, index=False)
    # TEMPS PASSE
    end = datetime.datetime.now()
    time_elapsed = str(end - start)
    print('\n')
    print('listing téléchargé dans ./films_senscritique.csv')
    print('\n')
    print('-- TIME ELAPSED --')
    print(time_elapsed)
    return 1


if __name__ == '__main__':
    get_film_names_sc()
