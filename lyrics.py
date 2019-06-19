import requests
from bs4 import BeautifulSoup

TOKEN = 'pjFgK42iwmjReYuLhCjjVj8HldIjQfXIe99aqPKjmKHNSWIzoy6qBWKxpYLw4_ny'
url = "http://api.genius.com"

#using api
headers = {'Authorization':'Bearer '+TOKEN}

song_title = "All Too Well"
artist_name = "Taylor Swift"

def lyrics_from_song_api_path(song_api_path):
    song_url = url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics

if __name__ == "__main__":
    search = url + "/search"
    params = {'q':song_title}
    response = requests.get(search,params=params,headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            print(song_info)
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        print(lyrics_from_song_api_path(song_api_path))