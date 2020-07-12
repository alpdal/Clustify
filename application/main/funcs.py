import base64, json, requests
from flask import current_app as app
from pandas.io.json import json_normalize

def get_playlists(auth_head):
    body = {
        "limit" : 50
    }
    url_playlist = "https://api.spotify.com/v1/me/playlists"
    list_pl =  requests.get(url_playlist, headers=auth_head, params=body)
    
    return json.loads(list_pl.text)

def pl_items(auth_head, playlist_id):
    body = {
        "limit" : 10,
        # get only necessary fields
        "fields" : "offset,next,total,limit,items(track(artists,name,id,popularity))"
    }
    url_playlist_items = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    pl_items =  requests.get(url_playlist_items, headers=auth_head, params=body)

    return json.loads(pl_items.text)

def get_next(auth_head, url):
    items_remained = requests.get(url, headers=auth_head)
    return json.loads(items_remained.text)

def get_pl_items(auth_head, id_list):
    all_items = []
    all_track_ids = []

    for id in id_list:
        response = pl_items(auth_head, id)

        for item in response["items"]:
            if item["track"] != None:
                all_items.append(item["track"])
                all_track_ids.append(item["track"]["id"])

        while response["next"] != None:
            response = get_next(auth_head, response["next"])

            for item in response["items"]:
                if item["track"] != None:
                    all_items.append(item["track"])
                    all_track_ids.append(item["track"]["id"])

    return all_items, all_track_ids

def audio_features(auth_head, id_list):
    track_ids = ",".join(id_list)
    body = {
        "ids" : track_ids
    }    
    url_audio_features = "https://api.spotify.com/v1/audio-features"
    audio_features =  requests.get(url_audio_features, headers=auth_head, params=body)    

    return json.loads(audio_features.text)

def get_audio_features(auth_head, id_list):
    id_chunks = [id_list[x:x+100] for x in range(0, len(id_list), 100)]
    all_features = []

    for chunk in id_chunks:
        feature_set = audio_features(auth_head, chunk)
        all_features += feature_set["audio_features"]

    return all_features

def make_df(pl_items, audio_features):
    normal_items = json_normalize(pl_items)
    normal_features = json_normalize(audio_features)
    tracks_merged = normal_items.set_index("id").join(normal_features.set_index("id"))
    tracks_merged["artists"] = tracks_merged["artists"].copy().apply(lambda x: x[0]["name"])

    return tracks_merged

def get_user_id(auth_head):
    url_current_profile = "https://api.spotify.com/v1/me"
    user_id =  requests.get(url_current_profile, headers=auth_head)
    
    return json.loads(user_id.text)

def create_playlist(auth_head, user_id, pl_name):
    url = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
    headers = {
        "Authorization" : auth_head["Authorization"],
        "Content-Type" : "application/json"
    }    
    response = requests.post(url, headers=headers, json={"name" : pl_name})
    pl_id = json.loads(response.text)["id"]

    return pl_id

def add_tracks(auth_head, track_uris, pl_id):
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(pl_id)
    headers = {
        "Authorization" : auth_head["Authorization"],
        "Content-Type" : "application/json"
    }
    uri_chunks = [track_uris[x:x+100] for x in range(0, len(track_uris), 100)]

    for chunk in uri_chunks:                
        data = {
            "uris" : chunk
        }
        requests.post(url, headers=headers, json=data)

def generate_cl_pls(auth_head, user_id, cl_list):
    for i in range(0, len(cl_list)):
        pl_name = "cluster{}".format(i+1)
        pl_id = create_playlist(auth_head, user_id, pl_name)
        add_tracks(auth_head, cl_list[i], pl_id)

