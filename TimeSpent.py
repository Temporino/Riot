import requests
import json
import time

api_key = "RGAPI-35d6ee2c-3154-4c62-8071-c4139b4c058b"
beginIndex=0
gamesIds = []
totalTime = 0
gamesDuration = dict()
Summoner = "Sbwinner"
server = "euw1"

def executeGet(request):
    response = requests.get(request)
    
    #Rate limit
    while(response.status_code == 429):
        time.sleep(30)
        response = requests.get(request)
        
    if response.status_code == 200:
        return response, 1        
    else:
        print(response.status_code)
        return response, None

request = "https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + Summoner + "?api_key=" + api_key
response, responseStatus = executeGet(request)
if responseStatus is not None:
    accountId = json.loads(response.content.decode('utf-8'))["accountId"]
else:
    print("Account could not be retrieved. Error code : " + response.status_code)
    
#retreive max games
request = "https://" + server + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?beginIndex=" + str(100000000) + "&api_key=" + api_key
response, responseStatus = executeGet(request)
if responseStatus is not None:
    maxIndex = json.loads(response.content.decode('utf-8'))["startIndex"]
    for tempIndex in range (beginIndex, maxIndex, 100):
        request = "https://" + server + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?beginIndex=" + str(tempIndex) + "&api_key=" + api_key
        response, responseStatus = executeGet(request)
        if responseStatus is not None:
            games = json.loads(response.content.decode('utf-8'))["matches"]
            for game in games:
                gamesIds.append(game["gameId"])
        else:
            print("request could not be executed. Error code : " + response.status_code)
else:
    print("request could not be executed. Error code : " + response.status_code)

def executeGet(request):
    response = requests.get(request)
    
    #Rate limit
    while(response.status_code == 429):
        time.sleep(30)
        response = requests.get(request)
        
    if response.status_code == 200:
        return response, 1        
    else:
        return response, None

#retrieve game duration 
for game in gamesIds:
    request = "https://" + server + ".api.riotgames.com/lol/match/v4/matches/"+ str(game) + "?api_key=" + api_key
    response, responseStatus = executeGet(request)
    if responseStatus is not None:
        totalTime = totalTime + json.loads(response.content.decode('utf-8'))["gameDuration"]
        gamesDuration[game] = json.loads(response.content.decode('utf-8'))["gameDuration"]
    else:
        print("request could not be executed. Error code : " + str(response.status_code))
totalTime
