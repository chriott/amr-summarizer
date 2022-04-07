import sys

import torch
import os
import penman
from penman.models.noop import NoOpModel
from penman.graph import Graph
import amr_coref
from   amr_coref.amr_coref.coref.inference import Inference

def gather_test_graphs(file):
    # For files in AMR cluster file format.
    with open(file, encoding='utf-8') as amrs:
        gn = penman.load(amrs, model=NoOpModel())
    gids = [graph.metadata['id'] for graph in gn]

    # Load the AMR file with penman and then extract the specific ids and put them in order
    pgraphs = penman.load(file, model=NoOpModel())
    ordered_pgraphs = [None]*len(gids)
    for pgraph in pgraphs:
        gid = pgraph.metadata['id']
        doc_idx = gids.index(gid) if gid in gids else None
        if doc_idx is not None:
            ordered_pgraphs[doc_idx] = pgraph
    assert None not in ordered_pgraphs
    return ordered_pgraphs

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

if __name__ == '__main__':
    model_dir = 'amr_coref/data/model_coref-v0.1.0/'

    # Load the model and test data
    print('Loading model from %s' % model_dir)
    inference = Inference(model_dir)

    # Get test data
    print('Loading test data')
    ordered_pgraphs = gather_test_graphs(sys.argv[1])

    # Cluster the data
    # This returns cluster_dict[relation_string] = [(graph_idx, variable), ...]
    print('Clustering')
    cluster_dict = inference.coreference(ordered_pgraphs)
    print(cluster_dict)


    # Print out the clusters
    print('Clusters')
    for relation, clusters in cluster_dict.items():
        print(relation)
        cid_strings = ['%d.%s' % (graph_idx, var) for (graph_idx, var) in clusters]
        print_list_of_strings(cid_strings, col_w=8, max_w=120)
