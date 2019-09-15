# -*- coding: utf-8 -*-
import os
import collections
import shutil
import config
import re
import sys
import csv
import time
import numpy as np
import pandas as pd
from sklearn.cluster import Birch, SpectralClustering, AffinityPropagation, AgglomerativeClustering, KMeans, DBSCAN, OPTICS

CONFIG = config.Config

def do_clustering(target_dataset, cluster_method):
	df_data = pd.read_csv(os.path.join(CONFIG.CSV_PATH, 'normalized_' + target_dataset + '.csv'), index_col=0, header=None, encoding='utf-8-sig')
	df_data.index.name = 'short_code'
	print(df_data.iloc[:100])

	df_pca_data = pd.read_csv(os.path.join(CONFIG.CSV_PATH, 'pca_' + target_dataset + '.csv'), index_col=0, header=0, encoding='utf-8-sig')
	df_pca_data.index.name = 'short_code'
	print(df_pca_data.iloc[:100])

	tsne_pca = pd.read_csv(os.path.join(CONFIG.CSV_PATH, 'tsne_' + target_dataset + '.csv'), index_col=0, header=0, encoding='utf-8-sig')
	tsne_pca = tsne_pca.iloc[1:]
	tsne_pca.index.name = 'short_code'
	print(tsne_pca.iloc[:100])

	start_time = time.time()
	if cluster_method == 0:
		clustering = DBSCAN(eps=0.3, min_samples=20).fit(tsne_pca)
		csv_name = 'clustered_dbscan_' + target_dataset + '.csv'
	elif cluster_method == 1:
		clustering = OPTICS(min_samples=20).fit(tsne_pca)
		csv_name = 'clustered_optics_' + target_dataset + '.csv'
	elif cluster_method == 2:
		clustering = SpectralClustering(n_clusters=21, random_state=42).fit(df_pca_data)
		csv_name = 'clustered_spectral_' + target_dataset + '.csv'
	elif cluster_method == 3:
		clustering = AgglomerativeClustering(n_clusters=21).fit(df_pca_data)
		csv_name = 'clustered_agglomerative_' + target_dataset + '.csv'
	else:
		clustering = Birch(n_clusters=21).fit(df_data)
		csv_name = 'clustered_birch_' + target_dataset + '.csv'
	print("time elapsed: " + str(time.time()-start_time))
	print(clustering.get_params())
	print(clustering.labels_)
	count_percentage(clustering.labels_)
	cluster_list = np.array(clustering.labels_).tolist()
	tsne_pca['cluster'] = clustering.labels_
	tsne_pca.to_csv(os.path.join(CONFIG.CSV_PATH, csv_name), encoding='utf-8-sig')

def count_percentage(cluster_labels):
	count = collections.Counter(cluster_labels)
	for k in count:
		print("cluster {} : {:.2%}".format(str(k), count[k]/len(cluster_labels)))


def run(option): 
	if option == 0:
		do_clustering(target_dataset=sys.argv[2], cluster_method=int(sys.argv[3]))
	else:
		print("This option does not exist!\n")


if __name__ == '__main__':
	run(int(sys.argv[1]))