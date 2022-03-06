import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys
import penman
import pstats


def generate(file):

    start = time.process_time()

    # Load amrlib models for parsing and generation
    g = './model_generate_t5wtense-v0_1_0'
    gtos = amrlib.load_gtos_model(model_dir=g)
    print('loading models done')
    a = time.process_time() - start
    print('time taken to load generator model:', a, 'seconds')


    # Read file into penman graphs
    AMRs = penman.load(file)

    # Decode the graph objects into a list of AMR strings
    String_AMRs = []
    for amr in AMRs:
        str_form = penman.encode(amr)
        String_AMRs.append(str_form)

    print('AMRs converted back to strings')
    b = time.process_time() - a
    print('time taken to convert AMR graphs back into strings:', b, 'seconds')

    # Generate sentences from the AMRs
    sents, _ = gtos.generate(String_AMRs, disable_progress=False)

    print('generation done')
    c = time.process_time() - b
    print('time taken to generate sentences:', c, 'seconds')

    # Write sentences into output file
    with open("generated_sentences.txt", "w") as o2:
        o2.writelines(sents)

        print('writing done')
        d = time.process_time() - c
        print('time taken to write sentences to generated_sentences.txt:',d,'seconds')


def main():
    generate(sys.argv[1])


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[2] == '-n':
            main()
        elif sys.argv[2] == '-ncalls':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('ncalls')
            stats.print_stats()
        elif sys.argv[2] == '-cumtime':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumtime')
            stats.print_stats()
    else:
        main()