import pytest
from unittest.mock import Mock, patch

import requests

from FormatResults import format_artist_result
from SpotifyMain import search

mockData = {'artists': {'href': 'https://api.spotify.com/v1/search?query=Lindsey+Stirling&type=artist&offset=0&limit=3', 'items': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/378dH6EszOLFShpRzAQkVM'}, 'followers': {'href': None, 'total': 2175577}, 'genres': ['bow pop', 'pop violin'], 'href': 'https://api.spotify.com/v1/artists/378dH6EszOLFShpRzAQkVM', 'id': '378dH6EszOLFShpRzAQkVM', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb8a0579f5bf1a376e019e6457', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab676161000051748a0579f5bf1a376e019e6457', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f1788a0579f5bf1a376e019e6457', 'width': 160}], 'name': 'Lindsey Stirling', 'popularity': 64, 'type': 'artist', 'uri': 'spotify:artist:378dH6EszOLFShpRzAQkVM'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/20VIE9Okvl7RfmuCsVlwxb'}, 'followers': {'href': None, 'total': 59286}, 'genres': ['bow pop', 'pop violin'], 'href': 'https://api.spotify.com/v1/artists/20VIE9Okvl7RfmuCsVlwxb', 'id': '20VIE9Okvl7RfmuCsVlwxb', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b27336535da03cd8bb08d73d229f', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e0236535da03cd8bb08d73d229f', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d0000485136535da03cd8bb08d73d229f', 'width': 64}], 'name': 'Escala', 'popularity': 34, 'type': 'artist', 'uri': 'spotify:artist:20VIE9Okvl7RfmuCsVlwxb'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/5VpyTzLuWMbReOGdB9bjiK'}, 'followers': {'href': None, 'total': 1434}, 'genres': ['pop violin'], 'href': 'https://api.spotify.com/v1/artists/5VpyTzLuWMbReOGdB9bjiK', 'id': '5VpyTzLuWMbReOGdB9bjiK', 'images': [], 'name': 'William Joseph & Lindsey Stirling', 'popularity': 22, 'type': 'artist', 'uri': 'spotify:artist:5VpyTzLuWMbReOGdB9bjiK'}], 'limit': 3, 'next': 'https://api.spotify.com/v1/search?query=Lindsey+Stirling&type=artist&offset=3&limit=3', 'offset': 0, 'previous': None, 'total': 246}}

@patch('FormatResults.search')
def test_format_artist_result(mock_get):
    mock_get.return_value = mockData
    firstResult = format_artist_result("Taylor Swift")
    assert firstResult == "Lindsey Stirling" 


@patch('SpotifyMain.get_token')
def test_search_no_token(mock_get):
    mock_get.return_value = None
    with pytest.raises(AttributeError):
        response = search("Taylor Swift")

@patch('SpotifyMain.get_token')
def test_search_invalid_token(mock_get):
    mock_get.return_value = "39127830183080x"
    response = search("Taylor Swift")
    response == 401


@patch('SpotifyMain.get_token')
def test_search_valid_token(mock_get):
    mock_get.return_value = ''
    response = search("Taylor Swift")
    assert type(response) == dict