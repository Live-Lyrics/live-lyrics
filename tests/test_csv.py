import csv

import pytest

from utils.lyrics_url import amalgama_url, vk_normalize


def get_vk():
    with open("test.csv") as f:
        records = csv.DictReader(f)
        l = [(row['vk_artist'], row['artist']) for row in records]
        l.extend([(row['vk_title'], row['title']) for row in records])
    return l


@pytest.mark.parametrize("vk_artist, artist", get_vk())
def test_vk(vk_artist, artist):
    assert vk_normalize(vk_artist) == artist


def get_amalgama():
    with open("test.csv") as f:
        records = csv.DictReader(f)
        l = [(row['artist'], row['title'], row['amalgama']) for row in records]
    return l


@pytest.mark.parametrize("artist, title, amalgama", get_amalgama())
def test_amalgama(artist, title, amalgama):
    assert amalgama_url(artist, title) == amalgama
