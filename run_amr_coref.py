# adaptation of https://github.com/bjascob/amr_coref.git 40_Run_Inference.py

# uncomment this block if using Google Colab
# !pip install penman
# !git clone https://github.com/bjascob/amr_coref.git
# import tensorflow as tf
# tf.test.gpu_device_name()

import torch
import os
import penman
from penman.models.noop import NoOpModel
from penman.graph import Graph
import amr_coref
from   amr_coref.amr_coref.coref.inference import Inference

# possible input files from AMR 3.0 corpus
proxy = "amr-clusters.txt"

def cluster():
    # open one of the files above twice
    fn = open(proxy, encoding='utf-8')
    gn = open(proxy, encoding='utf-8')

    # Cluster the graphs in amr_clusters with format: [[cluster],[cluster],...]
    gid_graphs = penman.load(fn,model=NoOpModel())
    current_gr_id = 0
    amr_clusters = []
    for graph in gid_graphs:
        gr_id = graph.metadata['cluster_id']
        if gr_id != current_gr_id:
            amr_clusters.append([])
            amr_clusters[int(gr_id)-1].append(graph)
            current_gr_id = gr_id
        else:
            amr_clusters[int(gr_id) - 1].append(graph)
    return amr_clusters

#     for cluster in amr_clusters:
#         #gids = [ggraph.metadata['id'] for ggraph in gid_graphs]
#         gids = [ggraph.metadata['id'] for ggraph in cluster]
#         print(gids)
#
#         # Load the AMR file with penman and then extract the specific ids and put them in order
#         pgraphs = penman.load(gn, model=NoOpModel())
#         ordered_pgraphs = [None]*len(gids)
#         print(pgraphs)
#         print(ordered_pgraphs)
#         for pgraph in pgraphs:
#             gid = pgraph.metadata['id']
#             doc_idx = gids.index(gid) if gid in gids else None
#             if doc_idx is not None:
#                 ordered_pgraphs[doc_idx] = pgraph
#         assert None not in ordered_pgraphs
#
# gather_graphs()

# Simple function to print a list a strings in columns
def print_list_of_strings(items, col_w, max_w):
    cur_len = 0
    fmt = '%%-%ds' % col_w  # ie.. fmt = '%-8s'
    print('  ', end='')
    for item in items:
        print(fmt % item, end='')
        cur_len += 8
        if cur_len > max_w:
            print('\n  ', end='')
            cur_len = 0
    if cur_len != 0:
        print()


def run():
    #Load coreference model and test data
    model_dir = 'amr_coref/data/model_coref-v0.1.0/'

    print('Loading model from %s' % model_dir)
    inference = Inference(model_dir)

    # Get test data
    print('Loading test data')
    #ordered_pgraphs = gather_graphs()
    amr_clusters = cluster()
    for pgraphs in amr_clusters:


    # Cluster the data
    # This returns cluster_dict[relation_string] = [(graph_idx, variable), ...]
        print('Clustering')
        cluster_dict = inference.coreference(pgraphs)
        print()
#
    # Print out the clusters
        print('Clusters')
        for relation, clusters in cluster_dict.items():
            print(relation)
            cid_strings = ['%d.%s' % (graph_idx, var) for (graph_idx, var) in clusters]
            print_list_of_strings(cid_strings, col_w=8, max_w=120)


