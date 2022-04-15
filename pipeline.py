import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys

import coreference
import summarizer

def summarize(file, n=4):

    # Open file and save each sentence to a different line
    with open(file) as f:
        sentences = [sentence.rstrip() for sentence in f.readlines()]

    # Load the parser model.
    print('Loading parser...')
    p = './model_parse_spring-v0_1_0'
    stog = amrlib.load_stog_model(model_dir=p)
    print('done')

    # Load the generator model.
    print('Loading generator...')
    g = './model_generate_t5wtense-v0_1_0'
    gtos = amrlib.load_gtos_model(model_dir=g)
    print('done')

    # Parse the sentences, convert output list into
    # string of AMRs separated by double new lines
    print('Parsing...')
    parser_output = stog.parse_sents(sentences)
    AMRs = ""
    id=1
    for amr in parser_output:
        AMRs += "# ::id " + str(id) + "\n" + amr + "\n\n"
        id += 1

    # Write the AMRs to an output file
    with open("amrs.txt", "w") as o:
        o.writelines(AMRs)
    print('done')

    # Coreference resolution
    print('Resolving coreference...')
    coreferences = coreference.resolve_coreferences("amrs.txt")

    # Summarization
    print('Generating summary...')
    summary_AMRs = summarizer.summarizer('amrs.txt', coreferences, n)

    # Rename concepts

    # Generate the sentences
    sents, _ = gtos.generate(summary_AMRs, disable_progress=False, use_tense=False)

    # Write the sentences to an output file
    with open("pipeline_summary.txt", "w") as o:
        for sent in sents:
            o.write(sent)
    print('Done. Summary saved as \"pipeline_summary.txt\".\n')

    # Print out the summary
    print("Summary:")
    for sent in sents:
        print(sent)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        summarize(sys.argv[1])
    elif len(sys.argv) == 3:
        summarize(sys.argv[1], int(sys.argv[2]))
    else:
        file = input("Please enter an input file name:  ")
        summarize(file)

