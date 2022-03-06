import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys


def pseudo_summarizer(file, option='-randomselect', summary_length=4):

    start = time.process_time()

    # Open file and save each sentence to a different line
    with open(file) as f:
        sentences = [sentence.rstrip() for sentence in f.readlines()]
        print('reading done')
        a = time.process_time() - start
        print('time taken to read in inputfile:', a, 'seconds')

    # Load amrlib models for parsing
    p = './model_parse_spring-v0_1_0'
    stog = amrlib.load_stog_model(model_dir=p)
    print('loading parser done')
    b = time.process_time() - a
    print('time taken to load parser:', b, 'seconds')

    # Convert each sentence to a list of multi-line AMRs
    parser_output = stog.parse_sents(sentences)  ## A list of penman notation AMRs.
    print('parsing done')
    c = time.process_time() - b
    print('time taken to parse sentences:', c, 'seconds')

    ## Option of selecting n random AMRs:

    if option == '-randomselect':
        if len(parser_output) > int(summary_length):
            summary_AMRs = random.choices(parser_output, k=int(summary_length))
        else:
            summary_AMRs = parser_output

        print('randomselect done')
        d = time.process_time() - c
        print('time taken to randomly select', summary_length, 'AMR graphs:', d, 'seconds')

    ## Option of using first n AMRs:

    if option == '-first':
        if len(AMRs) > int(summary_length):
            summary_AMRs = parser_output[:int(summary_length)]
        else:
            summary_AMRs = parser_output

        print('selection done')
        d = time.process_time() - c
        print('time taken to pick the first', summary_length, 'AMR graphs:', d, 'seconds')

    # Load amrlib models for parsing and generation
    g = './model_generate_t5wtense-v0_1_0'
    gtos = amrlib.load_gtos_model(model_dir=g)
    print('loading models done')
    e = time.process_time() - d
    print('time taken to load generator model:', e, 'seconds')

    # Generate sentences from the AMRs
    sents, _ = gtos.generate(summary_AMRs, disable_progress=False)

    print('generation done')
    f = time.process_time() - e
    print('time taken to generate sentences:', f, 'seconds')

    # Write sentences into output file
    with open("output.txt", "w") as o2:
        o2.writelines(sents)

        print('writing done')
        g = time.process_time() - f
        print('time taken to write sentences to output.txt:', g, 'seconds')


def main():
    pseudo_summarizer(sys.argv[1])

if __name__ == '__main__':
    main()

