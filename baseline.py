import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys

def summarize(file):

    version = input("Which version would you like to use? [baseline] ")

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

    # Query where details of the sentence selection are specified
    if version == 'baseline':
        select = input("Choose: random or first?")
        n = int(input("How many sentences should the summary have?"))

        # Selection of sentences
        if select == 'random':
            if len(sentences) > int(n):
                summary_AMRs = random.sample(sentences,k=n)
            else:
                summary_AMRs = sentences

        if select == 'first':
            if len(sentences) > int(n):
                summary_AMRs = sentences[:int(n)]
            else:
                summary_AMRs = sentences

        # Parse the sentences
        parser_output = stog.parse_sents(summary_AMRs)

        # Generate the sentences
        sents, _ = gtos.generate(summary_AMRs, disable_progress=False, use_tense=False)

        # Write the sentences to an output file
        with open("summary.txt", "w") as o:
            o.writelines(sents)


summarize(sys.argv[1])
