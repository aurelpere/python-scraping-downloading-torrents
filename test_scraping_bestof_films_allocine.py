#!/usr/bin/python3
# coding: utf-8
import os
import pandas as pd
from scraping_bestof_films_allocine import get_film_names_allocine


def test_get_film_names_allocine():
    get_film_names_allocine('2020')
    file = './films_allocine_2020.csv'
    assert os.path.isfile(file) == True
    df = pd.read_csv(file, sep=';')
    assert list(df.columns) == [
        'year',
        'title',
        'original title',
        'author',
        'actors',
        'duration',
        'genre',
        'synopsis',
    ]
    assert len(df) == 101
    os.remove(file)
