#!/usr/bin/python3
# coding: utf-8
import os
import pandas as pd
from scraping_bestof_films_senscritique import get_film_names_sc


def test_get_film_names_sc():
    get_film_names_sc()
    file = './films_senscritique.csv'
    assert os.path.isfile(file) == True
    df = pd.read_csv(file, sep=';')
    assert list(df.columns) == [
        'year',
        'title',
        'original title',
        'author',
        'actors',
    ]
    assert len(df) == 1575
    os.remove(file)
