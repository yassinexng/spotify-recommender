import os,requests,json, time
from dotenv import load_dotenv
import pandas as pd



def space():
    for i in range(0,4):
        print("\n")

space()


load_dotenv()



class Genre_handling:
    def __init__(self,artist_name):
        self.artist_name = artist_name
        self.link = "https://ws.audioscrobbler.com/2.0/"
        self.lastfmtoken = os.getenv("API_LASTFM")
        self.params = {
        "method": "artist.getTopTags",
    "artist": artist_name,
    "api_key": self.lastfmtoken,
    "format": "json"
        }
    def get_genre(self):
        time.sleep(1)
        response = requests.get(
        self.link,
         params=self.params
         )
        response.raise_for_status()    
        data = response.json()
        tags = []
        v = data["toptags"]
        for i in range(len(v["tag"])):
            c = v["tag"][i]["name"]
            if c not in tags:
                tags.append(c)
        return tags





class Spotify_Reader:
    def __init__(self,time):
        self.token = os.getenv("TOKEN")
        self.headers = {
    "Authorization" : f"Bearer {self.token}",
    }
        self.time = time
        
    def send_request(self):
        link = f"https://api.spotify.com/v1/me/top/tracks?time_range={self.time}&limit=50"
        response = requests.get(link,headers=self.headers) 
        response.raise_for_status()
        return response
    def get_size(self):
        return len(self.send_request().json()["items"])
    def handle_features(self,id):
        base_url = f"https://api.reccobeats.com/v1/audio-features?ids={id}"
        ourrequest = requests.get(base_url)
        return ourrequest.json()
    def initiate_extracted_info(self):
        extracted_info = [{
    "album_name": None,
    "genre(s)": [],
    "artist(s)": [],
    "Song": None,
    "song_code" : None,
    "acousticness" : 0.0,
    "danceability" : 0.0,
    "energy" : 0.0,
    "instrumentalness" : 0.0,
    "key" : 0,
    "liveness" : 0.0,
    "loudness" : 0.0,
    "mode" : 0,
    "speechiness" : 0.0,
    "tempo" : 0.0,
    "valence" : 0.0,
    } for _ in range(1, self.get_size() + 1)]
        return extracted_info
    def handle_extracted_info(self):
        request = self.send_request()
        data = request.json()
        extracted_info = self.initiate_extracted_info()
        songs = []
        
        check = {}
        i = 0
        j = 0
        for v in data["items"]:
            j += 1
            album = v["album"]
            album_name = album["name"]
            song_name = v["name"]
            extracted_info[i]["song_code"] = v["id"]
            features_request = self.handle_features(extracted_info[i]["song_code"] )
            time.sleep(1)
            if len(features_request["content"])  > 0:
                
                val = features_request["content"][0]
                extracted_info[i]["acousticness"] = val["acousticness"]
                extracted_info[i]["danceability"] = val["danceability"]
                extracted_info[i]["energy"] = val["energy"]
                extracted_info[i]["instrumentalness"] = val["instrumentalness"]
                extracted_info[i]["key"] = val["key"]
                extracted_info[i]["liveness"] = val["liveness"]
                extracted_info[i]["loudness"] = val["loudness"]
                extracted_info[i]["mode"] = val["mode"]
                extracted_info[i]["speechiness"] = val["speechiness"]
                extracted_info[i]["tempo"] = val["tempo"]
                extracted_info[i]["valence"] = val["valence"]
 


            if album_name not in check:
                check[album_name] = i
                extracted_info[i]["album_name"] = album_name
                extracted_info[i]["Song"] = song_name
        

                for l in album["artists"]:
                    extracted_info[i]["artist(s)"].append(l["name"])
                    
                    
                    
                genre_handler = Genre_handling(l["name"])
                tags = genre_handler.get_genre()
                extracted_info[i]["genre(s)"].extend(tags)
                songs.append(f"{song_name} -- {', '.join(extracted_info[i]['artist(s)'])} ")   

                
                time.sleep(2)

                i += 1
            else:
                k = check[album_name]
                extracted_info[k]["Song"] = song_name
        
        extracted_info = [e for e in extracted_info if e["album_name"] is not None]
        return extracted_info, songs,data




def test():
    extracted_info_one, songs_one,data_one = Spotify_Reader("short_term").handle_extracted_info()

    print("The dictionary, as a data:")
    print(json.dumps(extracted_info_one, indent=2, ensure_ascii=False))
    space()
    print("The top songs in the short term: ")
    for i in range(len(songs_one)):
        print(f"Song No{i+1}:  {songs_one[i]} . - Spotify URI: {extracted_info_one[i]["song_code"]}") 
       
        
    space()
    extracted_info_two, songs_two, data_two= Spotify_Reader("long_term").handle_extracted_info()
    space()

    print("The dictionary, as a data:")
    print(json.dumps(extracted_info_two, indent=2, ensure_ascii=False))
    space()
    print("The top songs in the long term: ")
    for i in range(len(songs_two)):
        print(f"Song No{i+1}:  {songs_two[i]}  .- Spotify URI: {extracted_info_two[i]["song_code"]} ")
      
    space()


    df_one = pd.DataFrame(extracted_info_one)
    df_two = pd.DataFrame(extracted_info_two)

    df_one.to_csv('output_short_i.csv', index=False)
    df_two.to_csv('output_long_ii.csv', index=False)
    return df_one, df_two, data_one








