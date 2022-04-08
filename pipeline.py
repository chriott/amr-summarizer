import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys

import coreference
import summarizer

def summarize(file):

    # Open file and save each sentence to a different line
    with open(file) as f:
        sentences = [sentence.rstrip() for sentence in f.readlines()]

    # Load the parser model.
    p = './model_parse_spring-v0_1_0'
    stog = amrlib.load_stog_model(model_dir=p)
    print('Parser loaded.')

    # Load the generator model.
    g = './model_generate_t5wtense-v0_1_0'
    gtos = amrlib.load_gtos_model(model_dir=g)
    print('Generator loaded.')

    # Parse the sentences
    parser_output = stog.parse_sents(sentences)

	# Coreference resolution
	coreferences = resolve_coreferences(parser_output)

	# Summarization
	summary_AMRs = summarizer.summarizer(parser_output, coreferences, 4)

	# Rename variables

    # Generate the sentences
    sents, _ = gtos.generate(summary_AMRs, disable_progress=False, use_tense=False)

    # Write the sentences to an output file
    with open("summary.txt", "w") as o:
        o.writelines(sents)

summarize(sys.argv[1])