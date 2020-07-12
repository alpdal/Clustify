import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_pl(df):
    # transform id from index to column
    df.reset_index(level=0, inplace=True)

    # transform and standardize data
    audio_features = df.iloc[:, 4:15] # 3-14 
    audio_features=audio_features.drop(columns=['loudness', "acousticness"])
    audio_features['key'] = audio_features['key'].astype('category')
    audio_features['mode'] = audio_features['mode'].astype('category')
    audio_features = pd.get_dummies(audio_features, columns = ["mode", "key"], drop_first=True).copy()

    num_features = audio_features.iloc[:, 0:8]
    names = num_features.columns
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(num_features)
    scaled_df = pd.DataFrame(scaled_df, columns=names)

    std_features = pd.concat([scaled_df, audio_features.iloc[:, 8:], df["name"], df["uri"]], axis=1).drop_duplicates()
    std_features.reset_index(inplace=True, drop=True)

    # define k with silhoutte 
    sil = []
    kmax = 10
    max_score = -1
    final_k = 0

    for k in range(2, kmax+1):
        kmeans = KMeans(n_clusters = k).fit(std_features.iloc[:, :-2])
        labels = kmeans.labels_
        score = silhouette_score(std_features.iloc[:, :-2], labels, metric = 'euclidean') * (1.01 ** k)
        # incentive coefficient 1.01 is added to increase the number of clusters 
        sil.append(score)
        if score > max_score:
            max_score = score
            final_k = k

    # if all list is needed
    # pd.concat([std_features, pd.DataFrame(labels, columns=["label"])], axis=1)

    km_model = KMeans(n_clusters = final_k).fit(std_features.iloc[:, :-2])
    labels = km_model.labels_
    
    clustered_list = pd.concat([std_features[["uri", "name"]], pd.DataFrame(labels, columns=["label"])], axis=1)

    label_set = list(set(labels))
    clustered_uris = []
    track_names=[]

    for l in label_set:
        cl = clustered_list[clustered_list["label"] == l]["uri"]
        names = clustered_list[clustered_list["label"] == l]["name"]

        lst = cl.tolist()
        name_lst = names.tolist()

        clustered_uris.append(lst)
        track_names.append(name_lst)
    
    return clustered_uris, track_names

