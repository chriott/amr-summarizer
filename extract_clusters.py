import sys

from extract_summaries import extract_summaries

import re
import amrlib
import penman

def extract_amr_clusters(file):
    texts = extract_summaries(file)[:2]
    amr_clusters = []

    # Load spring parser.
    p = './model_parse_spring-v0_1_0'
    stog = amrlib.load_stog_model(model_dir=p)
    print('Parser loaded.')
    with open("amr-clusters.txt","w") as o:
        # Create a cluster for each text and add it to amr_clusters.
        cluster_id = 0
        amr_id = 0
        for paragraph, summary in texts:
            cluster_id += 1
            split_paragraph = paragraph.split("\n")
            parsed_amrs = stog.parse_sents(split_paragraph)
            for amr in parsed_amrs:
                amr_id += 1
                o.write("# ::cluster_id " + str(cluster_id) + " " + "::id " + str(amr_id) + "\n" + amr + "\n")


extract_amr_clusters(sys.argv[1])

