# -*- coding: utf-8 -*-

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
proxy = "amr-release-3.0-amrs-proxy.txt"
dfa = "amr-release-3.0-amrs-dfa.txt"
proxy_1 = "proxy_1.txt"
summary_amr = "summary_amr.txt"


def gather_graphs():
  # open one of the files above twice
    fn = open(proxy_1, encoding='utf-8')
    gn = open(proxy_1, encoding='utf-8')
    
    # selection of graph IDs for proxy report
    # gids = ["PROXY_AFP_ENG_20020105_0162.5", "PROXY_AFP_ENG_20020105_0162.6", 
            # "PROXY_AFP_ENG_20020105_0162.7", "PROXY_AFP_ENG_20020105_0162.8", 
            # "PROXY_AFP_ENG_20020105_0162.9", "PROXY_AFP_ENG_20020105_0162.10", 
            # "PROXY_AFP_ENG_20020105_0162.11", "PROXY_AFP_ENG_20020105_0162.12", 
            # "PROXY_AFP_ENG_20020105_0162.13", "PROXY_AFP_ENG_20020105_0162.14", 
            # "PROXY_AFP_ENG_20020105_0162.15", ]
    
    # graph IDs for dfa
    #gids = ["DF-200-192400-625_7046.1",  "DF-200-192400-625_7046.2",  "DF-200-192400-625_7046.3",
     #       "DF-200-192400-625_7046.4",  "DF-200-192400-625_7046.5",  "DF-200-192400-625_7046.6",
     #       "DF-200-192400-625_7046.7",  "DF-200-192400-625_7046.8",  "DF-200-192400-625_7046.9",
     #       "DF-200-192400-625_7046.10", "DF-200-192400-625_7046.11", "DF-200-192400-625_7046.12",
     #       "DF-200-192400-625_7046.13", "DF-200-192400-625_7046.14", "DF-200-192400-625_7046.15",
     #       "DF-200-192400-625_7046.16", "DF-200-192400-625_7046.17", "DF-200-192400-625_7046.18"]

    # select graph IDs from the input
    # Use this for input files with only 1 document
    gid_graphs = penman.load(fn,model=NoOpModel())
    gids = [ggraph.metadata['id'] for ggraph in gid_graphs]
    print(gids)
    
    # Load the AMR file with penman and then extract the specific ids and put them in order
    pgraphs = penman.load(gn, model=NoOpModel())
    ordered_pgraphs = [None]*len(gids)
    for pgraph in pgraphs:
        gid = pgraph.metadata['id']
        doc_idx = gids.index(gid) if gid in gids else None
        if doc_idx is not None:
            ordered_pgraphs[doc_idx] = pgraph
    assert None not in ordered_pgraphs
    return ordered_pgraphs

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

# Load coreference model and test data
model_dir = 'amr_coref/data/model_coref-v0.1.0/'

print('Loading model from %s' % model_dir)
inference = Inference(model_dir)

# Get test data
print('Loading test data')
ordered_pgraphs = gather_graphs()

# Cluster the data
# This returns cluster_dict[relation_string] = [(graph_idx, variable), ...]
print('Clustering')
cluster_dict = inference.coreference(ordered_pgraphs)
print()

# Print out the clusters
print('Clusters')
for relation, clusters in cluster_dict.items():
  print(relation)
  cid_strings = ['%d.%s' % (graph_idx, var) for (graph_idx, var) in clusters]
  print_list_of_strings(cid_strings, col_w=8, max_w=120)

