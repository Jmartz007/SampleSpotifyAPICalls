import json

from SpotifyMain import search

def format_artist_result(artist):
    result = search(artist)
    formattedResults = json.dumps(result, indent=4,separators=(",",": "))
    artistResults = result["artists"]["items"]
    listResults = []
    for i in artistResults:
       print(i["name"])
       listResults.append(i["name"])
    firstResult = listResults[0]
    return firstResult



if __name__=="__main__":
    result = format_artist_result("Linkin Park")
    print(result)
