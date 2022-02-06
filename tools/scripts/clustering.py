import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pokedex.models import Resource, Endpoint
from tools.models import Cluster

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MaxAbsScaler

def get_cluster_label(l):
    if np.mean(l)>100:
        return "Legends"
    elif np.mean(l)<60:
        return "Babies"
    elif np.argmax(l)==5:
        return "Glass-Cannons"
    elif np.argmax(l)==3:
        return "Spec-Fighters"
    elif np.argmax(l)==1:
        return "Phy-Fighters"
    elif np.argmax(l)==2:
        return "Tankers"

def run(*args):
    endpoint = Endpoint.objects.get(name='pokemon')
    stats_raw = {
        'hp' : [],
        'attack' : [],
        'defense' : [],
        'sp_attack' : [],
        'sp_defense' : [],
        'speed' : [],
    }
    ids = []
    for resource in Resource.objects.filter(endpoint=endpoint).order_by('index'):
        for key in stats_raw.keys():
            stats_raw[key].append(resource.data[key])
        ids.append(resource.name)
    
    stats_dataframe = pd.DataFrame(stats_raw,index=ids)
    stats_array = stats_dataframe.to_numpy()
    scaler = MaxAbsScaler().fit(stats_array)
    stats_scaled = scaler.transform(stats_array)
    # print(stats_scaled)

    avg_stats = []
    cluster_sizes = []
    clusters = []
    
    K = 6
    kmeans = KMeans(K)
    kmeans.fit(stats_scaled)
    for i in range(K):
        clusters.append([])
        avg_stats.append(np.zeros(6))
        cluster_sizes.append(0)
    for index,label in enumerate(kmeans.labels_):
        clusters[label].append(ids[index])
        avg_stats[label] += stats_array[index]
        cluster_sizes[label]+=1
    for i in range(K):
        avg_stats[i] /= cluster_sizes[i]
    for i in range(K):
        cluster, created = Cluster.objects.get_or_create(name=get_cluster_label(avg_stats[i]))
        cluster.size = cluster_sizes[i]
        cluster.elements = clusters[i]
        cluster.save()
    
    # df = pd.DataFrame(avg_stats, index=[get_cluster_label(avg_stats[i],cluster_sizes[i]) for i in range(K)])
    # df.columns = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    # df.plot.bar(rot=0)
    # plt.ylim(0,180)
    # plt.savefig('cluster_averages.png')